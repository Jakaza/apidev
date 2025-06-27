import os
import sys
import json
from parser.route_extractor import extract_routes , extract_expected_inputs

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
