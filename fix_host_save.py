from fix_save import *
def main():
    try:
        if len(sys.argv) < 2:
            print('Usage: fix_host_save.py <save_path>')
            exit(1)
        save_path = sys.argv[1]        
        new_guid = input("Enter new GUID: ")
        old_guid = input("Enter old GUID: ")
        guild_fix = True
        if new_guid[-4:] == '.sav' or old_guid[-4:] == '.sav':
            print('ERROR: You should be using only the GUID, not the entire file name.')
            exit(1)
        if len(new_guid) != 32:
            print(f'ERROR: Your <new_guid> should be 32 characters long, but it is {len(new_guid)} characters long.')
            exit(1)
        if len(old_guid) != 32:
            print(f'ERROR: Your <old_guid> should be 32 characters long, but it is {len(old_guid)} characters long.')
            exit(1)
        if new_guid == old_guid:
            print('ERROR: You\'re using the same GUID for both the <new_guid> and <old_guid>.')
            exit(1)
        new_guid_formatted = '{}-{}-{}-{}-{}'.format(new_guid[:8], new_guid[8:12], new_guid[12:16], new_guid[16:20], new_guid[20:]).lower()
        old_guid_formatted = '{}-{}-{}-{}-{}'.format(old_guid[:8], old_guid[8:12], old_guid[12:16], old_guid[16:20], old_guid[20:]).lower()
        level_sav_path = os.path.join(save_path, 'Level.sav')
        old_sav_path = os.path.join(save_path, 'Players', old_guid + '.sav')
        new_sav_path = os.path.join(save_path, 'Players', new_guid + '.sav')
        if not os.path.exists(save_path):
            print(f'ERROR: Your given <save_path> "{save_path}" does not exist.')
            exit(1)
        if not os.path.exists(new_sav_path):
            print(f'ERROR: Your player save "{new_sav_path}" does not exist. Did the player create a character?')
            exit(1)
        print('WARNING: Running this script WILL change your save files... Backup recommended.')
        input('Press enter to continue...')
        level_json = sav_to_json(level_sav_path)
        old_json = sav_to_json(old_sav_path)
        print('Modifying JSON save data...')
        old_json['properties']['SaveData']['value']['PlayerUId']['value'] = new_guid_formatted
        json_to_sav(level_json, level_sav_path)
        json_to_sav(old_json, old_sav_path)
        if os.path.exists(new_sav_path):
            os.remove(new_sav_path)
        os.rename(old_sav_path, new_sav_path)
        print('Fix has been applied! Have fun!')
    except (FileNotFoundError, ValueError, KeyError) as e:
        print(f"ERROR: {e}")
        exit(1)
def sav_to_json(filepath):
    print(f"Converting {filepath} to JSON")
    print("Decompressing sav file")
    with open(filepath, "rb") as f:
        data = f.read()
        raw_gvas, _ = decompress_sav_to_gvas(data)
    print("Loading GVAS file")
    #gvas_file = GvasFile.read(raw_gvas, PALWORLD_TYPE_HINTS, PALWORLD_CUSTOM_PROPERTIES)
    gvas_file = ProgressGvasFile.read(raw_gvas, PALWORLD_TYPE_HINTS, SKP_PALWORLD_CUSTOM_PROPERTIES)
    json_data = gvas_file.dump()
    return json_data
def json_to_sav(json_data, output_filepath):
    print(f"Converting data to SAV, saving to {output_filepath}")
    gvas_file = GvasFile.load(json_data)
    print("Compressing SAV file")
    if (
        "Pal.PalWorldSaveGame" in gvas_file.header.save_game_class_name
        or "Pal.PalLocalWorldSaveGame" in gvas_file.header.save_game_class_name
    ):
        save_type = 0x32
    else:
        save_type = 0x31
    #sav_file = compress_gvas_to_sav(gvas_file.write(PALWORLD_CUSTOM_PROPERTIES), save_type)
    sav_file = compress_gvas_to_sav(gvas_file.write(SKP_PALWORLD_CUSTOM_PROPERTIES), save_type)
    print(f"Writing SAV file to {output_filepath}")
    with open(output_filepath, "wb") as f:
        f.write(sav_file)
if __name__ == '__main__':
    main()