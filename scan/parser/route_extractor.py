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


def extract_expected_inputs_for_route(js_code: str, method: str, path: str) -> Dict[str, List[str]]:
    """Extract expected inputs for a specific route by analyzing the handler function"""
    expected_inputs = {
        'req.body': [],
        'req.params': [],
        'req.query': [],
        'req.headers': []
    }
    # Try to find the handler function for this specific route
    # Simplified approach - NB ( need more sophisticated parsing )
    route_handler_patterns = [
        rf'{re.escape(path)}[\'"`]\s*,\s*(?:async\s+)?\(?(?:req|request|ctx)[^{{]*{{([^}}]+)}}',
        rf'{method.lower()}\s*\(\s*[\'"`]{re.escape(path)}[\'"`]\s*,\s*(?:async\s+)?\(?(?:req|request|ctx)[^{{]*{{([^}}]+)}}'
    ]

    handler_code = ''

    for pattern in route_handler_patterns:
        matches = re.search(pattern, js_code, re.IGNORECASE | re.DOTALL)

        if matches:
            handler_code = matches.group(1)
            break

    if not handler_code:
    # Fallback: analyze the entire file for common patterns
        handler_code = js_code

    # Extract req.body usage
    body_patterns = [
        r'req\.body\.(\w+)',
        r'request\.body\.(\w+)',
        r'ctx\.request\.body\.(\w+)',
        r'body\.(\w+)',
        r'const\s*{\s*([^}]+)\s*}\s*=\s*req\.body',
        r'const\s*{\s*([^}]+)\s*}\s*=\s*request\.body'
    ]

    for pattern in body_patterns:
        matches = re.findall(pattern, handler_code)
        for match in matches:
            if isinstance(match, tuple):
                match = match[0]
            if ',' in match:
                # Destructuring: {title, description} = req.body
                fields = [field.strip() for field in match.split(',')]
                expected_inputs['req.body'].extend(fields)
            else:
                expected_inputs['req.body'].append(match)

    # Extract req.params usage
    param_patterns = [
        r'req\.params\.(\w+)',
        r'request\.params\.(\w+)',
        r'ctx\.params\.(\w+)',
        r'params\.(\w+)'
    ]

    for pattern in param_patterns:
        matches = re.findall(pattern, handler_code)
        expected_inputs['req.params'].extend(matches)
    
    # Extract path parameters from the route path itself
    path_params = re.findall(r':(\w+)', path)
    expected_inputs['req.params'].extend(path_params)

    # Extract req.query usage
    query_patterns = [
        r'req\.query\.(\w+)',
        r'request\.query\.(\w+)',
        r'ctx\.query\.(\w+)',
        r'query\.(\w+)'
    ]
    
    for pattern in query_patterns:
        matches = re.findall(pattern, handler_code)
        expected_inputs['req.query'].extend(matches)

    # Extract req.headers usage
    header_patterns = [
        r'req\.headers\.(\w+)',
        r'req\.headers\[[\'"`]([^\'"`]+)[\'"`]\]',
        r'request\.headers\.(\w+)',
        r'ctx\.headers\.(\w+)'
    ]
    
    for pattern in header_patterns:
        matches = re.findall(pattern, handler_code)
        expected_inputs['req.headers'].extend(matches)


    # Remove duplicates and clean up
    for key in expected_inputs:
        expected_inputs[key] = list(set(expected_inputs[key]))
        expected_inputs[key] = [item.strip() for item in expected_inputs[key] if item.strip()]

    # Remove empty categories
    expected_inputs = {k: v for k, v in expected_inputs.items() if v}
    
    return expected_inputs



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