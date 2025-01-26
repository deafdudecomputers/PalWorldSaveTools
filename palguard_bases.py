from internal_libs.import_libs import *
from datetime import datetime, timedelta
def parse_log(inactivity_days=None, max_level=None):
    log_file = "scan_save.log"
    if not os.path.exists(log_file): return print(f"Log file '{log_file}' not found in the current directory.")
    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f: content = f.read()
    guilds, threshold_time, inactive_guilds, kill_commands = content.split("\n\n"), None, {}, []
    guild_count = base_count = 0
    if inactivity_days: threshold_time = datetime.now() - timedelta(days=inactivity_days)
    for guild in guilds:
        players_data = re.findall(r"Player: (.+?) \| UID: ([a-f0-9-]+) \| Level: (\d+) \| Caught: (\d+) \| Owned: (\d+) \| Encounters: (\d+) \| Uniques: (\d+) \| Last Online: (.+? \(\d+d:\d+h:\d+m:\d+s ago\))", guild)
        bases = re.findall(r"Base \d+: Base ID: ([a-f0-9-]+) \| Old: .+? \| New: .+? \| RawData: (.+)", guild)
        if not players_data or not bases: continue
        player_last_online = [player_time for _, _, _, _, _, _, _, player_time in players_data if re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", player_time)]
        player_levels = [level for _, _, level, _, _, _, _, _ in players_data]
        guild_name = re.search(r"Guild: (.+?) \|", guild)
        guild_leader = re.search(r"Guild Leader: (.+?) \|", guild)
        guild_id = re.search(r"Guild ID: ([a-f0-9-]+)", guild)
        guild_name = guild_name.group(1) if guild_name else "Unnamed Guild"
        guild_leader = guild_leader.group(1) if guild_leader else "Unknown"
        guild_id = guild_id.group(1) if guild_id else "Unknown"
        if inactivity_days and max_level:
            if all(last_online <= str(threshold_time) for last_online in player_last_online) and all(int(level) <= max_level for level in player_levels):
                if guild_id not in inactive_guilds:
                    inactive_guilds[guild_id] = {
                        "guild_name": guild_name,
                        "guild_leader": guild_leader,
                        "players": [],
                        "bases": []
                    }
                for player in players_data:
                    last_online_time = player[7]
                    inactive_guilds[guild_id]["players"].append({
                        "name": player[0],
                        "uid": player[1],
                        "level": player[2],
                        "caught": player[3],
                        "owned": player[4],
                        "encounters": player[5],
                        "uniques": player[6],
                        "last_online": f"{player[7]}"
                    })
                inactive_guilds[guild_id]["bases"].extend(bases)
                guild_count += 1
                base_count += len(bases)
                kill_commands.extend([f"killnearestbase {raw_data.replace(',', '')}" for _, raw_data in bases])
        elif inactivity_days and all(last_online <= str(threshold_time) for last_online in player_last_online):
            if guild_id not in inactive_guilds:
                inactive_guilds[guild_id] = {
                    "guild_name": guild_name,
                    "guild_leader": guild_leader,
                    "players": [],
                    "bases": []
                }
            for player in players_data:
                last_online_time = player[7]
                inactive_guilds[guild_id]["players"].append({
                        "name": player[0],
                        "uid": player[1],
                        "level": player[2],
                        "caught": player[3],
                        "owned": player[4],
                        "encounters": player[5],
                        "uniques": player[6],
                        "last_online": f"{player[7]}"
                    })
            inactive_guilds[guild_id]["bases"].extend(bases)
            guild_count += 1
            base_count += len(bases)
            kill_commands.extend([f"killnearestbase {raw_data.replace(',', '')}" for _, raw_data in bases])
        elif max_level and all(int(level) <= max_level for level in player_levels):
            if guild_id not in inactive_guilds:
                inactive_guilds[guild_id] = {
                    "guild_name": guild_name,
                    "guild_leader": guild_leader,
                    "players": [],
                    "bases": []
                }
            for player in players_data:
                last_online_time = player[7]
                inactive_guilds[guild_id]["players"].append({
                        "name": player[0],
                        "uid": player[1],
                        "level": player[2],
                        "caught": player[3],
                        "owned": player[4],
                        "encounters": player[5],
                        "uniques": player[6],
                        "last_online": f"{player[7]}"
                    })
            inactive_guilds[guild_id]["bases"].extend(bases)
            guild_count += 1
            base_count += len(bases)
            kill_commands.extend([f"killnearestbase {raw_data.replace(',', '')}" for _, raw_data in bases])
    for guild_id, guild_info in inactive_guilds.items():
        print(f"Guild: {guild_info['guild_name']} | Guild Leader: {guild_info['guild_leader']} | Guild ID: {guild_id}")
        print(f"Guild Players: {len(guild_info['players'])}")
        for player in guild_info["players"]:
            print(f"  Player: {player['name']} | UID: {player['uid']} | Level: {player['level']} | Caught: {player['caught']} | Owned: {player['owned']} | Encounters: {player['encounters']} | Uniques: {player['uniques']} | Last Online: {player['last_online']}")
        print(f"Base Locations: {len(guild_info['bases'])}")
        for base_id, raw_data in guild_info["bases"]:
            print(f"  Base ID: {base_id} | RawData: {raw_data}")
        print("-" * 40)
    print(f"\nFound {guild_count} guild(s) with {base_count} base(s).")
    if kill_commands:
        with open("palguard_bases.log", "w", encoding='utf-8') as log_file: log_file.writelines(f"{command}\n" for command in kill_commands)
        print(f"Successfully wrote {len(kill_commands)} kill commands to palguard_bases.log.")
    else: print("No kill commands were generated.")
    if inactivity_days: print(f"Inactivity filter applied: >= {inactivity_days} day(s).")
    if max_level: print(f"Player level filter applied: <= {max_level} level(s).")
if __name__ == "__main__":
    filter_type = input("Choose filter type:\n1) Inactivity (filter guilds based on days since last activity)\n2) Level (filter guilds based on maximum player level)\n3) Both (apply both inactivity and level filters)\nEnter your choice (1, 2, or 3): ")
    if filter_type == "1":
        inactivity_days = int(input("Enter the number of inactivity days to filter guilds: "))
        parse_log(inactivity_days=inactivity_days)
    elif filter_type == "2":
        max_level = int(input("Enter the maximum player level to filter guilds: "))
        parse_log(max_level=max_level)
    elif filter_type == "3":
        inactivity_days = int(input("Enter the number of inactivity days to filter guilds: "))
        max_level = int(input("Enter the maximum player level to filter guilds: "))
        parse_log(inactivity_days=inactivity_days, max_level=max_level)