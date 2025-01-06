import os
import re
from datetime import datetime, timedelta
def parse_log(inactivity_days):
    log_file = "fix_save.log"
    if not os.path.exists(log_file):
        print(f"Log file '{log_file}' not found in the current directory.")
        return
    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    guilds = content.split("\n\n")
    threshold_time = datetime.now() - timedelta(days=inactivity_days)
    inactive_guilds = []
    guild_count = 0
    base_count = 0
    kill_commands = []
    for guild in guilds:
        players_data = re.findall(r"Player: .+? Last Online: (.+?) \(", guild)
        bases = re.findall(r"Base \d+: Old: .+? New: .+? RawData: (.+)", guild)
        if not players_data or not bases:
            continue
        player_last_online = []
        for player_time in players_data:
            try:
                player_last_online.append(datetime.strptime(player_time, "%Y-%m-%d %H:%M:%S"))
            except ValueError:
                continue
        if all(last_online <= threshold_time for last_online in player_last_online):
            inactive_guilds.append((guild, bases))
            guild_count += 1
            base_count += len(bases)
            for base in bases:
                base_data = base.replace(",", "")
                kill_commands.append(f"killnearestbase {base_data}")
    for inactive_guild, bases in inactive_guilds:
        guild_id = re.search(r"Guild ID: ([a-f0-9-]+)", inactive_guild).group(1)
        print(f"Guild ID: {guild_id}")
        print("Base Locations:")
        for base in bases:
            print(f"  RawData: {base}")
        print("\n" + "-"*40 + "\n")
    print(f"\nFound {guild_count} guild(s) with {base_count} base(s).")
    if kill_commands:
        with open("palguard_bases.log", "w", encoding='utf-8') as log_file:
            for command in kill_commands:
                log_file.write(f"{command}\n")
        print(f"Successfully wrote {len(kill_commands)} kill commands to palguard_bases.log.")
    else:
        print("No kill commands were generated.")
if __name__ == "__main__":
    inactivity_days = int(input("Enter the number of inactivity days to filter guilds: "))
    parse_log(inactivity_days)