import os, re
from datetime import datetime, timedelta
def parse_log(inactivity_days):
    log_file = "fix_save.log"
    if not os.path.exists(log_file): return print(f"Log file '{log_file}' not found in the current directory.")
    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f: content = f.read()
    guilds, threshold_time, inactive_guilds, kill_commands = content.split("\n\n"), datetime.now() - timedelta(days=inactivity_days), [], []
    guild_count = base_count = 0
    for guild in guilds:
        players_data, bases = re.findall(r"Player: .+? Last Online: (.+?) \(", guild), re.findall(r"Base \d+: Old: .+? New: .+? RawData: (.+)", guild)
        if not players_data or not bases: continue
        player_last_online = [datetime.strptime(player_time, "%Y-%m-%d %H:%M:%S") for player_time in players_data if re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", player_time)]
        if all(last_online <= threshold_time for last_online in player_last_online):
            inactive_guilds.append((guild, bases))
            guild_count += 1
            base_count += len(bases)
            kill_commands.extend([f"killnearestbase {base.replace(',', '')}" for base in bases])
    for inactive_guild, bases in inactive_guilds:
        guild_id = re.search(r"Guild ID: ([a-f0-9-]+)", inactive_guild).group(1)
        print(f"Guild ID: {guild_id}\nBase Locations:\n" + "".join(f"  RawData: {base}\n" for base in bases) + "\n" + "-"*40 + "\n")
    print(f"\nFound {guild_count} guild(s) with {base_count} base(s).")
    if kill_commands:
        with open("palguard_bases.log", "w", encoding='utf-8') as log_file: log_file.writelines(f"{command}\n" for command in kill_commands)
        print(f"Successfully wrote {len(kill_commands)} kill commands to palguard_bases.log.")
    else: print("No kill commands were generated.")
if __name__ == "__main__": parse_log(int(input("Enter the number of inactivity days to filter guilds: ")))