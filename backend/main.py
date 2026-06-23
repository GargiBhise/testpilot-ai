from fastapi import FastAPI
from pydantic import BaseModel
from urllib.parse import urlparse
import httpx
from fastapi import HTTPException

app = FastAPI(title="TestPilot AI", version="0.1.0")


class RepoRequest(BaseModel):
    repo_url: str


@app.get("/")
def root():
    return {"message": "TestPilot AI Backend Running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/analyze-repo")
def analyze_repo(request: RepoRequest):
    parsed_url = urlparse(request.repo_url)

    path_parts = parsed_url.path.strip("/").split("/")

    owner = path_parts[0]
    repo = path_parts[1]

    github_api_url = f"https://api.github.com/repos/{owner}/{repo}"

    response = httpx.get(github_api_url)

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="GitHub repository not found")

    repo_data = response.json()

    return {
    "owner": owner,
    "repo": repo,
    "full_name": repo_data["full_name"],
    "description": repo_data["description"],
    "default_branch": repo_data["default_branch"],
    "language": repo_data["language"],
    "stars": repo_data["stargazers_count"],
    "github_url": repo_data["html_url"]
}

