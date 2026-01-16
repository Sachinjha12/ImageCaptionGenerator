import os
import json

def folder_to_json(root_path):
    file_structure = {}

    if not os.path.exists(root_path):
        return None

    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            if filename.endswith('.py'):
                full_path = os.path.join(dirpath, filename)
                
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                       
                        file_content = f.read().splitlines()

                   
                    rel_path = os.path.relpath(dirpath, os.path.dirname(os.path.abspath(root_path)))
                    path_parts = rel_path.split(os.sep)

                    current_level = file_structure
                    for part in path_parts:
                        if part not in current_level:
                            current_level[part] = {}
                        current_level = current_level[part]

                  
                    current_level[filename] = file_content

                except Exception as e:
                    print(f"Error reading {full_path}: {e}")

    return json.dumps(file_structure, indent=4)


target_directory = r"tests"  
output_filename = "output.json"

print(f"Scanning directory: {target_directory}...")
json_output = folder_to_json(target_directory)

if json_output:
    with open(output_filename, 'w', encoding='utf-8') as outfile:
        outfile.write(json_output)
    
    # Printing the validation(SUCCESS/FAILURE)
    print(f"SUCCESS: JSON generated at {os.path.abspath(output_filename)}")
else:
    print(f"ERROR: Directory '{target_directory}' not found.")