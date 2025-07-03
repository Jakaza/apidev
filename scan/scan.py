import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Any

# Add current directory and parent to sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, "parser"))

from parser.route_extractor import extract_routes


def is_valid_js_file(file_path: str) -> bool :
    """Check if file is a valid JavaScript file to scan."""
    valid_extensions = [".js"]
    return any(file_path.endswith(ext) for ext in valid_extensions)


def should_ignore_directory(dir_name: str) -> bool:
    """Check if directory should be ignored."""
    ignore_dirs = {
        'node_modules', '__pycache__', '.git', '.next', 'dist', 
        'build', 'coverage', '.nyc_output', 'logs', 'tmp', 'temp'
    }
    return dir_name in ignore_dirs or dir_name.startswith('.')

def scan_project(project_path: str, verbose: bool = False) -> List[Dict[str, Any]]:
    """Scan project for routes and return structured data"""
    routes = []
    scanned_files = 0
    errors = []

    if verbose :
        print(f"Scanning project at: {project_path}", file=sys.stderr)

    project_path = Path(project_path).resolve()

    if not project_path.exists():
        raise FileNotFoundError(f"Project path does not exist: {project_path}")
    
    if not project_path.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {project_path}")
    
    for root, dirs, files in os.walk(project_path):
        # Filter out ignored directories
        dirs[:] = [d for d in dirs if not should_ignore_directory(d)]

        for file in files : 
            if is_valid_js_file(file):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, project_path)

                if verbose:
                    print(f"Reading file: {file_path}", file=sys.stderr)

                try:
                    with open(file_path, "r", encoding="utf-8", errors='ignore') as f:
                        content = f.read()
                        file_routes = extract_routes(content, relative_path)

                        if verbose:
                            print(f"Found {len(file_routes)} route(s) in {file_path}", file=sys.stderr)

                        routes.extend(file_routes)
                        scanned_files += 1

                except:
                    error_msg = f"Error reading {relative_path}: {str(e)}"
                    errors.append(error_msg)
                    if verbose:
                        print(error_msg, file=sys.stderr)

    if verbose:
        print(f"\nScan complete:", file=sys.stderr)
        print(f"  Files scanned: {scanned_files}", file=sys.stderr)
        print(f"  Routes found: {len(routes)}", file=sys.stderr)
        print(f"  Errors: {len(errors)}", file=sys.stderr)

    return routes, {"scanned_files": scanned_files, "errors": errors}












# scan/scan.py

def main(project_path):
    routes = []

    print(f"Scanning project at: {project_path}", file=sys.stderr)

    for root, dirs, files in os.walk(project_path):
        # Ignore node_modules and other unwanted dirs
        dirs[:] = [d for d in dirs if d not in ['node_modules', '__pycache__', '.git']]

        for file in files:
            if file.endswith(".js"):
                file_path = os.path.join(root, file)
                print(f"Reading file: {file_path}", file=sys.stderr)

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        file_routes = extract_routes(content, file_path)

                        # Extracted expected inputs for each route can be called here
                        
                        print(f"Found {len(file_routes)} route(s) in {file_path}", file=sys.stderr)

                        routes.extend(file_routes)
                except Exception as e:
                    print(f"Error reading {file_path}: {str(e)}", file=sys.stderr)

    print(json.dumps(routes, indent=2))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scan.py /path/to/project", file=sys.stderr)
        sys.exit(1)

    project_path = sys.argv[1]
    main(project_path)
