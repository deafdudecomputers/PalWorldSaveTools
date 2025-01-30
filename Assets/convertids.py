from import_libs import *
def get_steam_id_from_local():
    local_app_data_path = os.path.expandvars(r"%localappdata%\Pal\Saved\SaveGames")
    try:
        if not os.path.exists(local_app_data_path): return None
        subdirs = [d for d in os.listdir(local_app_data_path) if os.path.isdir(os.path.join(local_app_data_path, d))]
        if not subdirs: return None
        return subdirs[0]
    except: return None
steam_id_from_local = get_steam_id_from_local()
if steam_id_from_local:
    steam_id = int(steam_id_from_local)
    palworld_uid = steamIdToPlayerUid(steam_id)
    nosteam_uid = PlayerUid2NoSteam(int.from_bytes(toUUID(palworld_uid).raw_bytes[0:4], byteorder='little')) + "-0000-0000-0000-000000000000"
    print(f"Your SteamID: {steam_id_from_local}")
    print(f"Your Steam Profile URL: https://steamcommunity.com/profiles/{steam_id_from_local}")
    print("Your Palworld UID:", str(palworld_uid).upper())
    print("Your NoSteam UID:", nosteam_uid.upper())
steam_input = input("Enter SteamID (with or without 'steam_' or full URL): ")
if "steamcommunity.com/profiles/" in steam_input: steam_input = steam_input.split("steamcommunity.com/profiles/")[1].split("/")[0]
elif steam_input.startswith("steam_"): steam_input = steam_input[6:]
try:
    steam_id = int(steam_input)
    palworld_uid = steamIdToPlayerUid(steam_id)
    nosteam_uid = PlayerUid2NoSteam(int.from_bytes(toUUID(palworld_uid).raw_bytes[0:4], byteorder='little')) + "-0000-0000-0000-000000000000"
    print("Palworld UID:", str(palworld_uid).upper())
    print("NoSteam UID:", nosteam_uid.upper())
except ValueError: pass