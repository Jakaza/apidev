import re
import sys
from typing import List, Dict, Any, Set

# parser/route_extractor.py

def extract_routes(js_code, file_path=None) -> List[Dict[str, Any]]:
    """Extract routes from JavaScript code with enhanced pattern matching"""
    routes = []

        # Enhanced patterns for different route declaration styles
    patterns = [
        # Express.js style: app.get('/path', handler)
        r'\b(app|router)\.(get|post|put|delete|patch|head|options|all)\s*\(\s*[\'"`]([^\'"`]+)[\'"`]',
        # Method chaining: .route('/path').get(handler).post(handler)
        r'\.route\s*\(\s*[\'"`]([^\'"`]+)[\'"`]\s*\)\s*\.(get|post|put|delete|patch|head|options|all)',    
    ]

    for i, pattern in enumerate(patterns):
        regex = re.compile(pattern, re.IGNORECASE | re.MULTILINE)
        matches = regex.findall(js_code)

        for match in matches:
            if i == 3:
                path, method = match
                obj = 'router'
            else:
                obj, method, path = match

            # Extract expected inputs for this route
            expected_inputs = extract_expected_inputs_for_route(js_code, method.upper(), path)

            route_info = {
                    "method": method.upper(),
                    "path": path,
                    "file": file_path,
                    "framework": obj,
                    "expected_inputs": expected_inputs
                }
            routes.append(route_info)
            total_matches += 1

    if file_path and total_matches > 0:
        print(f"[{file_path}] Found {total_matches} routes", file=sys.stderr)
        for route in routes[-total_matches:]:  # Show only the routes just added
            print(f"  -> {route['method']} {route['path']} ({route['framework']})", file=sys.stderr)
    
    return routes





# def extract_routes(js_code, file_path=None):
#     routes = []

#     pattern = re.compile(r'\b(app|router)\.(get|post|put|delete|patch)\s*\(\s*[\'"](.+?)[\'"]', re.IGNORECASE)

#     matches = pattern.findall(js_code)
#     print(f"[{file_path}] Matched {len(matches)} route expressions", file=sys.stderr)

#     for obj , method, path in matches:
#         print(f" Jakaza - >{method.upper()} {path} ({obj})", file=sys.stderr)
#         routes.append({
#             "method": method.upper(),
#             "path": path,
#             "file": file_path
#         })

#     return routes

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