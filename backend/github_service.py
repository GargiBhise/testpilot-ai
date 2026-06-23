from urllib.parse import urlparse

import httpx
from fastapi import HTTPException


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
    

    return {
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
}



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