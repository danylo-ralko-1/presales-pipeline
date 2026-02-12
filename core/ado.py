"""Azure DevOps REST API client for work item management."""

import json
import time
import base64
import click
import urllib.parse
import urllib.request
import urllib.error
from dataclasses import dataclass


ADO_API_VERSION = "7.1"
RATE_LIMIT_DELAY = 0.3  # seconds between API calls to avoid throttling


@dataclass
class AdoConfig:
    """ADO connection configuration."""
    organization: str
    project: str
    pat: str

    @property
    def base_url(self) -> str:
        proj = urllib.parse.quote(self.project, safe="")
        return f"https://dev.azure.com/{self.organization}/{proj}/_apis"

    @property
    def auth_header(self) -> str:
        token = base64.b64encode(f":{self.pat}".encode()).decode()
        return f"Basic {token}"


def from_project(proj: dict) -> AdoConfig:
    """Create AdoConfig from project config dict."""
    ado = proj.get("ado", {})
    org = ado.get("organization", "")
    project = ado.get("project", "")
    pat = ado.get("pat", "")
    if not all([org, project, pat]):
        raise ValueError(
            "ADO not configured. Ensure ado.organization, ado.project, and ado.pat "
            "are set in project.yaml"
        )
    return AdoConfig(organization=org, project=project, pat=pat)


def create_work_item(
    config: AdoConfig,
    work_item_type: str,
    title: str,
    description: str = "",
    tags: str = "",
    parent_id: int | None = None,
    extra_fields: dict | None = None,
) -> dict:
    """
    Create a work item in Azure DevOps.

    Args:
        config: ADO connection config
        work_item_type: "Epic", "Feature", or "User Story"
        title: Work item title
        description: HTML description
        tags: Semicolon-separated tags
        parent_id: Parent work item ID for hierarchy
        extra_fields: Additional field path → value pairs

    Returns:
        Created work item dict from ADO API
    """
    wit_encoded = urllib.parse.quote(work_item_type, safe="")
    url = f"{config.base_url}/wit/workitems/${wit_encoded}?api-version={ADO_API_VERSION}"

    # Build patch document
    patches = [
        {"op": "add", "path": "/fields/System.Title", "value": title},
    ]

    if description:
        patches.append({
            "op": "add",
            "path": "/fields/System.Description",
            "value": description,
        })

    if tags:
        patches.append({
            "op": "add",
            "path": "/fields/System.Tags",
            "value": tags,
        })

    if parent_id is not None:
        patches.append({
            "op": "add",
            "path": "/relations/-",
            "value": {
                "rel": "System.LinkTypes.Hierarchy-Reverse",
                "url": f"https://dev.azure.com/{config.organization}/_apis/wit/workItems/{parent_id}",
            },
        })

    if extra_fields:
        for field_path, value in extra_fields.items():
            if not field_path.startswith("/fields/"):
                field_path = f"/fields/{field_path}"
            patches.append({"op": "add", "path": field_path, "value": value})

    return _api_request(config, url, method="POST", body=patches,
                        content_type="application/json-patch+json")


def update_work_item(
    config: AdoConfig,
    work_item_id: int,
    fields: dict,
) -> dict:
    """
    Update fields on an existing work item.

    Args:
        config: ADO connection config
        work_item_id: ID of work item to update
        fields: field path → value pairs to update

    Returns:
        Updated work item dict
    """
    url = f"{config.base_url}/wit/workitems/{work_item_id}?api-version={ADO_API_VERSION}"

    patches = []
    for field_path, value in fields.items():
        if not field_path.startswith("/fields/"):
            field_path = f"/fields/{field_path}"
        patches.append({"op": "add", "path": field_path, "value": value})

    return _api_request(config, url, method="PATCH", body=patches,
                        content_type="application/json-patch+json")


def get_work_items_by_query(config: AdoConfig, wiql: str) -> list[dict]:
    """
    Query work items using WIQL (Work Item Query Language).

    Args:
        config: ADO connection config
        wiql: WIQL query string

    Returns:
        List of work item dicts with full details
    """
    url = f"{config.base_url}/wit/wiql?api-version={ADO_API_VERSION}"
    result = _api_request(config, url, method="POST", body={"query": wiql})

    work_items = result.get("workItems", [])
    if not work_items:
        return []

    # Fetch full details in batches of 200
    ids = [wi["id"] for wi in work_items]
    detailed = []
    for i in range(0, len(ids), 200):
        batch = ids[i:i + 200]
        id_str = ",".join(str(x) for x in batch)
        detail_url = (
            f"{config.base_url}/wit/workitems?ids={id_str}"
            f"&$expand=relations&api-version={ADO_API_VERSION}"
        )
        batch_result = _api_request(config, detail_url, method="GET")
        detailed.extend(batch_result.get("value", []))

    return detailed


def get_all_stories(config: AdoConfig, tag_filter: str | None = None) -> list[dict]:
    """Get all user stories, optionally filtered by tag."""
    wiql = (
        "SELECT [System.Id], [System.Title], [System.Description], "
        "[System.Tags], [System.State] "
        "FROM WorkItems WHERE [System.WorkItemType] = 'User Story'"
    )
    if tag_filter:
        wiql += f" AND [System.Tags] CONTAINS '{tag_filter}'"
    wiql += " ORDER BY [System.Id] ASC"

    return get_work_items_by_query(config, wiql)


def get_all_work_items(config: AdoConfig) -> dict:
    """
    Get all epics, features, and stories organized hierarchically.

    Returns:
        {
            "epics": [{"id": ..., "title": ..., "features": [...]}],
            "features": [...],
            "stories": [...]
        }
    """
    wiql = (
        "SELECT [System.Id], [System.Title], [System.WorkItemType], "
        "[System.Description], [System.Tags], [System.State] "
        "FROM WorkItems WHERE [System.WorkItemType] IN ('Epic', 'Feature', 'User Story') "
        "ORDER BY [System.WorkItemType] ASC, [System.Id] ASC"
    )
    items = get_work_items_by_query(config, wiql)

    epics = []
    features = []
    stories = []

    for item in items:
        fields = item.get("fields", {})
        wit = fields.get("System.WorkItemType", "")
        entry = {
            "id": item.get("id"),
            "title": fields.get("System.Title", ""),
            "description": fields.get("System.Description", ""),
            "tags": fields.get("System.Tags", ""),
            "state": fields.get("System.State", ""),
            "type": wit,
        }
        if wit == "Epic":
            epics.append(entry)
        elif wit == "Feature":
            features.append(entry)
        elif wit == "User Story":
            stories.append(entry)

    return {"epics": epics, "features": features, "stories": stories}


def test_connection(config: AdoConfig) -> bool:
    """Test ADO connection by fetching project info."""
    try:
        url = (
            f"https://dev.azure.com/{config.organization}/_apis/projects/"
            f"{urllib.parse.quote(config.project, safe='')}?api-version={ADO_API_VERSION}"
        )
        result = _api_request(config, url, method="GET")
        return "id" in result
    except Exception:
        return False


def upload_attachment(
    config: AdoConfig,
    work_item_id: int,
    file_path: str,
    filename: str | None = None,
    comment: str = "",
) -> dict:
    """
    Upload a file as an attachment to an ADO work item.

    Two-step process:
    1. Upload the file to get an attachment URL
    2. Link the attachment to the work item

    Args:
        config: ADO connection config
        work_item_id: ID of the work item to attach to
        file_path: Local path to the file
        filename: Display name (defaults to basename of file_path)
        comment: Optional comment for the attachment

    Returns:
        Attachment metadata dict from ADO API
    """
    from pathlib import Path
    fp = Path(file_path)
    if not fp.exists():
        raise FileNotFoundError(f"Attachment file not found: {file_path}")

    if not filename:
        filename = fp.name

    # Step 1: Upload the file blob
    encoded_name = urllib.parse.quote(filename, safe="")
    upload_url = (
        f"https://dev.azure.com/{config.organization}/{urllib.parse.quote(config.project, safe='')}/"
        f"_apis/wit/attachments?fileName={encoded_name}&api-version={ADO_API_VERSION}"
    )

    file_data = fp.read_bytes()
    headers = {
        "Authorization": config.auth_header,
        "Content-Type": "application/octet-stream",
    }
    req = urllib.request.Request(upload_url, data=file_data, headers=headers, method="POST")

    time.sleep(RATE_LIMIT_DELAY)
    with urllib.request.urlopen(req) as resp:
        upload_result = json.loads(resp.read().decode("utf-8"))

    attachment_url = upload_result.get("url", "")

    # Step 2: Link the attachment to the work item
    patches = [{
        "op": "add",
        "path": "/relations/-",
        "value": {
            "rel": "AttachedFile",
            "url": attachment_url,
            "attributes": {"comment": comment or filename},
        },
    }]

    wi_url = f"{config.base_url}/wit/workitems/{work_item_id}?api-version={ADO_API_VERSION}"
    return _api_request(config, wi_url, method="PATCH", body=patches,
                        content_type="application/json-patch+json")


def get_child_work_items(config: AdoConfig, parent_id: int) -> list[dict]:
    """Get child work items (tasks) of a parent work item."""
    wiql = (
        f"SELECT [System.Id], [System.Title], [System.WorkItemType] "
        f"FROM WorkItemLinks "
        f"WHERE ([Source].[System.Id] = {parent_id}) "
        f"AND ([System.Links.LinkType] = 'System.LinkTypes.Hierarchy-Forward') "
        f"MODE (MustContain)"
    )
    url = f"{config.base_url}/wit/wiql?api-version={ADO_API_VERSION}"
    result = _api_request(config, url, method="POST", body={"query": wiql})

    # Extract target (child) IDs — skip the source itself
    child_ids = []
    for relation in result.get("workItemRelations", []):
        target = relation.get("target", {})
        tid = target.get("id")
        if tid and tid != parent_id:
            child_ids.append(tid)

    if not child_ids:
        return []

    # Fetch details
    id_str = ",".join(str(x) for x in child_ids)
    detail_url = (
        f"{config.base_url}/wit/workitems?ids={id_str}"
        f"&api-version={ADO_API_VERSION}"
    )
    batch_result = _api_request(config, detail_url, method="GET")
    return batch_result.get("value", [])


# --- Internal helpers ---

def _api_request(
    config: AdoConfig,
    url: str,
    method: str = "GET",
    body: dict | list | None = None,
    content_type: str = "application/json",
) -> dict:
    """Make an authenticated API request to ADO."""
    headers = {
        "Authorization": config.auth_header,
        "Content-Type": content_type,
    }

    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    retries = 3
    for attempt in range(retries):
        try:
            time.sleep(RATE_LIMIT_DELAY)
            with urllib.request.urlopen(req) as resp:
                resp_body = resp.read().decode("utf-8")
                return json.loads(resp_body) if resp_body else {}
        except urllib.error.HTTPError as e:
            body_text = ""
            try:
                body_text = e.read().decode("utf-8")
            except Exception:
                pass

            if e.code == 429:  # Rate limited
                delay = 2 ** (attempt + 1)
                click.secho(f"    Rate limited, waiting {delay}s...", fg="yellow")
                time.sleep(delay)
                continue
            elif e.code >= 500 and attempt < retries - 1:
                delay = 2 ** attempt
                time.sleep(delay)
                continue
            else:
                raise RuntimeError(
                    f"ADO API error {e.code}: {e.reason}\n"
                    f"URL: {url}\n"
                    f"Response: {body_text[:500]}"
                )

    raise RuntimeError(f"ADO API request failed after {retries} retries: {url}")
