from internal_libs.import_libs import *
steam_input = input("Enter Steam ID (with or without 'steam_' or full URL): ")
if "steamcommunity.com/profiles/" in steam_input:
    steam_input = steam_input.split("steamcommunity.com/profiles/")[1].split("/")[0]
elif steam_input.startswith("steam_"):
    steam_input = steam_input[6:]
try:
    steam_id = int(steam_input)
    palworld_uid = steamIdToPlayerUid(steam_id)
    nosteam_uid = PlayerUid2NoSteam(int.from_bytes(toUUID(palworld_uid).raw_bytes[0:4], byteorder='little')) + "-0000-0000-0000-000000000000"
    print("Palworld UID:", str(palworld_uid).upper())
    print("NoSteam UID:", nosteam_uid.upper())
except ValueError:
    print("Invalid Steam ID entered. Please provide a valid number.")