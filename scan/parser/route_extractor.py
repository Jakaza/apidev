import re
import sys

def extract_routes(js_code, file_path=None):
    routes = []

    pattern = re.compile(r'\b(app|router)\.(get|post|put|delete|patch)\s*\(\s*[\'"](.+?)[\'"]', re.IGNORECASE)

    matches = pattern.findall(js_code)
    print(f"[{file_path}] Matched {len(matches)} route expressions", file=sys.stderr)

    for obj, method, path in matches:
        print(f"{method.upper()} {path} ({obj})", file=sys.stderr)
        routes.append({
            "method": method.upper(),
            "path": path,
            "file": file_path
        })

    return routes
