from convert import *
def search_file(pattern, directory):
    return glob.glob(f"{directory}/PalWorldSave/**/{pattern}", recursive=True)
def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ["sav", "json"]: print("Usage: script.py <sav|json>"); exit(1)
    level_files = search_file("Level.json", ".") if sys.argv[1] == "sav" else search_file("Level.sav", ".")
    if not level_files: print("File not found."); exit(1)
    for level_file in level_files:
        if sys.argv[1] == "sav":
            output_path = level_file.replace(".json", ".sav")
            convert_json_to_sav(level_file, output_path)
        else:
            output_path = level_file.replace(".sav", ".json")
            convert_sav_to_json(level_file, output_path)
        print(f"Converted {level_file} to {output_path}")
if __name__ == "__main__": main()