"""Push command: create work items in Azure DevOps from push_ready.json.

Reads pre-generated user stories and acceptance criteria from push_ready.json
(generated in conversation before running this command).
Falls back to breakdown.json if push_ready.json doesn't exist.
Creates Epics → Features → User Stories (with discipline Tasks) in ADO.
"""

import json
import click

from core.config import get_output_path, update_state
from core.context import invalidate_downstream
from core import ado as ado_client


def run(proj: dict, dry_run: bool = False) -> None:
    """Push stories to Azure DevOps from push_ready.json (or breakdown.json fallback)."""
    project_name = proj["project"]
    click.secho(f"\n  Pushing to Azure DevOps for '{project_name}'", bold=True)

    if dry_run:
        click.secho("  [DRY RUN — no changes will be made to ADO]\n", fg="yellow")

    # Load data source
    push_data, source_name = _load_data(proj)
    if not push_data:
        return
    click.echo(f"  Source: {source_name}")

    # Test ADO connection
    if not dry_run:
        try:
            config = ado_client.from_project(proj)
        except ValueError as e:
            click.secho(f"  ✗ {e}", fg="red")
            return

        click.echo("  Testing ADO connection...")
        if not ado_client.test_connection(config):
            click.secho("  ✗ Failed to connect to ADO. Check credentials.", fg="red")
            return
        click.secho("  ✓ Connected to ADO\n", fg="green")

    # Count totals
    total_stories = sum(
        len(feature.get("stories", []))
        for epic in push_data.get("epics", [])
        for feature in epic.get("features", [])
    )
    total_epics = len(push_data.get("epics", []))
    total_features = sum(len(e.get("features", [])) for e in push_data.get("epics", []))

    click.echo(f"  Will create: {total_epics} epics, {total_features} features, {total_stories} stories")
    if not dry_run and not click.confirm("  Proceed?", default=True):
        return

    # Track created IDs for hierarchy
    created = {"epics": {}, "features": {}, "stories": []}
    story_index = 0

    for epic in push_data.get("epics", []):
        epic_name = epic.get("name", "Unknown Epic")
        epic_id_key = epic.get("id", epic_name)
        epic_desc = epic.get("description", "")

        feature_names = [f.get("name", "?") for f in epic.get("features", [])]
        epic_html = (
            f"<h3>{epic_name}</h3>"
            f"<p>{epic_desc}</p>"
            f"<p><b>Features:</b></p><ul>"
            + "".join(f"<li>{fn}</li>" for fn in feature_names)
            + "</ul>"
        )

        click.secho(f"  Epic: {epic_name}", fg="cyan", bold=True)

        if dry_run:
            epic_ado_id = None
            click.echo(f"    [DRY RUN] Would create Epic: {epic_name}")
        else:
            result = ado_client.create_work_item(
                config, "Epic", epic_name,
                description=epic_html,
                tags=f"presales;{project_name}",
            )
            epic_ado_id = result.get("id")
            click.echo(f"    ✓ Created Epic #{epic_ado_id}")

        created["epics"][epic_id_key] = epic_ado_id

        for feature in epic.get("features", []):
            feat_name = feature.get("name", "Unknown Feature")
            feat_id_key = feature.get("id", feat_name)

            story_names = [s.get("title", "?") for s in feature.get("stories", [])]
            feat_html = (
                f"<h4>{feat_name}</h4>"
                f"<p><b>Stories:</b></p><ul>"
                + "".join(f"<li>{sn}</li>" for sn in story_names)
                + "</ul>"
            )

            click.echo(f"    Feature: {feat_name}")

            if dry_run:
                feat_ado_id = None
                click.echo(f"      [DRY RUN] Would create Feature: {feat_name}")
            else:
                result = ado_client.create_work_item(
                    config, "Feature", feat_name,
                    description=feat_html,
                    tags=f"presales;{project_name};{epic_name}",
                    parent_id=epic_ado_id,
                )
                feat_ado_id = result.get("id")
                click.echo(f"      ✓ Created Feature #{feat_ado_id}")

            created["features"][feat_id_key] = feat_ado_id

            for story in feature.get("stories", []):
                story_index += 1
                story_title = story.get("title", "Unknown Story")
                story_id = story.get("id", f"US-{story_index:03d}")

                click.echo(f"      [{story_index}/{total_stories}] {story_title}")

                # Read user story and AC from push_ready.json fields;
                # fallback: breakdown.json has acceptance_criteria as a string
                user_story_text = story.get("user_story", f"As a user, I want to {story_title.lower()}.")
                ac_list = story.get("acceptance_criteria", [])

                # Effort
                fe = story.get("fe_days", 0)
                be = story.get("be_days", 0)
                devops = story.get("devops_days", 0)
                design = story.get("design_days", 0)
                total = fe + be + devops + design

                description_html = _build_story_description(
                    user_story_text, epic_name, feat_name
                )
                ac_html = _build_ac_html(ac_list)

                if dry_run:
                    click.echo(f"        [DRY RUN] Would create User Story: {story_title}")
                    click.echo(f"        User story: {user_story_text[:100]}...")
                else:
                    result = ado_client.create_work_item(
                        config, "User Story", story_title,
                        description=description_html,
                        tags=f"presales;{project_name};{epic_name};{feat_name}",
                        parent_id=feat_ado_id,
                        extra_fields={
                            "Microsoft.VSTS.Scheduling.Effort": total,
                            "Microsoft.VSTS.Common.AcceptanceCriteria": ac_html,
                        },
                    )
                    story_ado_id = result.get("id")
                    click.secho(f"        ✓ Created Story #{story_ado_id}", fg="green")

                    # Create discipline tasks
                    _create_tasks(config, project_name, story_ado_id, story_title, story)

                    created["stories"].append({
                        "ado_id": story_ado_id,
                        "id": story_id,
                        "title": story_title,
                        "epic": epic_name,
                        "feature": feat_name,
                    })

    # Save mapping file
    mapping_path = get_output_path(proj, "ado_mapping.json")
    with open(mapping_path, "w", encoding="utf-8") as f:
        json.dump(created, f, indent=2)

    # Update state
    if not dry_run:
        invalidate_downstream(proj, "push")
        update_state(proj, ado_pushed=True)

    click.secho(f"\n  ✓ Push complete", fg="green", bold=True)
    click.echo(f"    Created: {total_epics} epics, {total_features} features, {story_index} stories")
    click.echo(f"    Mapping: {mapping_path}")
    click.echo(f"\n    When designs are ready, run: presales enrich {project_name} --figma-link <url>")


def _create_tasks(config, project_name: str, parent_id: int,
                   story_title: str, story: dict) -> None:
    """Create FE / BE / DevOps tasks as children of the user story."""
    disciplines = [
        ("fe_days", "FE"),
        ("be_days", "BE"),
        ("devops_days", "DevOps"),
    ]
    for field, prefix in disciplines:
        days = story.get(field, 0)
        if days and days > 0:
            task_title = f"[{prefix}] {story_title}"
            try:
                ado_client.create_work_item(
                    config, "Task", task_title,
                    parent_id=parent_id,
                    tags=f"presales;{project_name}",
                    extra_fields={
                        "Microsoft.VSTS.Scheduling.Effort": days,
                    },
                )
            except Exception as e:
                click.secho(f"          ⚠ Failed to create {prefix} task: {e}", fg="yellow")


def _build_story_description(user_story: str, epic: str, feature: str) -> str:
    """Build HTML description — user story text + epic/feature table only."""
    return f"""<p><em>{user_story}</em></p>

<table>
<tr><td><b>Epic</b></td><td>{epic}</td></tr>
<tr><td><b>Feature</b></td><td>{feature}</td></tr>
</table>""".strip()


def _build_ac_html(ac_list) -> str:
    """Build HTML for acceptance criteria."""
    if isinstance(ac_list, str):
        return f"<p>{ac_list}</p>"

    if isinstance(ac_list, list) and ac_list:
        items = "".join(f"<li>{ac}</li>" for ac in ac_list if ac)
        return f"<ol>{items}</ol>"

    return "<p>To be defined when designs are ready.</p>"


def _load_data(proj: dict) -> tuple[dict | None, str]:
    """Load push_ready.json, falling back to breakdown.json."""
    # Try push_ready.json first
    pr_path = get_output_path(proj, "push_ready.json")
    if pr_path.exists():
        try:
            with open(pr_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if "epics" in data:
                return data, "push_ready.json"
        except json.JSONDecodeError as e:
            click.secho(f"  ⚠ Failed to parse push_ready.json: {e}", fg="yellow")

    # Fallback to breakdown.json
    bd_path = get_output_path(proj, "breakdown.json")
    if bd_path.exists():
        try:
            with open(bd_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if "epics" in data:
                click.secho("  ℹ Using breakdown.json (push_ready.json not found)", fg="yellow")
                return data, "breakdown.json"
        except json.JSONDecodeError as e:
            click.secho(f"  ✗ Failed to parse breakdown.json: {e}", fg="red")

    click.secho("  ✗ No data source found.", fg="red")
    click.echo("    Generate push_ready.json in conversation, or ensure breakdown.json exists.")
    return None, ""
