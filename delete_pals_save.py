import re, os , sys
def extract_player_info(line):
    match = re.search(r'Player: (.+?) \| UID: ([\w-]+) \| .*?Owned: (\d+)', line)
    if match:
        player_name = match.group(1)
        player_uid = match.group(2)
        pals_found = int(match.group(3))
        return player_name, player_uid, pals_found
    return None, None, None
def find_player_uids_with_max_pals(log_file, max_pals):
    try:
        with open(log_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"File '{log_file}' not found.")
        return []
    player_info = []
    for line in lines:
        player_name, player_uid, pals_found = extract_player_info(line)
        if player_uid and pals_found <= max_pals:
            player_info.append((line.strip(), player_uid, pals_found))
    return player_info
def delete_player_saves(player_info):
    players_folder = "Players"
    if not os.path.exists(players_folder):
        print(f"Players folder '{players_folder}' not found.")
        return
    total_pals_to_delete = sum(pals_found for _, _, pals_found in player_info)
    deleted_count = 0
    for line, uid, _ in player_info:
        uid_no_hyphens = uid.replace('-', '')
        sav_filename = f"{uid_no_hyphens}.sav"
        sav_file_paths = [os.path.join(players_folder, f) for f in os.listdir(players_folder) if f.lower() == sav_filename.lower()]
        if sav_file_paths:
            sav_file_path = sav_file_paths[0]
            os.remove(sav_file_path)
            deleted_count += 1
            print(f"Deleted: {sav_file_path}")
            print(f"Deleted Player Info: {line}")
    if deleted_count == 0:
        print(f"No PlayerUID.sav files found for deletion, skipping...")
    else:
        print(f"Total number of pals deleted: {total_pals_to_delete}")
        print(f"Deleted {deleted_count} PlayerUID.sav files.")
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python delete_pals_save.py <log_file> <max_pals>")
        sys.exit(1)
    log_file = sys.argv[1]
    max_pals = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    player_info = find_player_uids_with_max_pals(log_file, max_pals)
    if player_info:
        delete_player_saves(player_info)
        print(f"Filter used: {max_pals} or fewer pals")
    else:
        print(f"No PlayerUIDs with {max_pals} or fewer pals found in {log_file}.")
    input("Press enter to exit...")