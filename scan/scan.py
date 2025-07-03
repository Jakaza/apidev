import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any

# Add current directory and parent to sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, "parser"))

from parser.route_extractor import extract_routes


def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


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


def output_results(routes: List[Dict[str, Any]], output_format: str = "json", 
                  output_file: str = None, include_stats: bool = False, 
                  stats: Dict[str, Any] = None):
        """Output results in specified format"""
        if output_format == "json":
            result = {"routes": routes}
            if include_stats and stats:
                result["stats"] = stats
            
            output = json.dumps(result, indent=2, ensure_ascii=False)

        if output_file:
                try:
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(output)
                    print(f"Results written to: {output_file}", file=sys.stderr)
                except Exception as e:
                    print(f"Error writing to file {output_file}: {e}", file=sys.stderr)
                    print(output)
        else:
                print(output)

def main():
    parser = argparse.ArgumentParser(
        description="Scan JavaScript/TypeScript projects for API routes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scan.py /path/to/project
  python scan.py /path/to/project --format table
  python scan.py /path/to/project --output routes.json --stats
  python scan.py /path/to/project --verbose --format summary
        """
    )
    
    parser.add_argument('project_path', help='Path to the project directory')
    parser.add_argument('-v', '--verbose', action='store_true', 
                       help='Enable verbose output')
    parser.add_argument('-f', '--format', choices=['json', 'table', 'summary'], 
                       default='json', help='Output format (default: json)')
    parser.add_argument('-o', '--output', help='Output file (default: stdout)')
    parser.add_argument('-s', '--stats', action='store_true', 
                       help='Include scan statistics in output')
    
    args = parser.parse_args()
    
    try:
        routes, stats = scan_project(args.project_path, args.verbose)
        output_results(routes, args.format, args.output, args.stats, stats)
        
    except (FileNotFoundError, NotADirectoryError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nScan interrupted by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
