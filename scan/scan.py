import os
import sys
import json
from parser.route_extractor import extract_routes

def main(project_path):
    routes = []

    for root, dirs, files in os.walk(project_path):
        for file in files : 
            if file.endswith(".js"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding="utf-0") as f:
                        content = f.read()
                        file_routes = extract_routes(content, file_path)
                        routes.extend(file_routes)
                except Exception as e:
                    print(f"Error reading {file_path}: {str(e)}", file=sys.stderr)

        print(json.dumps(routes, indent=2))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scan.py /path/to/project", file=sys.stderr)
        sys.exit(1)

    project_path = sys.argv[1]
    main(project_path=project_path)

