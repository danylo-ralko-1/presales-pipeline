"""Validate command: fetch Figma screenshots + ADO stories → validation_bundle.json.

Fetches all top-level frame screenshots from a Figma file using the REST API,
downloads them locally, fetches all ADO stories, and bundles everything into
validation_bundle.json for analysis in conversation.
"""

import json
import re
import urllib.parse
import urllib.request
import urllib.error
import click
from pathlib import Path

from core.config import get_output_path, update_state
from core import ado as ado_client


def run(proj: dict, figma_link: str) -> None:
    """Fetch Figma screenshots and ADO stories into validation_bundle.json."""
    project_name = proj["project"]
    click.secho(f"\n  Preparing design validation for '{project_name}'", bold=True)
    click.echo(f"  Figma link: {figma_link}\n")

    # Get Figma credentials
    figma_pat = _get_figma_pat(proj)
    if not figma_pat:
        return

    file_key = _extract_file_key(figma_link)
    if not file_key:
        click.secho("  ✗ Could not extract file key from Figma URL", fg="red")
        click.echo("    Expected: https://www.figma.com/design/ABC123/ProjectName")
        return

    # Step 1-3: Fetch screenshots from Figma
    click.echo("  Fetching Figma file structure...")
    screens = _fetch_figma_screenshots(proj, figma_pat, file_key)
    if screens is None:
        return
    click.secho(f"  ✓ Downloaded {len(screens)} screenshots\n", fg="green")

    # Step 4: Fetch ADO stories
    stories = _fetch_ado_stories(proj)
    if stories is None:
        return

    # Step 5: Save validation bundle
    bundle = {
        "figma_file_key": file_key,
        "screens": screens,
        "stories": stories,
    }
    bundle_path = get_output_path(proj, "validation_bundle.json")
    with open(bundle_path, "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2, ensure_ascii=False)

    update_state(proj, validated=True)

    click.secho(f"\n  ✓ Validation bundle ready", fg="green", bold=True)
    click.echo(f"    Bundle: {bundle_path}")
    click.echo(f"    Screens: {len(screens)}")
    click.echo(f"    Stories: {len(stories)}")
    click.echo(f"\n  Next: analyze the bundle in conversation to find gaps.")


def _get_figma_pat(proj: dict) -> str | None:
    """Read Figma PAT from project.yaml."""
    pat = proj.get("figma", {}).get("pat", "")
    if not pat:
        click.secho("  ✗ Figma PAT not configured.", fg="red")
        click.echo("    Add figma.pat to project.yaml")
        click.echo("    Get one from: figma.com → Settings → Personal Access Tokens")
        return None
    return pat


def _extract_file_key(figma_link: str) -> str | None:
    """Extract file key from a Figma URL."""
    # Matches /design/KEY/ or /file/KEY/
    m = re.search(r"figma\.com/(?:design|file)/([a-zA-Z0-9]+)", figma_link)
    return m.group(1) if m else None


def _fetch_figma_screenshots(proj: dict, pat: str, file_key: str) -> list[dict] | None:
    """Fetch Figma file structure, collect frame IDs, download screenshots."""
    # Step 1: GET file structure
    try:
        file_data = _figma_get(pat, f"/v1/files/{file_key}?depth=2")
    except Exception as e:
        click.secho(f"  ✗ Failed to fetch Figma file: {e}", fg="red")
        return None

    # Step 2: Collect top-level frame node IDs per page
    frames = []
    document = file_data.get("document", {})
    for page in document.get("children", []):
        page_name = page.get("name", "Unknown Page")
        for child in page.get("children", []):
            if child.get("type") == "FRAME":
                frames.append({
                    "name": child.get("name", "Untitled"),
                    "node_id": child.get("id"),
                    "page": page_name,
                })

    if not frames:
        click.secho("  ✗ No frames found in Figma file", fg="red")
        return None

    click.echo(f"  Found {len(frames)} frames across {len(document.get('children', []))} pages")

    # Step 3: Get screenshot URLs (batch — max 50 IDs per request)
    screenshots_dir = Path(proj["path"]) / "output" / "screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    screens = []
    batch_size = 50
    for i in range(0, len(frames), batch_size):
        batch = frames[i:i + batch_size]
        node_ids = ",".join(f["node_id"] for f in batch)
        ids_encoded = urllib.parse.quote(node_ids, safe=",:")

        click.echo(f"  Requesting screenshots ({i + 1}-{min(i + batch_size, len(frames))}/{len(frames)})...")
        try:
            images_data = _figma_get(pat, f"/v1/images/{file_key}?ids={ids_encoded}&format=png&scale=2")
        except Exception as e:
            click.secho(f"  ⚠ Failed to get image URLs: {e}", fg="yellow")
            continue

        image_urls = images_data.get("images", {})

        # Step 4: Download each screenshot
        for frame in batch:
            nid = frame["node_id"]
            url = image_urls.get(nid)
            if not url:
                click.secho(f"    ⚠ No image URL for '{frame['name']}'", fg="yellow")
                continue

            safe_name = re.sub(r'[^\w\-.]', '_', frame["name"])
            filename = f"{safe_name}_{nid.replace(':', '-')}.png"
            filepath = screenshots_dir / filename

            try:
                _download_file(url, filepath)
                screens.append({
                    "name": frame["name"],
                    "node_id": nid,
                    "page": frame["page"],
                    "screenshot_path": str(filepath),
                })
            except Exception as e:
                click.secho(f"    ⚠ Failed to download '{frame['name']}': {e}", fg="yellow")

    return screens


def _fetch_ado_stories(proj: dict) -> list[dict] | None:
    """Fetch all stories from ADO with full details."""
    try:
        config = ado_client.from_project(proj)
    except ValueError as e:
        click.secho(f"  ✗ ADO not configured: {e}", fg="red")
        return None

    click.echo("  Fetching stories from ADO...")
    try:
        data = ado_client.get_all_work_items(config)
    except Exception as e:
        click.secho(f"  ✗ ADO fetch failed: {e}", fg="red")
        return None

    raw_stories = data.get("stories", [])
    if not raw_stories:
        click.secho("  ⚠ No stories found in ADO", fg="yellow")
        return []

    click.echo(f"  Found {len(raw_stories)} stories")

    stories = []
    for s in raw_stories:
        stories.append({
            "ado_id": s.get("id"),
            "title": s.get("title", ""),
            "description": s.get("description", ""),
            "acceptance_criteria": _get_ac_field(s),
            "tags": s.get("tags", ""),
            "state": s.get("state", ""),
        })
    return stories


def _get_ac_field(story: dict) -> str:
    """Extract acceptance criteria from an ADO story dict.

    The get_all_work_items helper flattens fields, but AC may be nested
    under the raw fields key depending on the query.
    """
    # Try the flattened key first (our ado module normalises this)
    ac = story.get("acceptance_criteria", "")
    if ac:
        return ac
    # Try the raw field path
    fields = story.get("fields", {})
    return fields.get("Microsoft.VSTS.Common.AcceptanceCriteria", "")


def _figma_get(pat: str, endpoint: str) -> dict:
    """Make an authenticated GET request to the Figma REST API."""
    url = f"https://api.figma.com{endpoint}"
    req = urllib.request.Request(url, headers={"X-FIGMA-TOKEN": pat})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _download_file(url: str, dest: Path) -> None:
    """Download a file from a URL to a local path."""
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as resp:
        dest.write_bytes(resp.read())
