from internal_libs.import_libs import *
players_folder = "LocalWorldSave/Players"
def sanitize_uid(uid):
    return uid.replace("-", "")
def extract_uid_from_sav(save_file):
    steam_uid = save_file[:-4]
    xbox_uid = PlayerUid2NoSteam(
        int.from_bytes(toUUID(steam_uid).raw_bytes[0:4], byteorder='little')
    ) + "-0000-0000-0000-000000000000"
    return steam_uid, sanitize_uid(nosteam_uid)
save_files = [f for f in os.listdir(players_folder) if f.endswith(".sav")]
nosteam_saves = []
total_processed_files = 0
matching_pairs = []
for save_file in save_files:
    print(f"Processing: {save_file}")
    total_processed_files += 1
    steam_uid, xbox_uid = extract_uid_from_sav(save_file)
    xbox_file = xbox_uid + ".sav"
    print(f"Palworld UID Save: {steam_uid}.sav | Xbox Save: {xbox_file}")
    if xbox_file in save_files:
        print(f"Found Xbox counterpart: {xbox_file}")
        Xbox_saves.append(xbox_file)
        matching_pairs.append((save_file, xbox_file))
print("Checking if there's matching pairs...")
if matching_pairs:
    print("Now inspecting the matching ones...")
    for steam_file, xbox_file in matching_pairs:
        print(f"Steam: {steam_file} | Xbox: {xbox_file}")
    total_deletions = 0
    for _, xbox_file in matching_pairs:
        os.remove(os.path.join(players_folder, xbox_file))
        total_deletions += 1
        print(f"Deleted Xbox save: {xbox_file}")
        if not os.path.exists(os.path.join(players_folder, xbox_file)):
            print(f"Successfully confirmed deletion of: {xbox_file}")
    print(f"Total Xbox saves deleted: {total_deletions}")
else:
    print("There's no matching pairs...")
print(f"Total .sav files processed: {total_processed_files}")