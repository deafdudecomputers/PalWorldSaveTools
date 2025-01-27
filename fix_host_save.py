from scan_save import *
def fix_save(save_path, new_guid, old_guid, guild_fix=True):
    if new_guid[-4:] == '.sav' or old_guid[-4:] == '.sav':
        print('ERROR: You should be using only the GUID, not the entire file name.')
        sys.exit(1)
    if len(new_guid) != 32:
        print(f'ERROR: Your <new_guid> should be 32 characters long, but it is {len(new_guid)} characters long.')
        sys.exit(1)
    if len(old_guid) != 32:
        print(f'ERROR: Your <old_guid> should be 32 characters long, but it is {len(old_guid)} characters long.')
        sys.exit(1)
    if new_guid == old_guid:
        print('ERROR: You\'re using the same GUID for both the <new_guid> and <old_guid>.')
        sys.exit(1)
    new_guid_formatted = '{}-{}-{}-{}-{}'.format(new_guid[:8], new_guid[8:12], new_guid[12:16], new_guid[16:20], new_guid[20:]).lower()
    old_guid_formatted = '{}-{}-{}-{}-{}'.format(old_guid[:8], old_guid[8:12], old_guid[12:16], old_guid[16:20], old_guid[20:]).lower()
    level_sav_path = os.path.join(save_path, 'Level.sav')
    old_sav_path = os.path.join(save_path, 'Players', old_guid + '.sav')
    new_sav_path = os.path.join(save_path, 'Players', new_guid + '.sav')
    if not os.path.exists(save_path):
        print(f'ERROR: Your given <save_path> "{save_path}" does not exist.')
        sys.exit(1)
    if not os.path.exists(new_sav_path):
        print(f'ERROR: Your player save "{new_sav_path}" does not exist. Did the player create a character?')
        sys.exit(1)
    level_json = sav_to_json(level_sav_path)
    old_json = sav_to_json(old_sav_path)
    print('Modifying JSON save data...')
    old_json['properties']['SaveData']['value']['PlayerUId']['value'] = new_guid_formatted
    old_instance_id = old_json['properties']['SaveData']['value']['IndividualId']['value']['InstanceId']['value']
    if guild_fix:
        group_ids = level_json['properties']['worldSaveData']['value']['GroupSaveDataMap']['value']
        for group_id in group_ids:
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
    json_to_sav(level_json, level_sav_path)
    json_to_sav(old_json, old_sav_path)
    if os.path.exists(new_sav_path): os.remove(new_sav_path)
    os.rename(old_sav_path, new_sav_path)
    print('Fix has been applied! Have fun!')
def sav_to_json(filepath):
    print(f"Converting {filepath} to JSON")
    print("Decompressing sav file")
    with open(filepath, "rb") as f:
        data = f.read()
        raw_gvas, save_type, cnk_header = decompress_sav_to_gvas(data)
    print("Loading GVAS file")
    gvas_file = ProgressGvasFile.read(raw_gvas, PALWORLD_TYPE_HINTS, SKP_PALWORLD_CUSTOM_PROPERTIES)
    json_data = gvas_file.dump()
    return json_data
def json_to_sav(json_data, output_filepath):
    print(f"Converting data to SAV, saving to {output_filepath}")
    gvas_file = GvasFile.load(json_data)
    print("Compressing SAV file")
    save_type = 0x32 if "Pal.PalWorldSaveGame" in gvas_file.header.save_game_class_name or "Pal.PalLocalWorldSaveGame" in gvas_file.header.save_game_class_name else 0x31
    sav_file = compress_gvas_to_sav(gvas_file.write(SKP_PALWORLD_CUSTOM_PROPERTIES), save_type)
    print(f"Writing SAV file to {output_filepath}")
    with open(output_filepath, "wb") as f: f.write(sav_file)
def extract_player_data(log_file):
    players = {}
    with open(log_file, 'r', encoding='utf-8') as f: log_data = f.read()
    player_pattern = r"Player: (\w+)\s+\| UID: ([a-f0-9\-]+)"
    matches = re.findall(player_pattern, log_data)
    for match in matches:
        player_name, player_uid = match
        player_uid = player_uid.replace("-", "").upper() 
        players[player_uid] = player_name
    return players
def main():
    sg.theme('Dark')
    layout = [
        [sg.Text("Please select the \"Level.sav\" file that should be updated:")],
        [sg.InputText(key="file_path", enable_events=True, default_text=os.path.join("PalWorldSave", "Level.sav")), sg.FileBrowse(file_types=(("SAV Files", "*.sav"),))],
        [sg.Text("Select the old GUID:")],
        [sg.Combo([], key='old_guid', enable_events=True, size=(40, 1))],
        [sg.Text("Select the new GUID:")],
        [sg.Combo([], key='new_guid', size=(40, 1))],
        [sg.Button("Migrate", key='button_migrate')],
        [sg.ProgressBar(100, orientation='h', size=(20, 20), key='progressbar')],
        [sg.Text("", key='progressbarText')],]
    icon_path = os.path.join("internal_libs", "pal.ico")
    window = sg.Window("GUID Migration Tool", layout, icon=icon_path)
    player_files = []
    players = {}
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Cancel": break
        if event == "file_path":
            file_path = values["file_path"]
            if not os.path.exists(file_path): sg.popup(f"The file doesn't exist. Please select a valid \"Level.sav\" file.", text_color='lightcoral')
            else:
                folder_path = os.path.dirname(file_path)
                players_folder = os.path.join(folder_path, "Players")
                if os.path.exists(players_folder):
                    player_files = [f[:-4] for f in os.listdir(players_folder) if f.endswith(".sav")]
                    if len(player_files) <= 1:
                        sg.popup("There should be at least two different saves in the Players folder to proceed.", text_color='lightcoral')
                        window.close()
                        sys.exit(1)
                    try:
                        LoadFile(file_path)
                        ShowPlayers()
                    except Exception as e: sg.popup(f"Error loading the file: {e}", text_color='lightcoral')
                    log_file = 'players.log'
                    players = extract_player_data(log_file)
                    player_files_with_names = []
                    for save in player_files:
                        save_uid = save.replace("-", "").upper()
                        if save_uid in players: player_files_with_names.append(f"{players[save_uid]} ({save_uid})")
                        else: player_files_with_names.append(f"Unknown ({save_uid})")
                    window['old_guid'].update(values=player_files_with_names)
                    window['new_guid'].update(values=player_files_with_names)
                else:
                    sg.popup("No Players folder found.", text_color='lightcoral')
        if event == "old_guid":
            old_guid_name = values["old_guid"]
            old_guid = re.search(r'\((.*?)\)', old_guid_name).group(1)
            available_new_guids = [guid for guid in player_files if guid != old_guid]
            player_files_with_names = []
            for save in available_new_guids:
                save_uid = save.replace("-", "").upper()
                if save_uid in players: player_files_with_names.append(f"{players[save_uid]} ({save_uid})")
                else: player_files_with_names.append(f"Unknown ({save_uid})")
            window['new_guid'].update(values=player_files_with_names)
        if event == "new_guid":
            new_guid_name = values["new_guid"]
            new_guid = re.search(r'\((.*?)\)', new_guid_name).group(1)
            available_old_guids = [guid for guid in player_files if guid != new_guid]
            player_files_with_names = []
            for save in available_old_guids:
                save_uid = save.replace("-", "").upper()
                if save_uid in players: player_files_with_names.append(f"{players[save_uid]} ({save_uid})")
                else: player_files_with_names.append(f"Unknown ({save_uid})")
            window['old_guid'].update(values=player_files_with_names)
        if event == "button_migrate":
            new_guid_name = values['new_guid']
            old_guid_name = values['old_guid']
            file_path = values["file_path"]
            old_guid = re.search(r'\((.*?)\)', old_guid_name).group(1)
            new_guid = re.search(r'\((.*?)\)', new_guid_name).group(1)
            if not new_guid or not old_guid: sg.popup("Both GUID fields are required!", text_color='lightcoral')
            else:
                window['progressbarText'].update("Validating and migrating save files...")
                window['progressbar'].update_bar(30)
                window.refresh()
                try:
                    fix_save(folder_path, new_guid, old_guid)
                    window['progressbarText'].update("Migration successful!")
                    window['progressbar'].update_bar(100)
                    sg.popup("Finished migrating. Have fun!")
                except Exception as e:
                    window['progressbarText'].update("An error occurred during migration.")
                    sg.popup(f"Error: {e}", text_color='lightcoral')
    window.close()
if __name__ == "__main__":
    file_path = 'players.log'
    if os.path.exists(file_path):
        with open(file_path, 'w'): pass
    main()