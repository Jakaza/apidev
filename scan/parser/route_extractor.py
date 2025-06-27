import re
import sys

# parser/route_extractor.py

def extract_routes(js_code, file_path=None):
    routes = []

    pattern = re.compile(r'\b(app|router)\.(get|post|put|delete|patch)\s*\(\s*[\'"](.+?)[\'"]', re.IGNORECASE)

    matches = pattern.findall(js_code)
    print(f"[{file_path}] Matched {len(matches)} route expressions", file=sys.stderr)

    for obj , method, path in matches:
        print(f" Jakaza - >{method.upper()} {path} ({obj})", file=sys.stderr)
        routes.append({
            "method": method.upper(),
            "path": path,
            "file": file_path
        })

    return routes

"""""
    The method extract_expected_inputs takes a JavaScript code block as input and returns a dictionary of expected inputs for each route.
    E.G. 
    {'req.body': ['title', 'description']}
    {'req.params': ['id', 'title']}
    {'req.query': ['page', 'limit']}

    To be implemented
"""""

def extract_expected_inputs(js_code_block):
    pass