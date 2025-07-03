#!/usr/bin/env python3
"""
Debug version of the scanner to help identify issues
"""

import os
import sys
import json
import traceback
from pathlib import Path

def debug_imports():
    """Debug import issues"""
    print("=== DEBUG: Testing imports ===", file=sys.stderr)
    
    # Check current directory
    current_dir = os.getcwd()
    print(f"Current directory: {current_dir}", file=sys.stderr)
    
    # Check if route_extractor.py exists
    route_extractor_path = os.path.join(current_dir, 'route_extractor.py')
    print(f"Looking for route_extractor.py at: {route_extractor_path}", file=sys.stderr)
    print(f"Exists: {os.path.exists(route_extractor_path)}", file=sys.stderr)
    
    # Try different import paths
    possible_paths = [
        '.',
        'parser',
        'scan',
        os.path.join('scan', 'parser')
    ]
    
    for path in possible_paths:
        full_path = os.path.join(current_dir, path, 'route_extractor.py')
        print(f"Checking: {full_path} -> {os.path.exists(full_path)}", file=sys.stderr)
    
    # Check sys.path
    print(f"sys.path: {sys.path}", file=sys.stderr)
    
    # Try importing
    try:
        from route_extractor import extract_routes
        print("✅ Successfully imported from route_extractor", file=sys.stderr)
        return extract_routes
    except ImportError as error:
        print(f"❌ Failed to import route_extractor: {error}", file=sys.stderr)
        
        # Try alternative imports
        try:
            sys.path.insert(0, os.path.join(current_dir, 'parser'))
            from route_extractor import extract_routes
            print("✅ Successfully imported from parser/route_extractor", file=sys.stderr)
            return extract_routes
        except ImportError as error2:
            print(f"❌ Failed to import from parser: {error2}", file=sys.stderr)
            return None

def simple_extract_routes(js_code, file_path=None):
    """Simple fallback route extractor"""
    import re
    routes = []
    
    # Basic Express.js pattern
    pattern = re.compile(r'\b(app|router)\.(get|post|put|delete|patch)\s*\(\s*[\'"](.+?)[\'"]', re.IGNORECASE)
    matches = pattern.findall(js_code)
    
    for obj, method, path in matches:
        routes.append({
            "method": method.upper(),
            "path": path,
            "file": file_path,
            "framework": obj
        })
    
    return routes

def scan_project_debug(project_path):
    """Debug version of scan_project"""
    print(f"=== DEBUG: Scanning {project_path} ===", file=sys.stderr)
    
    # Test imports first
    extract_routes = debug_imports()
    if extract_routes is None:
        print("Using fallback route extractor", file=sys.stderr)
        extract_routes = simple_extract_routes
    
    routes = []
    scanned_files = 0
    
    project_path = Path(project_path).resolve()
    print(f"Resolved project path: {project_path}", file=sys.stderr)
    
    if not project_path.exists():
        raise FileNotFoundError(f"Project path does not exist: {project_path}")
    
    if not project_path.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {project_path}")
    
    # List all files first
    print("=== FILES FOUND ===", file=sys.stderr)
    for root, dirs, files in os.walk(project_path):
        # Skip node_modules and hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
        
        for file in files:
            if file.endswith('.js'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, project_path)
                print(f"Found JS file: {relative_path}", file=sys.stderr)
                
                try:
                    with open(file_path, "r", encoding="utf-8", errors='ignore') as f:
                        content = f.read()
                        print(f"Read {len(content)} characters from {relative_path}", file=sys.stderr)
                        
                        file_routes = extract_routes(content, relative_path)
                        print(f"Extracted {len(file_routes)} routes from {relative_path}", file=sys.stderr)
                        
                        routes.extend(file_routes)
                        scanned_files += 1
                        
                except Exception as error:
                    print(f"Error reading {relative_path}: {error}", file=sys.stderr)
                    traceback.print_exc(file=sys.stderr)
    
    print(f"=== SCAN COMPLETE ===", file=sys.stderr)
    print(f"Files scanned: {scanned_files}", file=sys.stderr)
    print(f"Routes found: {len(routes)}", file=sys.stderr)
    
    return routes

def main():
    try:
        if len(sys.argv) < 2:
            print("Usage: python debug_scan.py <project_path>", file=sys.stderr)
            sys.exit(1)
        
        project_path = sys.argv[1]
        routes = scan_project_debug(project_path)
        
        # Output results
        result = {"routes": routes}
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except Exception as error:
        print(f"Unexpected error: {error}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()