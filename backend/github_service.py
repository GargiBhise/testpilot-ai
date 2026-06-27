from urllib.parse import urlparse
from repo_analyzer import detect_framework, discover_pages, get_ui_files, discover_workflows, extract_ui_elements, extract_user_actions
import httpx
from fastapi import HTTPException
from context_builder import build_application_context


def get_repo_metadata(repo_url: str):
    parsed_url = urlparse(repo_url)
    path_parts = parsed_url.path.strip("/").split("/")

    if len(path_parts) < 2:
        raise HTTPException(status_code=400, detail="Invalid GitHub repository URL")

    owner = path_parts[0]
    repo = path_parts[1]

    github_api_url = f"https://api.github.com/repos/{owner}/{repo}"
    
    response = httpx.get(github_api_url)
    
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="GitHub repository not found")
    
    repo_data = response.json()
    file_tree = get_repo_file_tree(owner, repo, repo_data["default_branch"])
    analysis = detect_framework(file_tree)
    pages = discover_pages(file_tree)
    ui_files = get_ui_files(file_tree)
    workflows = discover_workflows(pages)
    ui_elements = []

    for file_path in ui_files:
        content = get_file_content(owner, repo, repo_data["default_branch"], file_path)
        elements = extract_ui_elements(file_path, content)
        ui_elements.append(elements)

    user_actions = []

    for file_path in ui_files:
        content = get_file_content(owner, repo, repo_data["default_branch"], file_path)
        actions = extract_user_actions(file_path, content)
        user_actions.extend(actions)
    

    repo_result = {
    "owner": owner,
    "repo": repo,
    "full_name": repo_data["full_name"],
    "description": repo_data["description"],
    "default_branch": repo_data["default_branch"],
    "language": repo_data["language"],
    "stars": repo_data["stargazers_count"],
    "github_url": repo_data["html_url"],
    "file_count": len(file_tree),
    "sample_files": file_tree[:30],
    "analysis": analysis,
    "pages": pages,
    "ui_files": ui_files,
    "workflows": workflows,
    "ui_elements": ui_elements,
    "user_actions": user_actions,
}

    application_context = build_application_context(repo_result)

    repo_result["application_context"] = application_context

    return repo_result

def get_repo_file_tree(owner: str, repo: str, branch: str):
    tree_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"

    response = httpx.get(tree_url)

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Could not fetch repository file tree")

    tree_data = response.json()

    files = []
    for item in tree_data.get("tree", []):
        if item.get("type") == "blob":
            files.append(item.get("path"))

    return files

def get_file_content(owner: str, repo: str, branch: str, file_path: str):
    file_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{file_path}"

    response = httpx.get(file_url)

    if response.status_code != 200:
        raise HTTPException(
            status_code=404,
            detail=f"Could not fetch file content: {file_path}"
        )

    return response.text