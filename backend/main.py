from fastapi import FastAPI
from pydantic import BaseModel

from github_service import get_repo_metadata

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
    return get_repo_metadata(request.repo_url)