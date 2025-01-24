from convert import *
def search_for_players_folders(search_name, root_path): return [os.path.join(root, dir_name) for root, dirs, _ in os.walk(root_path) for dir_name in dirs if dir_name == search_name]
def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ["sav", "json"]: print("Usage: script.py <sav|json>"); exit(1)
    players_folders = search_for_players_folders("Players", ".")
    if not players_folders: print("Players folder not found."); exit(1)
    for folder in players_folders:
        for root, _, files in os.walk(folder):
            if not files: print("Players folder empty."); continue
            for file in files:
                path = os.path.join(root, file)
                if sys.argv[1] == "sav" and file.endswith(".json"): 
                    output_path = path.replace(".json", ".sav")
                    convert_json_to_sav(path, output_path)
                elif sys.argv[1] == "json" and file.endswith(".sav"): 
                    output_path = path.replace(".sav", ".json")
                    convert_sav_to_json(path, output_path)
if __name__ == "__main__": main()