from internal_libs.import_libs import *
players_folder = "PalWorldSave/Players"
def sanitize_uid(uid):
    return uid.replace("-", "")
def extract_uid_from_sav(save_file):
    steam_uid = save_file[:-4]
    nosteam_uid = PlayerUid2NoSteam(
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
    steam_uid, nosteam_uid = extract_uid_from_sav(save_file)
    nosteam_file = nosteam_uid + ".sav"
    print(f"Palworld UID Save: {steam_uid}.sav | NoSteam Save: {nosteam_file}")
    if nosteam_file in save_files:
        print(f"Found NoSteam counterpart: {nosteam_file}")
        nosteam_saves.append(nosteam_file)
        matching_pairs.append((save_file, nosteam_file))
print("Checking if there's matching pairs...")
if matching_pairs:
    print("Now inspecting the matching ones...")
    for steam_file, nosteam_file in matching_pairs:
        print(f"Steam: {steam_file} | NoSteam: {nosteam_file}")
    total_deletions = 0
    for _, nosteam_file in matching_pairs:
        os.remove(os.path.join(players_folder, nosteam_file))
        total_deletions += 1
        print(f"Deleted NoSteam save: {nosteam_file}")
        if not os.path.exists(os.path.join(players_folder, nosteam_file)):
            print(f"Successfully confirmed deletion of: {nosteam_file}")
    print(f"Total NoSteam saves deleted: {total_deletions}")
else:
    print("There's no matching pairs...")
print(f"Total .sav files processed: {total_processed_files}")