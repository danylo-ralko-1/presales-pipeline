"""Enrich command: fetch Figma screenshots + ADO stories → enrichment_bundle.json.

Same screenshot approach as validate. Reuses existing screenshots if present.
Supports --story-ids to filter which ADO stories are included.
The actual enrichment (writing detailed AC) happens in conversation.
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


def run(proj: dict, figma_link: str, story_ids: list[str] | None = None) -> None:
    """Fetch Figma screenshots and ADO stories into enrichment_bundle.json."""
    project_name = proj["project"]
    click.secho(f"\n  Preparing AC enrichment for '{project_name}'", bold=True)
    click.echo(f"  Figma link: {figma_link}")

    if story_ids:
        click.echo(f"  Target stories: {', '.join(story_ids)}")
        click.echo(f"  Mode: TARGETED\n")
    else:
        click.echo(f"  Mode: FULL (all stories)\n")

    # Get Figma credentials
    figma_pat = _get_figma_pat(proj)
    if not figma_pat:
        return

    file_key = _extract_file_key(figma_link)
    if not file_key:
        click.secho("  ✗ Could not extract file key from Figma URL", fg="red")
        click.echo("    Expected: https://www.figma.com/design/ABC123/ProjectName")
        return

    # Fetch or reuse screenshots
    screens = _get_screenshots(proj, figma_pat, file_key)
    if screens is None:
        return

    # Fetch ADO stories (optionally filtered)
    stories = _fetch_ado_stories(proj, story_ids)
    if stories is None:
        return

    # Save enrichment bundle
    bundle = {
        "figma_file_key": file_key,
        "screens": screens,
        "stories": stories,
    }
    bundle_path = get_output_path(proj, "enrichment_bundle.json")
    with open(bundle_path, "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2, ensure_ascii=False)

    click.secho(f"\n  ✓ Enrichment bundle ready", fg="green", bold=True)
    click.echo(f"    Bundle: {bundle_path}")
    click.echo(f"    Screens: {len(screens)}")
    click.echo(f"    Stories: {len(stories)}")
    click.echo(f"\n  Next: analyze the bundle in conversation to generate detailed AC.")


def _get_screenshots(proj: dict, pat: str, file_key: str) -> list[dict] | None:
    """Reuse existing screenshots or fetch new ones."""
    screenshots_dir = Path(proj["path"]) / "output" / "screenshots"

    # Check if screenshots already exist
    if screenshots_dir.exists():
        existing = list(screenshots_dir.glob("*.png"))
        if existing:
            click.echo(f"  Reusing {len(existing)} existing screenshots from output/screenshots/")
            screens = []
            for fp in sorted(existing):
                # Try to reconstruct metadata from filename
                screens.append({
                    "name": fp.stem.rsplit("_", 1)[0].replace("_", " "),
                    "node_id": "",
                    "page": "",
                    "screenshot_path": str(fp),
                })
            return screens

    # No existing screenshots — fetch from Figma
    click.echo("  No existing screenshots found, fetching from Figma...")
    return _fetch_figma_screenshots(proj, pat, file_key)


def _fetch_figma_screenshots(proj: dict, pat: str, file_key: str) -> list[dict] | None:
    """Fetch file structure, collect frame IDs, download screenshots."""
    try:
        file_data = _figma_get(pat, f"/v1/files/{file_key}?depth=2")
    except Exception as e:
        click.secho(f"  ✗ Failed to fetch Figma file: {e}", fg="red")
        return None

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

    click.echo(f"  Found {len(frames)} frames")

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

        for frame in batch:
            nid = frame["node_id"]
            url = image_urls.get(nid)
            if not url:
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

    click.secho(f"  ✓ Downloaded {len(screens)} screenshots", fg="green")
    return screens


def _fetch_ado_stories(proj: dict, story_ids: list[str] | None = None) -> list[dict] | None:
    """Fetch stories from ADO, optionally filtered by IDs."""
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

    # Filter by story IDs if provided
    if story_ids:
        ids_set = set(str(sid) for sid in story_ids)
        raw_stories = [s for s in raw_stories if str(s.get("id", "")) in ids_set]
        if not raw_stories:
            click.secho(f"  ⚠ None of the specified story IDs found in ADO", fg="yellow")
            return []
        click.echo(f"  Found {len(raw_stories)} of {len(story_ids)} requested stories")
    else:
        click.echo(f"  Found {len(raw_stories)} stories")

    stories = []
    for s in raw_stories:
        ac = s.get("acceptance_criteria", "")
        if not ac:
            fields = s.get("fields", {})
            ac = fields.get("Microsoft.VSTS.Common.AcceptanceCriteria", "")
        stories.append({
            "ado_id": s.get("id"),
            "title": s.get("title", ""),
            "description": s.get("description", ""),
            "acceptance_criteria": ac,
            "tags": s.get("tags", ""),
            "state": s.get("state", ""),
        })
    return stories


def _get_figma_pat(proj: dict) -> str | None:
    """Read Figma PAT from project.yaml."""
    pat = proj.get("figma", {}).get("pat", "")
    if not pat:
        click.secho("  ✗ Figma PAT not configured.", fg="red")
        click.echo("    Add figma.pat to project.yaml")
        return None
    return pat


def _extract_file_key(figma_link: str) -> str | None:
    """Extract file key from a Figma URL."""
    m = re.search(r"figma\.com/(?:design|file)/([a-zA-Z0-9]+)", figma_link)
    return m.group(1) if m else None


def _figma_get(pat: str, endpoint: str) -> dict:
    """Make an authenticated GET request to the Figma REST API."""
    url = f"https://api.figma.com{endpoint}"
    req = urllib.request.Request(url, headers={"X-FIGMA-TOKEN": pat})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _download_file(url: str, dest: Path) -> None:
    """Download a file from a URL."""
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as resp:
        dest.write_bytes(resp.read())
