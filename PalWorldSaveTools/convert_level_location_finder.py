from convert import *
import glob
def search_file(pattern, directory):
    return glob.glob(f"{directory}/**/{pattern}", recursive=True)
def main():
    convertion_type = sys.argv[1]
    if convertion_type == "sav":
        level_files = search_file("Level.json", ".")
    elif convertion_type == "json":
        level_files = search_file("Level.sav", ".")
    else:
        print("Invalid conversion type. Use 'sav' or 'json'.")
        exit(1)
    if not level_files:
        print("File not found.")
        exit(1)
    for level_file in level_files:
        if convertion_type == "sav":
            level_sav_output_path = level_file.replace(".json", ".sav")
            convert_json_to_sav(level_file, level_sav_output_path)
            print(f"Converted {level_file} to {level_sav_output_path}")
        elif convertion_type == "json":
            level_json_output_path = level_file.replace(".sav", ".json")
            convert_sav_to_json(level_file, level_json_output_path)
            print(f"Converted {level_file} to {level_json_output_path}")
if __name__ == "__main__":
    main()