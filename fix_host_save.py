from fix_save import *
def main():
    if len(sys.argv) < 5:
        print('fix_host_save.py <save_path> <new_guid> <old_guid> <guild_fix>')
        exit(1)    
    save_path = sys.argv[1]
    new_guid = sys.argv[2]
    old_guid = sys.argv[3]
    guild_fix = sys.argv[4]    
    if guild_fix.lower() == 'true':
        guild_fix = True
    elif guild_fix.lower() == 'false':
        guild_fix = False
    else:
        print('ERROR: Invalid <guild_fix> argument. It should be either "True" or "False".')
        exit(1)    
    if new_guid[-4:] == '.sav' or old_guid[-4:] == '.sav':
        print('ERROR: It looks like you\'re providing the whole name of the file instead of just the GUID. For example, instead of using "<GUID>.sav" in the command, you should be using only the GUID.')
        exit(1)    
    if len(new_guid) != 32:
        print('ERROR: Your <new_guid> should be 32 characters long, but it is ' + str(len(new_guid)) + ' characters long. Make sure you copied the exact GUID.')
        exit(1)    
    if len(old_guid) != 32:
        print('ERROR: Your <old_guid> should be 32 characters long, but it is ' + str(len(old_guid)) + ' characters long. Make sure you copied the exact GUID.')
        exit(1)    
    if new_guid == old_guid:
        print('ERROR: It looks like you\'re using the same GUID for both the <new_guid> and <old_guid> argument. Remember, you\'re moving GUIDs so you need your old one and your new one.')
        exit(1)    
    new_guid_formatted = '{}-{}-{}-{}-{}'.format(new_guid[:8], new_guid[8:12], new_guid[12:16], new_guid[16:20], new_guid[20:]).lower()
    old_guid_formatted = '{}-{}-{}-{}-{}'.format(old_guid[:8], old_guid[8:12], old_guid[12:16], old_guid[16:20], old_guid[20:]).lower()    
    level_sav_path = save_path + '/Level.sav'
    old_sav_path = save_path + '/Players/'+ old_guid + '.sav'
    new_sav_path = save_path + '/Players/' + new_guid + '.sav'
    level_json_path = level_sav_path + '.json'
    old_json_path = old_sav_path + '.json'    
    if not os.path.exists(save_path):
        print('ERROR: Your given <save_path> of "' + save_path + '" does not exist. Did you enter the correct path to your save folder?')
        exit(1)    
    if not os.path.exists(new_sav_path):
        print('ERROR: Your player save does not exist. Did you enter the correct new GUID of your player? It should look like "8E910AC2000000000000000000000000".\nDid your player create their character with the provided save? Once they create their character, a file called "' + new_sav_path + '" should appear. Look back over the steps in the README on how to get your new GUID.')
        exit(1)    
    print('WARNING: Running this script WILL change your save files and could \
potentially corrupt your data. It is HIGHLY recommended that you make a backup \
of your save folder before continuing. Press enter if you would like to continue.')
    input('> ')    
    level_json = sav_to_json(level_sav_path)
    old_json = sav_to_json(old_sav_path)    
    print('Modifying JSON save data...', end='', flush=True)
    old_json['properties']['SaveData']['value']['PlayerUId']['value'] = new_guid_formatted
    old_json['properties']['SaveData']['value']['IndividualId']['value']['PlayerUId']['value'] = new_guid_formatted
    old_instance_id = old_json['properties']['SaveData']['value']['IndividualId']['value']['InstanceId']['value']    
    instance_ids_len = len(level_json['properties']['worldSaveData']['value']['CharacterSaveParameterMap']['value'])
    for i in range(instance_ids_len):
        instance_id = level_json['properties']['worldSaveData']['value']['CharacterSaveParameterMap']['value'][i]['key']['InstanceId']['value']
        if instance_id == old_instance_id:
            level_json['properties']['worldSaveData']['value']['CharacterSaveParameterMap']['value'][i]['key']['PlayerUId']['value'] = new_guid_formatted
            break    
    if guild_fix:
        group_ids_len = len(level_json['properties']['worldSaveData']['value']['GroupSaveDataMap']['value'])
        for i in range(group_ids_len):
            group_id = level_json['properties']['worldSaveData']['value']['GroupSaveDataMap']['value'][i]
            if group_id['value']['GroupType']['value']['value'] == 'EPalGroupType::Guild':
                group_data = group_id['value']['RawData']['value']
                if 'individual_character_handle_ids' in group_data:
                    handle_ids = group_data['individual_character_handle_ids']
                    for j in range(len(handle_ids)):
                        if handle_ids[j]['instance_id'] == old_instance_id:
                            handle_ids[j]['guid'] = new_guid_formatted
                if 'admin_player_uid' in group_data and old_guid_formatted == group_data['admin_player_uid']:
                    group_data['admin_player_uid'] = new_guid_formatted
                if 'players' in group_data:
                    for j in range(len(group_data['players'])):
                        if old_guid_formatted == group_data['players'][j]['player_uid']:
                            group_data['players'][j]['player_uid'] = new_guid_formatted
    print('Done!', flush=True)    
    json_to_sav(level_json, level_sav_path)
    json_to_sav(old_json, old_sav_path)    
    if os.path.exists(new_sav_path):
        os.remove(new_sav_path)
    os.rename(old_sav_path, new_sav_path)
    print('Fix has been applied! Have fun!')
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