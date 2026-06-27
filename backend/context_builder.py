def build_application_context(repo_data: dict):
    return {
        "repository": {
            "name": repo_data["full_name"],
            "url": repo_data["github_url"],
            "default_branch": repo_data["default_branch"],
            "file_count": repo_data["file_count"],
        },
        "application": {
            "framework": repo_data["analysis"]["framework"],
            "language": repo_data["analysis"]["language"],
            "test_strategy": repo_data["analysis"]["test_strategy"],
        },
        "structure": {
            "pages": repo_data["pages"],
            "ui_files": repo_data["ui_files"],
        },
        "behavior": {
            "workflows": repo_data["workflows"],
            "user_actions": repo_data.get("user_actions", []),
        },
    }