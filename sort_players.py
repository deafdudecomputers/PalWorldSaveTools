import re, os, sys, argparse
from datetime import datetime, timedelta
def extract_last_online(data):
    match = re.search(r'Last Online: ([\d\- :]+)', data)
    if match:
        date_str = match.group(1)
        try:
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            clean_date_str = re.sub(r'[\(\[].*?[\)\]]', '', date_str)
            return datetime.strptime(clean_date_str.strip(), "%Y-%m-%d %H:%M:%S")
    return None
def extract_level(data):
    match = re.search(r'Level: (\d+)', data)
    if match:
        return int(match.group(1))
    return None
def extract_pals_count(data):
    match = re.search(r'Owned: (\d+)', data)
    if match:
        return int(match.group(1))
    return None
def filter_players_by_days_and_level(players, days, level):
    current_time = datetime.now()
    filtered_players = []
    for player in players:
        last_online = extract_last_online(player)
        player_level = extract_level(player)
        pals_count = extract_pals_count(player)
        if last_online and player_level is not None and pals_count is not None:
            if (current_time - last_online) >= timedelta(days=days) and player_level <= level:
                filtered_players.append((player, pals_count))
    return filtered_players
def delete_player_saves(player_data):
    players_folder = "Players"
    if not os.path.exists(players_folder):
        print(f"Players folder '{players_folder}' not found.")
        return 0, 0
    total_pals_to_delete = sum(pals_count for _, pals_count in player_data)
    deleted_count = 0
    for player, _ in player_data:
        match = re.search(r'UID: ([\w-]+)', player)
        if match:
            uid = match.group(1).replace('-', '')
            sav_filename = f"{uid}.sav"
            sav_file_paths = [os.path.join(players_folder, f) for f in os.listdir(players_folder) if f.lower() == sav_filename.lower()]
            if sav_file_paths:
                sav_file_path = sav_file_paths[0]
                os.remove(sav_file_path)
                deleted_count += 1
                print(f"Deleted: {sav_file_path}")
                print(f"Deleted Player Info: {player}")
    if deleted_count == 0:
        print(f"No PlayerUID.sav files found for deletion, skipping...")
    else:
        print(f"Total number of pals deleted: {total_pals_to_delete}")
    return deleted_count, total_pals_to_delete
def main(file_path, days, level):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            player_data = file.readlines()
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        sys.exit(1)
    player_data = [line.strip() for line in player_data if line.strip()]
    filtered_players = filter_players_by_days_and_level(player_data, days, level)
    sorted_players = sorted(filtered_players, key=lambda x: extract_last_online(x[0]) or datetime.min)
    total_pals_deleted = sum(pals_count for _, pals_count in sorted_players)
    delete_count, _ = delete_player_saves(sorted_players)
    print(f"Total Players: {len(player_data)}")
    print(f"Total Players Deleted: {len(sorted_players)}")
    print(f"Total Pals Count of Deleted Players: {total_pals_deleted}")
    print(f"Total Players Kept: {len(player_data) - len(sorted_players)}")
    print(f"Filtered by: Days since last online >= {days}, Level <= {level}")
    print(f"Deleted {delete_count} PlayerUID.sav files.")
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sort, filter, and delete players by days since last online and level.")
    parser.add_argument("file", help="Path to the file containing player data")
    parser.add_argument("days", type=int, help="Minimum number of days since last online to include")
    parser.add_argument("level", type=int, help="Maximum level to include")
    args = parser.parse_args()
    main(args.file, args.days, args.level)