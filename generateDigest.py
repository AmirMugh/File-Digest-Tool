import os
import argparse
import json
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

# Allowed file types
INCLUDE_EXTENSIONS = {".py", ".cpp", ".c", ".h", ".java", ".cs", ".js", ".html", ".css", ".txt"}
EXCLUDE_EXTENSIONS = {".ttf", ".exe", ".dll", ".bin", ".log", ".zip", ".tar", ".rar", ".mp4", ".mp3", ".jpg", ".png"}

def read_file_content(file_path):
    """Reads a file and returns its content as a list of lines."""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.readlines()
    except Exception as e:
        return [f"Error reading file: {e}\n"]

def generate_file_digest(directory, excluded_dirs=None, max_size=None):
    """Recursively reads files in a directory, applying filters and multithreading."""
    files_to_process = []
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not excluded_dirs or d not in excluded_dirs]
        for file in files:
            file_extension = os.path.splitext(file)[1].lower()
            if file_extension in INCLUDE_EXTENSIONS and file_extension not in EXCLUDE_EXTENSIONS:
                file_path = os.path.join(root, file)

                if max_size and os.path.getsize(file_path) > max_size * 1024:
                    continue  # Skip files larger than max_size KB
                
                files_to_process.append(file_path)

    with ThreadPoolExecutor() as executor:
        results = executor.map(read_file_content, files_to_process)

    for file_path, content in tqdm(zip(files_to_process, results), total=len(files_to_process), desc="Processing Files", unit="file"):
        yield "=" * 48 + "\n"
        yield f"File: {file_path}\n"
        yield "=" * 48 + "\n"
        yield from content
        yield "\n"  # Separate files with a blank line

def generate_directory_tree(directory, excluded_dirs=None, prefix=""):
    """Generates a properly formatted directory tree with correct indentation and sorting."""
    output = []
    
    # List all items, sorting directories first, then files (case-insensitive)
    entries = sorted(os.listdir(directory), key=lambda e: (not os.path.isdir(os.path.join(directory, e)), e.lower()))

    # Exclude unwanted directories
    entries = [e for e in entries if not excluded_dirs or e not in excluded_dirs]

    for index, entry in enumerate(entries):
        path = os.path.join(directory, entry)
        is_last = index == len(entries) - 1  # Check if it's the last item in the list

        connector = "└── " if is_last else "├── "
        
        # Determine if it's a directory
        if os.path.isdir(path):
            formatted_entry = f"{entry}/"
        else:
            size = os.path.getsize(path)
            formatted_size = f" ({size / 1024:.1f} KB)" if size < 1024 * 1024 else f" ({size / 1024 / 1024:.1f} MB)"
            formatted_entry = f"{entry}{formatted_size}"

        output.append(f"{prefix}{connector}{formatted_entry}")

        # Recursively process directories
        if os.path.isdir(path):
            new_prefix = prefix + ("    " if is_last else "│   ")
            sub_tree = generate_directory_tree(path, excluded_dirs, new_prefix)
            if sub_tree:  # Prevent blank spots
                output.append(sub_tree)

    return "\n".join(output)

def save_output(output_file, content):
    """Saves content to a file in txt format."""
    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(content)

def main():
    parser = argparse.ArgumentParser(description="Generate a digest of a project directory.")
    parser.add_argument("project_dir", type=str, help="Path to the project directory.")
    parser.add_argument("-o", "--output", type=str, default=None, help="Output directory (default: project root).")
    parser.add_argument("-e", "--exclude", nargs="*", default=[], help="Directories to exclude.")
    parser.add_argument("--max-size", type=int, default=None, help="Maximum file size in KB to include (default: no limit).")

    args = parser.parse_args()
    project_path = os.path.abspath(args.project_dir)
    output_dir = args.output if args.output else project_path
    excluded_dirs = set(args.exclude)
    max_size_kb = args.max_size

    print(f"📂 Scanning project: {project_path}")
    print(f"📤 Output directory: {output_dir}")
    print(f"🚫 Excluded directories: {', '.join(excluded_dirs) if excluded_dirs else 'None'}")
    print(f"📏 Max file size: {max_size_kb} KB" if max_size_kb else "📏 No file size limit")

    # Generate directory structure
    directory_tree = generate_directory_tree(project_path, excluded_dirs)
    
    # Generate file digest
    file_contents = list(generate_file_digest(project_path, excluded_dirs, max_size_kb))

    # Save output in txt format
    output_file = os.path.join(output_dir, "project_summary.txt")
    save_output(output_file, [directory_tree + "\n\n"] + file_contents)

    print(f"✅ Project digest saved to: {output_file}")

if __name__ == "__main__":
    main()
