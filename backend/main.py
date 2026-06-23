from fastapi import FastAPI
from pydantic import BaseModel
from urllib.parse import urlparse

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

    return {
        "owner": owner,
        "repo": repo
    }