def build_test_generation_prompt(application_context: dict, test_request: dict):
    prompt = f"""
You are an AI test generation assistant.

Your task is to generate Playwright tests using the structured application context below.

Application Context:
{application_context}

Instructions:
- Generate valid Playwright test code.
- Focus on discovered pages, workflows, and user actions.
- Prefer stable selectors like text, role, and label.
- Use clear test names.
- Return only the Playwright test code.
"""
    return prompt


def create_test_plan(application_context: dict):
    workflows = application_context.get("behavior", {}).get("workflows", [])
    user_actions = application_context.get("behavior", {}).get("user_actions", [])

    test_plan = []

    for workflow in workflows:
        test_plan.append({
            "name": workflow.get("name"),
            "type": workflow.get("test_type", "workflow"),
            "source": "workflow",
            "details": workflow
        })

    for action in user_actions:
        test_plan.append({
            "name": f"Test user action: {action.get('label')}",
            "type": action.get("type", "interaction"),
            "source": "user_action",
            "details": action
        })

    return test_plan



def build_prompt_context(application_context: dict, test_request: dict):
    return {
        "application": application_context.get("application", {}),
        "structure": {
            "pages": application_context.get("structure", {}).get("pages", []),
            "ui_files": application_context.get("structure", {}).get("ui_files", []),
        },
        "current_test": test_request,
        "relevant_behavior": {
            "workflows": application_context.get("behavior", {}).get("workflows", []),
            "user_actions": application_context.get("behavior", {}).get("user_actions", []),
        },
    }



def build_test_generation_prompt(application_context: dict, test_request: dict):
    prompt_context = build_prompt_context(application_context, test_request)

    prompt = f"""
You are an AI assistant that generates Playwright tests.

Generate one Playwright test for the current test request.

Focused Context:
{prompt_context}

Requirements:
- Use Playwright with TypeScript.
- Focus only on the current test request.
- Use stable selectors like role, text, and label.
- Include clear test names.
- Return only executable Playwright test code.
"""
    return prompt