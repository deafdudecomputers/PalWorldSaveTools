from internal_libs.import_libs import *
steam_input = input("Enter Steam ID (with or without 'steam_'): ")
if steam_input.startswith("steam_"):
    steam_input = steam_input[6:]
try:
    steam_id = int(steam_input)
    palworld_uid = steamIdToPlayerUid(steam_id)
    print("Palworld UID:", palworld_uid)
except ValueError:
    print("Invalid Steam ID entered. Please provide a valid number.")