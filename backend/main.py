from fastapi import FastAPI
from pydantic import BaseModel
from prompt_engine import create_test_plan, build_test_generation_prompt
from llm_service import generate_test_from_prompt

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


@app.post("/generate-test")
def generate_test(request: RepoRequest):
    repo_result = get_repo_metadata(request.repo_url)
    application_context = repo_result["application_context"]

    test_plan = create_test_plan(application_context)

    if not test_plan:
        return {
            "status": "no_tests_planned",
            "message": "No workflows or user actions found to generate tests."
        }

    first_test_request = test_plan[0]
    prompt = build_test_generation_prompt(application_context, first_test_request)
    generated_test = generate_test_from_prompt(prompt)

    return {
        "status": "completed",
        "test_request": first_test_request,
        "generated_test": generated_test
    }