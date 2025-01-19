#!/usr/bin/env python3

import os
import json
import sys

def create_files_from_json(json_path: str, root_dir: str = "proj"):
    """
    Reads a JSON file containing an array of objects, each with 'id', 'path', and 'code',
    and writes the contents of 'code' to the specified 'path'. All paths will be chrooted
    to root_dir.

    :param json_path: The path to the JSON file.
    :param root_dir: The root directory to chroot to.
    """
    print(f"Creating files from {json_path}")
    # Change to root directory, creating it if needed
    os.makedirs(root_dir, exist_ok=True)
    # Load JSON data
    with open(json_path, 'r', encoding='utf-8') as f:
        code_entries = json.load(f)

    os.chdir(root_dir)
    print(f"Changed to root directory: {os.getcwd()}")

    # debug print number of loaded entries
    print(f"Loaded {len(code_entries)} entries")
    # For each JSON object
    for entry in code_entries:
        file_path = entry["path"]
        # chroot
        if file_path.startswith("/"):
            file_path = file_path[1:]
        # Do not allow upward traversal
        if ".." in file_path:
            print(f"Invalid path: {file_path}")
            continue
        file_code = entry["code"]

        # Create the folder path if needed.
        dir_name = os.path.dirname(file_path)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)

        # Write the code to the file
        with open(file_path, 'w', encoding='utf-8') as file_out:
            file_out.write(file_code)

        print(f"Created file: {file_path}")

def main():
    """
    Main entry point. Expects a single argument that is the path to the JSON file.
    """
    if len(sys.argv) < 2:
        print("Usage: create_files.py <path_to_code_files.json>")
        sys.exit(1)

    json_path = sys.argv[1]
    create_files_from_json(json_path)

if __name__ == "__main__":
    main()
