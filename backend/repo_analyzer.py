import re


def detect_framework(files: list[str]):
    file_set = set(files)

    if "angular.json" in file_set:
        return {"framework": "Angular", "language": "TypeScript", "test_strategy": "playwright"}

    if "next.config.js" in file_set or "next.config.ts" in file_set:
        return {"framework": "Next.js", "language": "TypeScript/JavaScript", "test_strategy": "playwright"}

    if "package.json" in file_set and any(
        path.startswith("src/") or "/src/" in path for path in files
    ):
        return {"framework": "React", "language": "JavaScript/TypeScript", "test_strategy": "playwright"}

    if "pom.xml" in file_set or "build.gradle" in file_set:
        return {"framework": "Spring Boot / Java", "language": "Java", "test_strategy": "api"}

    if "manage.py" in file_set:
        return {"framework": "Django", "language": "Python", "test_strategy": "api"}

    if "requirements.txt" in file_set and any("main.py" in path for path in files):
        return {"framework": "FastAPI / Python", "language": "Python", "test_strategy": "api"}

    return {"framework": "Unknown", "language": "Unknown", "test_strategy": "manual-review"}

def discover_pages(files: list[str]):
    pages = []

    for file in files:
        filename = file.split("/")[-1]

        if filename.endswith((".js", ".jsx", ".tsx", ".ts")):
            if filename not in ["App.js", "index.js"]:
                page_name = filename.split(".")[0]
                pages.append(page_name)

    return list(set(pages))


def get_ui_files(files: list[str]):
    ui_files = []

    for file in files:
        if file.endswith((".js", ".jsx", ".ts", ".tsx")):
            if any(folder in file for folder in ["src/", "components/", "pages/", "app/"]):
                if not file.endswith((".test.js", ".test.jsx", ".test.ts", ".test.tsx")):
                    ui_files.append(file)

    return ui_files[:10]



def discover_workflows(pages: list[str]):
    workflows = []

    if "Home" in pages:
        for page in pages:
            if page != "Home":
                workflows.append({
                    "name": f"Navigate from Home to {page}",
                    "start_page": "Home",
                    "target_page": page,
                    "test_type": "navigation"
                })

    return workflows



def extract_ui_elements(file_path: str, content: str):
    elements = {
        "file": file_path,
        "buttons": [],
        "links": [],
        "forms": [],
        "inputs": []
    }

    button_matches = re.findall(r"<button[^>]*>(.*?)</button>", content, re.DOTALL)
    for button in button_matches:
        clean_text = re.sub(r"<[^>]+>", "", button).strip()
        if clean_text:
            elements["buttons"].append(clean_text)

    link_matches = re.findall(r"<Link[^>]*to=[\"']([^\"']+)[\"']", content)
    elements["links"].extend(link_matches)

    if "<form" in content:
        elements["forms"].append("form_detected")

    input_matches = re.findall(r"<input[^>]*placeholder=[\"']([^\"']+)[\"']", content)
    elements["inputs"].extend(input_matches)

    return elements



def extract_user_actions(file_path: str, content: str):
    actions = []

    button_matches = re.findall(
        r"<button[^>]*(?:onClick=\{([^}]+)\})?[^>]*>(.*?)</button>",
        content,
        re.DOTALL
    )

    for handler, label in button_matches:
        clean_label = re.sub(r"<[^>]+>", "", label).strip()

        if clean_label:
            actions.append({
                "file": file_path,
                "type": "button",
                "label": clean_label,
                "handler": handler.strip() if handler else None
            })

    link_matches = re.findall(
        r"<Link[^>]*to=[\"']([^\"']+)[\"'][^>]*>(.*?)</Link>",
        content,
        re.DOTALL
    )

    for target, label in link_matches:
        clean_label = re.sub(r"<[^>]+>", "", label).strip()

        actions.append({
            "file": file_path,
            "type": "navigation",
            "label": clean_label if clean_label else f"Navigate to {target}",
            "target": target
        })

    return actions