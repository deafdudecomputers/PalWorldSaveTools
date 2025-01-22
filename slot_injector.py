import json, sys, glob
from convert import convert_json_to_sav, convert_sav_to_json
def search_file(pattern, directory): return glob.glob(f"{directory}/**/{pattern}", recursive=True)
def edit_json(file_path, pages, slots):
    with open(file_path, 'r') as file: data = json.load(file)
    value_to_replace, new_value, count_found, count_replaced = 960, pages * slots, 0, 0
    def replace_values(obj):
        nonlocal count_found, count_replaced
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == "value" and value == value_to_replace: count_found += 1; obj[key] = new_value; count_replaced += 1
                else: replace_values(value)
        elif isinstance(obj, list): [replace_values(item) for item in obj]
    replace_values(data)
    with open(file_path, 'w') as file: json.dump(data, file, indent=4)
    return count_found, count_replaced
def get_user_input():
    while True:
        try:
            pages, slots = int(input("Enter the number of pages: ")), int(input("Enter the number of slots: "))
            total = pages * slots; print(f"The total is {total}.")
            if input("Is this correct? (yes/no): ").strip().lower() == 'yes': return pages, slots
            else: print("Let's try again.")
        except ValueError: print("Invalid input. Please enter numeric values.")
def main():
    level_files = search_file("Level.sav", ".")
    if not level_files: print("No .sav file found."); sys.exit(1)
    for level_file in level_files:
        level_json_output_path = level_file.replace(".sav", ".json")
        convert_sav_to_json(level_file, level_json_output_path)
        print(f"Converted {level_file} to {level_json_output_path}")
        pages, slots = get_user_input()
        print(f"Now loading json and making edits... please be patient.")
        found, replaced = edit_json(level_json_output_path, pages, slots)
        print(f"Found 'value': 960, {found} times."); print(f"Replaced with {pages * slots}, {replaced} times.")
        level_sav_output_path = level_json_output_path.replace(".json", ".sav")
        convert_json_to_sav(level_json_output_path, level_sav_output_path)
        print(f"Converted {level_json_output_path} back to {level_sav_output_path}")
    print("Process completed.")
if __name__ == "__main__": main()