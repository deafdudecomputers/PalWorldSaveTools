from import_libs import *
from datetime import datetime, timedelta
STRUCT_START = b'\x0f\x00\x00\x00StructProperty\x00'
MAP_START = b'\x0c\x00\x00\x00MapProperty\x00'
ARRAY_START = b'\x0e\x00\x00\x00ArrayProperty\x00'
def backup_whole_directory(source_folder, backup_folder):
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_folder, f"PalWorldSave_backup_{timestamp}")
    shutil.copytree(source_folder, backup_path)
    print(f"Backup of {source_folder} created at: {backup_path}")
def _convert_stringval(value):
    if hasattr(value, 'typename'):
        value = str(value)
        try:
            value = int(value)
        except (ValueError, TypeError):
            pass
    return value
ttk._convert_stringval = _convert_stringval
class SkipFArchiveWriter(FArchiveWriter):
    data: io.BytesIO
    size: int
    custom_properties: dict[str, tuple[Callable, Callable]]
    debug: bool
    def __init__(
            self,
            custom_properties: dict[str, tuple[Callable, Callable]] = {},
            debug: bool = os.environ.get("DEBUG", "0") == "1",):
        self.data = io.BytesIO()
        self.custom_properties = custom_properties
        self.debug = debug
    def curr_properties(self, properties):
        for key in properties:
            if key not in ['custom_type', 'skip_type']:
                self.fstring(key)
                self.property(properties[key])
    def properties(self, properties: dict[str, Any]):
        for key in properties:
            if key not in ['custom_type', 'skip_type']:
                self.fstring(key)
                self.property(properties[key])
        self.fstring("None")
    def copy(self) -> "SkipFArchiveWriter":
        return SkipFArchiveWriter(self.custom_properties)
    def write_sections(self, props, section_ranges, bytes, parent_section_size_idx):
        props = [{k: v} for k, v in props.items()]
        prop_bytes = []
        for prop in props:
            self.curr_properties(prop)
            prop_bytes.append(self.bytes())
            self.data = io.BytesIO()
        bytes_concat_array = []
        last_end = 0
        n_bytes_more = 0
        old_size = struct.unpack('Q', bytes[parent_section_size_idx:parent_section_size_idx + 8])[0]
        for prop_byte, (section_start, section_end) in zip(prop_bytes, section_ranges):
            bytes_concat_array.append(bytes[last_end:section_start])
            bytes_concat_array.append(prop_byte)
            n_bytes_more += len(prop_byte) - (section_end - section_start)
            last_end = section_end
        bytes_concat_array.append(bytes[last_end:])
        new_size_bytes = struct.pack('Q', old_size + n_bytes_more)
        bytes_concat_array[0] = bytes_concat_array[0][:parent_section_size_idx] + new_size_bytes + bytes_concat_array[0][parent_section_size_idx + 8:]
        output = b''
        for byte_segment in bytes_concat_array:
            output += byte_segment
        return output
    def guid(self, u): 
        self.data.write(u)
    def optional_guid(self, u):
        if u is None:
            self.bool(False)
        else:
            self.bool(True)
            self.data.write(u)
class SkipFArchiveReader(FArchiveReader):
    def __init__(
            self,
            data,
            type_hints: dict[str, str] = {},
            custom_properties: dict[str, tuple[Callable, Callable]] = {},
            debug=False,
            allow_nan=True):
        self.size = len(data)
        self.orig_data = data
        self.data = io.BytesIO(data)
        self.type_hints = type_hints
        self.debug = debug
        self.custom_properties = custom_properties
        self.allow_nan = allow_nan
    def curr_property(self, path: str = "") -> dict[str, Any]:
        properties = {}
        name = self.fstring()
        type_name = self.fstring()
        size = self.u64()
        properties[name] = self.property(type_name, size, f"{path}.{name}")
        return properties
    def internal_copy(self, data, debug: bool) -> "FArchiveReader":
        return SkipFArchiveReader(
            data,
            self.type_hints,
            self.custom_properties,
            debug=debug,
            allow_nan=self.allow_nan,)
    def skip(self, size: int) -> None:
        self.data.seek(size, 1)
    def properties_until_end(self, path: str = "") -> dict[str, Any]:
        properties = {}
        while True:
            name = self.fstring()
            if name == "None":
                break
            type_name = self.fstring()
            size = self.u64()
            properties[name] = self.property(type_name, size, f"{path}.{name}")
        return properties
    def guid(self):
        return self.data.read(16)
    def optional_guid(self):
        if self.data.read(1)[0]:
            return self.data.read(16)
        return None
    def encode(self, property_name):
        return struct.pack('i', len(property_name) + 1) + property_name.encode('ascii') + b'\x00'
    def find_property_start(self, property_name, type_start=STRUCT_START, offset=0, reverse=False):
        if not reverse:
            return self.orig_data[offset:].find(self.encode(property_name) + type_start) + offset
        return self.orig_data[offset:].rfind(self.encode(property_name) + type_start) + offset
    def load_section(self, property_name, type_start=STRUCT_START, path='.worldSaveData', reverse=False):
        find_timer = time.time()
        start_index = self.find_property_start(property_name, type_start, reverse=reverse)
        self.data.seek(start_index, 0)
        start_timer = time.time()
        prop = self.curr_property(path=path)
        end_timer = time.time()
        print(f"Property {property_name} loaded in {end_timer - start_timer} seconds, total time including find: {end_timer - find_timer}")
        return prop, (start_index, self.data.tell())
    def load_sections(self, prop_types, path='.worldSaveData', reverse=False):
        properties = {}
        end_idx = 0
        section_ranges = []
        for prop, type_start in prop_types:
            find_timer = time.time()
            start_idx = self.find_property_start(prop, type_start, offset=end_idx, reverse=reverse)
            if start_idx == end_idx - 1:
                raise ValueError(f"Property {prop} not found")
            self.data.seek(start_idx, 0)
            start_timer = time.time()
            properties.update(self.curr_property(path=path))
            end_timer = time.time()
            end_idx = self.data.tell()
            print(f"Property {prop} loaded in {end_timer - start_timer} seconds, total time including find: {end_timer - find_timer}")
            section_ranges.append((start_idx, end_idx))
        return properties, section_ranges
def skip_decode(
        reader: SkipFArchiveReader, type_name: str, size: int, path: str
) -> dict[str, Any]:
    if type_name == "ArrayProperty":
        array_type = reader.fstring()
        value = {
            "skip_type": type_name,
            "array_type": array_type,
            "id": reader.optional_guid(),
            "value": reader.read(size),
            "size": size}
    elif type_name == "MapProperty":
        key_type = reader.fstring()
        value_type = reader.fstring()
        _id = reader.optional_guid()
        value = {
            "skip_type": type_name,
            "key_type": key_type,
            "value_type": value_type,
            "id": _id,
            "value": reader.read(size),}
    elif type_name == "StructProperty":
        value = {
            "skip_type": type_name,
            "struct_type": reader.fstring(),
            "struct_id": reader.guid(),
            "id": reader.optional_guid(),
            "value": reader.read(size),}
    else:
        raise Exception(f"Expected ArrayProperty or MapProperty or StructProperty, got {type_name} in {path}")
    return value
def skip_encode(
        writer: FArchiveWriter, property_type: str, properties: dict[str, Any]
) -> int:
    if "skip_type" not in properties:
        if properties['custom_type'] in PALWORLD_CUSTOM_PROPERTIES is not None:
            return PALWORLD_CUSTOM_PROPERTIES[properties["custom_type"]][1](
                writer, property_type, properties)
    if property_type == "ArrayProperty":
        writer.fstring(properties["array_type"])
        writer.optional_guid(properties.get("id", None))
        writer.write(properties["value"])
        return len(properties["value"])
    elif property_type == "MapProperty":
        writer.fstring(properties["key_type"])
        writer.fstring(properties["value_type"])
        writer.optional_guid(properties.get("id", None))
        writer.write(properties["value"])
        return len(properties["value"])
    elif property_type == "StructProperty":
        writer.fstring(properties["struct_type"])
        writer.guid(properties["struct_id"])
        writer.optional_guid(properties.get("id", None))
        writer.write(properties["value"])
        return len(properties["value"])
    else:
        raise Exception(f"Expected ArrayProperty or MapProperty or StructProperty, got {property_type}")
def decode_group(
        reader: SkipFArchiveReader, type_name: str, size: int, path: str
) -> dict[str, Any]:
    if type_name != "MapProperty":
        raise Exception(f"Expected MapProperty, got {type_name}")
    value = reader.property(type_name, size, path, nested_caller_path=path)
    group_map = value["value"]
    for group in group_map:
        group_type = group["value"]["GroupType"]["value"]["value"]
        if group_type == "EPalGroupType::Guild":
            group_bytes = group["value"]["RawData"]["value"]
            group["value"]["RawData"]["value"] = decode_bytes(reader, group_bytes, group_type)
    return value
def instance_id_reader(reader):
    return {"guid": reader.guid(), "instance_id": reader.guid(),}
def decode_bytes(
        parent_reader: SkipFArchiveReader, group_bytes: Sequence[int], group_type: str
) -> dict[str, Any]:
    reader = parent_reader.internal_copy(group_bytes, debug=False)
    reader.skip(4)
    group_data = {
        "group_type": group_type,
        "group_id": reader.guid(),
        "group_name": reader.fstring(),
        "individual_character_handle_ids": reader.tarray(instance_id_reader),}
    org = {
        "org_type": reader.byte(),
        "base_ids": reader.tarray(uuid_reader),}
    group_data |= org
    guild: dict[str, Any] = {
        "base_camp_level": reader.i32(),
        "map_object_instance_ids_base_camp_points": reader.tarray(uuid_reader),
        "guild_name": reader.fstring(),}
    group_data |= guild
    guild = {
        "unknown_bytes": reader.byte_list(16),
        "admin_player_uid": reader.guid(),
        "players": [],}
    player_count = reader.i32()
    for _ in range(player_count):
        player = {
            "player_uid": reader.guid(),
            "player_info": {
                "last_online_real_time": reader.i64(),
                "player_name": reader.fstring(),},}
        guild["players"].append(player)
    group_data |= guild
    if not reader.eof():
        raise Exception("Warning: EOF not reached")
    return group_data
def encode_group(
        writer: FArchiveWriter, property_type: str, properties: dict[str, Any]
) -> int:
    if property_type != "MapProperty":
        raise Exception(f"Expected MapProperty, got {property_type}")
    custom_type = properties["custom_type"]
    del properties["custom_type"]
    group_map = properties["value"]
    encoded_list = []
    for i, group in enumerate(group_map):
        group_type = group["value"]["GroupType"]["value"]["value"]
        if group_type == "EPalGroupType::Guild":
            encoded_list.append((i, group["value"]["RawData"]["value"]))
            group["value"]["RawData"]["value"] = encode_bytes(group["value"]["RawData"]["value"])
    write_ret = writer.property_inner(property_type, properties)
    properties["custom_type"] = custom_type
    for i, orig_val in encoded_list:
        group_map[i]["value"]["RawData"]["value"] = orig_val
    return write_ret
def instance_id_writer(writer, d):
    writer.guid(d["guid"])
    writer.guid(d["instance_id"])
def encode_bytes(p: dict[str, Any]) -> bytes:
    outer_writer = SkipFArchiveWriter()
    writer = SkipFArchiveWriter()
    writer.guid(p["group_id"])
    writer.fstring(p["group_name"])
    writer.tarray(instance_id_writer, p["individual_character_handle_ids"])
    writer.byte(p["org_type"])
    writer.tarray(uuid_writer, p["base_ids"])
    writer.i32(p["base_camp_level"])
    writer.tarray(uuid_writer, p["map_object_instance_ids_base_camp_points"])
    writer.fstring(p["guild_name"])
    writer.write(bytes(p["unknown_bytes"]))
    writer.guid(p["admin_player_uid"])
    writer.i32(len(p["players"]))
    for i in range(len(p["players"])):
        writer.guid(p["players"][i]["player_uid"])
        writer.i64(p["players"][i]["player_info"]["last_online_real_time"])
        writer.fstring(p["players"][i]["player_info"]["player_name"])
    encoded_bytes = writer.bytes()
    outer_writer.u32(len(encoded_bytes))
    outer_writer.write(encoded_bytes)
    return outer_writer.bytes()
PALWORLD_CUSTOM_PROPERTIES[".worldSaveData.CharacterSaveParameterMap.Value.RawData"] = (skip_decode, skip_encode)
PALWORLD_CUSTOM_PROPERTIES[".worldSaveData.DynamicItemSaveData.DynamicItemSaveData.RawData"] = (skip_decode, skip_encode)
PALWORLD_CUSTOM_PROPERTIES[".worldSaveData.DynamicItemSaveData.DynamicItemSaveData.ID"] = (skip_decode, skip_encode)
PALWORLD_CUSTOM_PROPERTIES[".worldSaveData.CharacterContainerSaveData.Value.Slots"] = (skip_decode, skip_encode)
PALWORLD_CUSTOM_PROPERTIES[".worldSaveData.CharacterContainerSaveData.Value.RawData"] = (skip_decode, skip_encode)
PALWORLD_CUSTOM_PROPERTIES[".worldSaveData.ItemContainerSaveData.Value.BelongInfo"] = (skip_decode, skip_encode)
PALWORLD_CUSTOM_PROPERTIES[".worldSaveData.ItemContainerSaveData.Value.Slots"] = (skip_decode, skip_encode)
PALWORLD_CUSTOM_PROPERTIES[".worldSaveData.ItemContainerSaveData.Value.RawData"] = (skip_decode, skip_encode)
PALWORLD_CUSTOM_PROPERTIES[".worldSaveData.GroupSaveDataMap"] = (decode_group, encode_group)
PALWORLD_CUSTOM_PROPERTIES[".worldSaveData.GroupSaveDataMap.Value.RawData"] = (skip_decode, skip_encode)
OwnerPlayerUIdSearchPrefix = b'\x0f\x00\x00\x00OwnerPlayerUId\x00\x0f\x00\x00\x00StructProperty\x00\x10\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00Guid\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
LocalIdSearchPrefix = b'\x16\x00\x00\x00LocalIdInCreatedWorld\x00\x0f\x00\x00\x00StructProperty\x00\x10\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00Guid\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
PalSlotDataPrefix = b'\r\x00\x00\x00ByteProperty\x00\x00!\x00\x00\x00'
OldOwnerPlayerUIdPrefix = b'\x13\x00\x00\x00OldOwnerPlayerUIds\x00\x0e\x00\x00\x00ArrayProperty\x00'
OldOwnerPlayerUIdSuffix = b'\x06\x00\x00\x00MaxHP'
def find_id_match_prefix(encoded_bytes, prefix):
    start_idx = encoded_bytes.find(prefix) + len(prefix)
    return encoded_bytes[start_idx:start_idx + 16]
def find_all_ids_match_prefix(encoded_bytes, prefix):
    last_idx = 0
    start_idx = encoded_bytes.find(prefix)
    ids = []
    while start_idx != last_idx - 1:
        start_idx += len(prefix)
        last_idx = start_idx + 16
        ids.append(encoded_bytes[start_idx:last_idx])
        start_idx = encoded_bytes[last_idx:].find(prefix) + last_idx
    return ids
def find_all_occurrences_with_prefix(encoded_bytes, prefix):
    last_idx = 0
    start_idx = encoded_bytes.find(prefix)
    end_indices = []
    while start_idx != last_idx - 1:
        start_idx += len(prefix)
        last_idx = start_idx
        end_indices.append(start_idx)
        start_idx = encoded_bytes[last_idx:].find(prefix) + last_idx
    return end_indices
def fast_deepcopy(json_dict):
    return pickle.loads(pickle.dumps(json_dict, -1))
class SkipGvasFile(GvasFile):
    header: GvasHeader
    properties: dict[str, Any]
    trailer: bytes
    @staticmethod
    def read(
        data: bytes,
        type_hints: dict[str, str] = {},
        custom_properties: dict[str, tuple[Callable, Callable]] = {},
        allow_nan: bool = True,
    ) -> "GvasFile":
        gvas_file = SkipGvasFile()
        with SkipFArchiveReader(
            data,
            type_hints=type_hints,
            custom_properties=custom_properties,
            allow_nan=allow_nan,
        ) as reader:
            gvas_file.header = GvasHeader.read(reader)
            gvas_file.properties = reader.properties_until_end()
            gvas_file.trailer = reader.read_to_end()
            if gvas_file.trailer != b"\x00\x00\x00\x00":
                print(
                    f"{len(gvas_file.trailer)} bytes of trailer data, file may not have fully parsed"
                )
        return gvas_file
    def write(
        self, custom_properties: dict[str, tuple[Callable, Callable]] = {}
    ) -> bytes:
        writer = SkipFArchiveWriter(custom_properties)
        self.header.write(writer)
        writer.properties(self.properties)
        writer.write(self.trailer)
        return writer.bytes()
def main():
    global host_sav_path, level_sav_path, t_level_sav_path, t_host_sav_path, host_json, level_json, targ_json, targ_lvl
    if None in [level_sav_path, t_level_sav_path, selected_source_player, selected_target_player]:
        messagebox.showerror(message='Please have both level files and players selected before starting transfer.')
        return
    response = messagebox.askyesno(title='WARNING', message='WARNING: Running this script WILL change your target save files and could \
potentially corrupt your data. It is HIGHLY recommended that you make a backup \
of your save folder before continuing. Press Yes if you would like to continue.')
    if not response: return
    host_json_gvas = load_player_file(level_sav_path, selected_source_player)
    if host_json_gvas is None: return
    host_json = host_json_gvas.properties
    targ_json_gvas = load_player_file(t_level_sav_path, selected_target_player)
    if targ_json_gvas is None: return
    targ_json = targ_json_gvas.properties
    host_guid = UUID.from_str(selected_source_player).raw_bytes
    host_instance_id = host_json["SaveData"]["value"]["IndividualId"]["value"]["InstanceId"]["value"]
    pal_player_uid_filters = [b'\x00'*16, b'\x00'*12 + b'\x01\x00\x00\x00'] 
    count = 0
    found = 0
    expected_containers = 7
    exported_map = {}
    param_maps = []
    palcount = 0
    for character_save_param in level_json["CharacterSaveParameterMap"]["value"]:
        instance_id = character_save_param["key"]["InstanceId"]["value"]
        if instance_id == host_instance_id:
            exported_map = character_save_param
            count = count + 1
            found = 1
            print('found instance')
        elif character_save_param["key"]["PlayerUId"]["value"] in pal_player_uid_filters:
            if find_id_match_prefix(character_save_param['value']['RawData']['value'],
                                    OwnerPlayerUIdSearchPrefix) == host_guid:
                param_maps.append(fast_deepcopy(character_save_param))
                palcount += 1
    if not found:
        print("Couldn't find character instance data to export")
        messagebox.showerror(message="Couldn't find source character instance data in the source world save")
        return
    print("Found Character Parameter Map")
    print(f"Read {palcount} pals from source save")
    print("Searching for container data")
    host_save = host_json["SaveData"]["value"]
    inv_info = host_save["InventoryInfo"]["value"] if "InventoryInfo" in host_save else host_save["inventoryInfo"]["value"]
    inv_main = inv_info["CommonContainerId"]
    inv_key = inv_info["EssentialContainerId"]
    inv_weps = inv_info["WeaponLoadOutContainerId"]
    inv_armor = inv_info["PlayerEquipArmorContainerId"]
    inv_foodbag = inv_info["FoodEquipContainerId"]
    inv_pals = host_json["SaveData"]["value"]["PalStorageContainerId"]
    inv_otomo = host_json["SaveData"]["value"]["OtomoCharacterContainerId"]
    host_main = {}
    host_key = {}
    host_weps = {}
    host_armor = {}
    host_foodbag = {}
    host_pals = {}
    host_otomo = {}
    count = 0
    for container in level_json["CharacterContainerSaveData"]["value"]:
        container_id = container["key"]["ID"]["value"]
        if container_id == inv_pals["value"]["ID"]["value"]:
            print("Found host pal inventory")
            host_pals = container
            count = count + 1
        elif container_id == inv_otomo["value"]["ID"]["value"]:
            print("Found host otomo inventory")
            host_otomo = container
            count = count + 1
        if count >= 2:
            print("Found all pal containers")
            break
    dynamic_guids = set()
    for container in level_json["ItemContainerSaveData"]["value"]:
        container_id = container["key"]["ID"]["value"]
        if container_id == inv_main["value"]["ID"]["value"]:
            print("Found host main inventory")
            dynamic_guids |= set(find_all_ids_match_prefix(container['value']['Slots']['value'], LocalIdSearchPrefix))
            host_main = container
            count = count + 1
        elif container_id == inv_key["value"]["ID"]["value"]:
            print("Found host key inventory")
            dynamic_guids |= set(find_all_ids_match_prefix(container['value']['Slots']['value'], LocalIdSearchPrefix))
            host_key = container
            count = count + 1
        elif container_id == inv_weps["value"]["ID"]["value"]:
            print("Found host weapon inventory")
            dynamic_guids |= set(find_all_ids_match_prefix(container['value']['Slots']['value'], LocalIdSearchPrefix))
            host_weps = container
            count = count + 1
        elif container_id == inv_armor["value"]["ID"]["value"]:
            print("Found host armor inventory")
            dynamic_guids |= set(find_all_ids_match_prefix(container['value']['Slots']['value'], LocalIdSearchPrefix))
            host_armor = container
            count = count + 1
        elif container_id == inv_foodbag["value"]["ID"]["value"]:
            print("Found host food bag inventory")
            dynamic_guids |= set(find_all_ids_match_prefix(container['value']['Slots']['value'], LocalIdSearchPrefix))
            host_foodbag = container
            count = count + 1
        if count >= expected_containers:
            print("Found all target containers")
            break
    dynamic_guids.discard(b'\x00' * 16)
    dynamic_container_level_json = level_json['DynamicItemSaveData']['value']['values']
    level_additional_dynamic_containers = [(dynamic_container, dynamic_container.get('ID', {}).get('value')) for dynamic_container in dynamic_container_level_json]
    print(f"Copied {len(level_additional_dynamic_containers)} containers to target")
    if count < expected_containers:
        print("Missing container info! Only found " + str(count))
        messagebox.showerror(message="Missing container info! Only found " + str(count))
        return
    char_instanceid = targ_json["SaveData"]["value"]["IndividualId"]["value"]["InstanceId"]["value"]
    print("Transferring profile data...")
    if "TechnologyPoint" in host_json["SaveData"]["value"]:
        targ_json["SaveData"]["value"]["TechnologyPoint"] = host_json["SaveData"]["value"]["TechnologyPoint"]
    elif "TechnologyPoint" in targ_json["SaveData"]["value"]:
        targ_json["SaveData"]["value"]["TechnologyPoint"]["value"] = 0
    if "bossTechnologyPoint" in host_json["SaveData"]["value"]:
        targ_json["SaveData"]["value"]["bossTechnologyPoint"] = host_json["SaveData"]["value"]["bossTechnologyPoint"]
    elif "bossTechnologyPoint" in targ_json["SaveData"]["value"]:
        targ_json["SaveData"]["value"]["bossTechnologyPoint"]["value"] = 0
    targ_json["SaveData"]["value"]["UnlockedRecipeTechnologyNames"] = host_json["SaveData"]["value"]["UnlockedRecipeTechnologyNames"]
    targ_json["SaveData"]["value"]["PlayerCharacterMakeData"] = host_json["SaveData"]["value"]["PlayerCharacterMakeData"]
    if 'RecordData' in host_json["SaveData"]["value"]:
        targ_json["SaveData"]["value"]["RecordData"] = host_json["SaveData"]["value"]["RecordData"]
    elif 'RecordData' in targ_json["SaveData"]:
        del targ_json['RecordData']
    target_section_load_handle.join()
    found = False
    for i, char_save_instance in enumerate(targ_lvl["CharacterSaveParameterMap"]["value"]):
        instance_id = char_save_instance["key"]["InstanceId"]["value"]
        if instance_id == char_instanceid:
            print("Existing character parameter map found, overwriting")
            char_save_instance['value'] = exported_map['value']
            found = True
            break
    if not found:
        print("Couldn't find character paramater map, aborting")
        messagebox.showerror(message="Couldn't find target character instance in target world save.")
        return
    print("Searching for target containers")
    targ_save = targ_json["SaveData"]["value"]
    inv_info = targ_save["InventoryInfo"]["value"] if "InventoryInfo" in targ_save else targ_save["inventoryInfo"]["value"]
    inv_main = inv_info["CommonContainerId"]
    inv_key = inv_info["EssentialContainerId"]
    inv_weps = inv_info["WeaponLoadOutContainerId"]
    inv_armor = inv_info["PlayerEquipArmorContainerId"]
    inv_foodbag = inv_info["FoodEquipContainerId"]
    host_inv_pals = inv_pals
    host_inv_otomo = inv_otomo
    inv_pals = targ_json["SaveData"]["value"]["PalStorageContainerId"]
    inv_otomo = targ_json["SaveData"]["value"]["OtomoCharacterContainerId"]
    group_id = None
    targ_uid = targ_json["SaveData"]["value"]["IndividualId"]["value"]["PlayerUId"]["value"]
    if not keep_old_guild_id:
        for group_data in targ_lvl["GroupSaveDataMap"]["value"]:
            if group_data["value"]["GroupType"]["value"]["value"] == "EPalGroupType::Guild":
                if targ_uid in [player_item['player_uid'] for player_item in group_data["value"]["RawData"]["value"]["players"]]:
                    group_id = group_data["value"]["RawData"]["value"]['group_id']
                    guild_items_json = group_data["value"]["RawData"]["value"]["individual_character_handle_ids"]
                    break
        if group_id is None:
            messagebox.showerror(message='Guild ID not found, aboorting')
            return
        guild_item_instances = set()
        for guild_item in guild_items_json:
            guild_item_instances.add(guild_item['instance_id'])
    else:
        for group_idx, group_data in enumerate(targ_lvl["GroupSaveDataMap"]["value"]):
            if group_data["value"]["GroupType"]["value"]["value"] == "EPalGroupType::Guild" and group_data["key"] not in source_guild_dict:
                new_character_guild_found = False
                for player_idx, player_item in enumerate(group_data["value"]["RawData"]["value"]["players"]):
                    if player_item['player_uid'] == targ_uid:
                        new_character_guild_found = True
                        break
                if new_character_guild_found:
                    group_data["value"]["RawData"]["value"]["players"].pop(player_idx)
                    if len(group_data["value"]["RawData"]["value"]["players"]) > 0: 
                        if group_data["value"]["RawData"]["value"]["admin_player_uid"] == targ_uid:
                            group_data["value"]["RawData"]["value"]["admin_player_uid"] = group_data["value"]["RawData"]["value"]["players"][0]['player_uid']
                        for handle_idx, character_handle_id in enumerate(group_data["value"]["RawData"]["value"]["individual_character_handle_ids"]):
                            if character_handle_id['guid'] == targ_uid:
                                group_data["value"]["RawData"]["value"]["individual_character_handle_ids"].pop(handle_idx)
                    else:
                        targ_lvl["GroupSaveDataMap"]["value"].pop(group_idx)
                    break
        for group_data in targ_lvl["GroupSaveDataMap"]["value"]:
            if group_data["key"] in source_guild_dict:
                old_player_found = False
                for player_item in group_data["value"]["RawData"]["value"]["players"]:
                    if player_item['player_uid'] == host_guid:
                        old_player_found = True
                        player_item['player_uid'] = targ_uid
                        break
                if old_player_found:
                    for character_handle_id in group_data["value"]["RawData"]["value"]["individual_character_handle_ids"]:
                        if character_handle_id['guid'] == host_guid:
                            character_handle_id['guid'] = targ_uid
                            character_handle_id['instance_id'] = char_instanceid
                            break
                    if group_data["value"]["RawData"]["value"]["admin_player_uid"] == host_guid:
                        group_data["value"]["RawData"]["value"]["admin_player_uid"] = targ_uid
                    group_id = group_data["key"]
                    break
        if group_id is None:
            print("No old guild containing the source player is found in target, moving guilds from old world now...")
            old_guild = None
            for group_data in source_guild_dict.values():
                for player_item in group_data["value"]["RawData"]["value"]["players"]:
                    if player_item['player_uid'] == host_guid:
                        old_guild = fast_deepcopy(group_data)
                        break
            if old_guild is None:
                print("No guild containing the source player is found in the source either, either this is a bug or the files are corrupted. Aborting.")
                messagebox.showerror(message="No guild containing the source player is found in the source either, either this is a bug or the files are corrupted. Aborting.")
                return
            group_id = old_guild["key"]
            if old_guild["value"]["RawData"]["value"]["admin_player_uid"] == host_guid:
                old_guild["value"]["RawData"]["value"]["admin_player_uid"] = targ_uid
            for player_item in old_guild["value"]["RawData"]["value"]["players"]:
                if player_item['player_uid'] == host_guid:
                    player_item['player_uid'] = targ_uid
                    break
            for character_handle_id in old_guild["value"]["RawData"]["value"]["individual_character_handle_ids"]:
                if character_handle_id['guid'] == host_guid:
                    character_handle_id['guid'] = targ_uid
                    character_handle_id['instance_id'] = char_instanceid
                    break
            targ_lvl["GroupSaveDataMap"]["value"].append(old_guild)
    for pal_param in param_maps:
        pal_data = pal_param['value']['RawData']['value']
        slot_id_idx = pal_data.find(b'\x07\x00\x00\x00SlotID\x00\x0f\x00\x00\x00StructProperty\x00')
        if slot_id_idx == -1: continue
        pal_container_id_bytes = pal_data[slot_id_idx + 217:slot_id_idx + 233]
        pal_data_bytearray = bytearray(pal_data)
        if pal_container_id_bytes == host_inv_pals["value"]["ID"]["value"]:
            pal_data_bytearray[slot_id_idx + 217:slot_id_idx + 233] = inv_pals["value"]["ID"]["value"]
        elif pal_container_id_bytes == host_inv_otomo["value"]["ID"]["value"]:
            pal_data_bytearray[slot_id_idx + 217:slot_id_idx + 233] = inv_otomo["value"]["ID"]["value"]
        player_uid_start_idx = pal_data.find(OwnerPlayerUIdSearchPrefix) + len(OwnerPlayerUIdSearchPrefix)
        pal_data_bytearray[player_uid_start_idx:player_uid_start_idx + 16] = targ_uid
        pal_data_bytearray[-16:] = group_id
        pal_param['value']['RawData']['value'] = bytes(pal_data_bytearray)
        if not keep_old_guild_id and pal_param["key"]["InstanceId"]["value"] not in guild_item_instances:
            guild_items_json.append(
                {"guid": pal_param["key"]["PlayerUId"]["value"],
                 "instance_id": pal_param["key"]["InstanceId"]["value"]})
    new_character_save_param_map = []
    removed = 0
    for entity in targ_lvl["CharacterSaveParameterMap"]["value"]:
        if find_id_match_prefix(entity['value']['RawData']['value'], OwnerPlayerUIdSearchPrefix) == targ_uid:
            removed += 1
            continue
        new_character_save_param_map.append(entity)
    new_character_save_param_map += param_maps
    targ_lvl["CharacterSaveParameterMap"]["value"] = new_character_save_param_map
    print(f"Removed {removed} pals from the original character in the target world")
    print(f"Appended {len(param_maps)} pals of data from the source character")
    count = 0    
    for container in targ_lvl["CharacterContainerSaveData"]["value"]:
        container_id = container["key"]["ID"]["value"]
        if container_id == inv_pals["value"]["ID"]["value"]:
            target_slot_data = container['value']['Slots']['value']
            source_slot_data = host_pals['value']['Slots']['value']            
            container['value']['Slots']['value'] = source_slot_data                      
            count += 1
        elif container_id == inv_otomo["value"]["ID"]["value"]:
            target_slot_data = container['value']['Slots']['value']
            source_slot_data = host_otomo['value']['Slots']['value']
            container['value']['Slots']['value'] = source_slot_data                  
            count += 1            
        if count >= 2:
            print("Found all pal containers")
            break
    for container in targ_lvl["ItemContainerSaveData"]["value"]:
        container_id = container["key"]["ID"]["value"]
        if container_id == inv_main["value"]["ID"]["value"]:
            print("Found main inventory in target")
            container["value"] = host_main["value"]
            count += 1
        elif container_id == inv_key["value"]["ID"]["value"]:
            print("Found key inventory in target")
            container["value"] = host_key["value"]
            count += 1
        elif container_id == inv_weps["value"]["ID"]["value"]:
            print("Found weapon inventory in target")
            container["value"] = host_weps["value"]
            count += 1
        elif container_id == inv_armor["value"]["ID"]["value"]:
            print("Found armor inventory in target")
            container["value"] = host_armor["value"]
            count += 1
        elif container_id == inv_foodbag["value"]["ID"]["value"]:
            print("Found food bag inventory in target")
            container["value"] = host_foodbag["value"]
            count += 1
        if count >= expected_containers:
            print("Found all target containers")
            break
    target_dynamic_containers = targ_lvl['DynamicItemSaveData']['value']['values']
    repeated_indices = set()
    for i, target_dynamic_container in enumerate(target_dynamic_containers):
            target_container_id = target_dynamic_container.get('ID')
            if target_container_id is None:
                continue
            print("found value in target dynamic_container")
            target_guid = find_id_match_prefix(target_container_id['value'], LocalIdSearchPrefix)
            if target_guid in dynamic_guids:
                for j, (dynamic_container, container_local_id) in enumerate(level_additional_dynamic_containers):
                    if target_guid == container_local_id:
                        target_dynamic_containers[i] = dynamic_container
                        repeated_indices.add(j)
                        break
    targ_lvl['DynamicItemSaveData']['value']['values'] += [container for i, (container, local_id) in enumerate(level_additional_dynamic_containers) if i not in repeated_indices]
    print("Transferred all Dynamic containers, writing to output...")
    WORLDSAVESIZEPREFIX = b'\x0e\x00\x00\x00worldSaveData\x00\x0f\x00\x00\x00StructProperty\x00'
    size_idx = target_raw_gvas.find(WORLDSAVESIZEPREFIX) + len(WORLDSAVESIZEPREFIX)
    output_data = SkipFArchiveWriter(custom_properties=PALWORLD_CUSTOM_PROPERTIES).write_sections(targ_lvl, target_section_ranges, target_raw_gvas, size_idx)
    targ_json_gvas.properties = targ_json
    t_host_sav_path = os.path.join(os.path.dirname(t_level_sav_path), 'Players', selected_target_player + '.sav')
    if not os.path.exists(t_host_sav_path): t_host_sav_path = os.path.join(os.path.dirname(t_level_sav_path), '../Players', selected_target_player + '.sav')
    parent_directory = os.path.dirname(t_level_sav_path)
    backup_folder = "Backups/Character Transfer"
    backup_whole_directory(parent_directory, backup_folder)
    print("Writing to file...")
    gvas_to_sav(t_level_sav_path, output_data)
    gvas_to_sav(t_host_sav_path, targ_json_gvas.write())
    print("Saved all data successfully. PLEASE DON'T BREAK")
    messagebox.showinfo(message='Transfer finished! You may continue transferring more players or close the windows now.')
def sav_to_gvas(file):
    with open(file, 'rb') as f:
        data = f.read()
        raw_gvas, save_type, cnk_header = decompress_sav_to_gvas(data)
    return raw_gvas, save_type
def gvas_to_sav(file, gvas_data):
    sav_file_data = compress_gvas_to_sav(gvas_data, target_save_type)
    with open(file, 'wb') as out:
        out.write(sav_file_data)
def select_file():
    return filedialog.askopenfilename(filetypes=[("Palworld Saves", "*.sav *.json")])
def ishex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False
def load_file(path):
    global status_label, root
    loaded_file, save_type = None, None
    if path.endswith(".sav"):
        loaded_file, save_type = sav_to_gvas(path)
    return loaded_file, save_type
def load_player_file(level_sav_path, player_uid):
    player_file_path = os.path.join(os.path.dirname(level_sav_path), 'Players', player_uid + '.sav')
    if not os.path.exists(player_file_path):
        player_file_path = os.path.join(os.path.dirname(level_sav_path), '../Players', player_uid + '.sav')
        if not os.path.exists(player_file_path):
            messagebox.showerror(message=f"Player file {player_file_path} not present")
            return None
    raw_gvas, _ = load_file(player_file_path)
    if not raw_gvas:
        messagebox.showerror(message=f"Invalid file {player_file_path}")
        return
    return SkipGvasFile.read(raw_gvas)
def load_players(save_json, is_source):
    guild_dict = source_guild_dict if is_source else target_guild_dict
    if len(guild_dict) > 0:
        guild_dict.clear()
    players = dict()
    for group_data in save_json["GroupSaveDataMap"]["value"]:
        if group_data["value"]["GroupType"]["value"]["value"] == "EPalGroupType::Guild":
            group_id = group_data["value"]["RawData"]["value"]['group_id']
            players[group_id] = group_data["value"]["RawData"]["value"]["players"]
            guild_dict[group_id] = group_data
    list_box = source_player_list if is_source else target_player_list
    for item in list_box.get_children():
        list_box.delete(item)
    for guild_id, player_items in players.items():
        for player_item in player_items:
            playerUId = ''.join(str(UUID(player_item['player_uid'])).split('-')).upper()
            list_box.insert('', tk.END, values=(UUID(guild_id), playerUId, player_item['player_info']['player_name']))
def load_all_source_sections_async(group_save_section, reader):
    global level_json
    level_json, _ = reader.load_sections([
        ('CharacterSaveParameterMap', MAP_START),
        ('ItemContainerSaveData', MAP_START),
        ('DynamicItemSaveData', ARRAY_START),
        ('CharacterContainerSaveData', MAP_START)],
        path='.worldSaveData')
    level_json.update(group_save_section)
def source_level_file():
    global level_sav_path, source_level_path_label, level_json, selected_source_player, source_section_load_handle
    tmp = select_file()
    if tmp:
        if not tmp.endswith('.sav'):
            messagebox.showerror("Incorrect file", "This is not the right file. Please select *.sav file.")
            return
        raw_gvas, _ = load_file(tmp)
        if not raw_gvas:
            messagebox.showerror(message="Invalid files, files must be .sav")
            return
        reader = SkipFArchiveReader(raw_gvas, PALWORLD_TYPE_HINTS, PALWORLD_CUSTOM_PROPERTIES)
        group_save_section, _ = reader.load_section('GroupSaveDataMap', MAP_START, reverse=True)
        source_section_load_handle = threading.Thread(target=load_all_source_sections_async, args=(group_save_section, reader))
        source_section_load_handle.start()
        load_players(group_save_section, True)
        source_level_path_label.config(text=tmp)
        level_sav_path = tmp
        selected_source_player = None
        current_selection_label.config(text=f"Source: {selected_source_player}, Target: {selected_target_player}")
def load_all_target_sections_async(group_save_section, group_save_section_range, reader):
    global targ_lvl, target_section_ranges
    targ_lvl, target_section_ranges = reader.load_sections([
        ('CharacterSaveParameterMap', MAP_START),
        ('ItemContainerSaveData', MAP_START),
        ('DynamicItemSaveData', ARRAY_START),
        ('CharacterContainerSaveData', MAP_START)],
        path='.worldSaveData')
    targ_lvl.update(group_save_section)
    target_section_ranges.append(group_save_section_range)
def target_level_file():
    global t_level_sav_path, target_level_path_label, targ_lvl, target_level_cache, target_section_ranges, target_raw_gvas, target_save_type, selected_target_player, target_section_load_handle, TARGET_CNK_DATA_HEADER
    tmp = select_file()
    if tmp:
        if not tmp.endswith('.sav'):
            messagebox.showerror("Incorrect file", "This is not the right file. Please select *.sav file.")
            return
        raw_gvas, target_save_type = load_file(tmp)
        if not raw_gvas:
            messagebox.showerror(message="Invalid files, files must be .sav")
            return
        target_raw_gvas = raw_gvas
        reader = SkipFArchiveReader(raw_gvas, PALWORLD_TYPE_HINTS, PALWORLD_CUSTOM_PROPERTIES)
        group_save_section, group_save_section_range = reader.load_section('GroupSaveDataMap', MAP_START, reverse=True)
        target_section_load_handle = threading.Thread(target=load_all_target_sections_async, args=(group_save_section, group_save_section_range, reader))
        target_section_load_handle.start()
        load_players(group_save_section, False)
        target_level_path_label.config(text=tmp)
        t_level_sav_path = tmp
        selected_target_player = None
        current_selection_label.config(text=f"Source: {selected_source_player}, Target: {selected_target_player}")
def on_exit():
    global level_sav_path, host_sav_path, t_level_sav_path, t_host_sav_path
    root.destroy() 
def on_selection_of_source_player(event):
    global selected_source_player
    selections = source_player_list.selection()
    if len(selections):
        selected_source_player = source_player_list.item(selections[0])['values'][1]
        current_selection_label.config(text=f"Source: {selected_source_player}, Target: {selected_target_player}")
def on_selection_of_target_player(event):
    global selected_target_player
    selections = target_player_list.selection()
    if len(selections):
        selected_target_player = target_player_list.item(selections[0])['values'][1]
        current_selection_label.config(text=f"Source: {selected_source_player}, Target: {selected_target_player}")
def on_keep_old_guild_check():
    global keep_old_guild_id
    keep_old_guild_id = bool(checkbox_var.get())
    print("Keep old guild id after transfer:", "on" if keep_old_guild_id else "off")
    checkbox_var.set(1 if keep_old_guild_id else 0)
def create_label(text, row, column):
    return tk.Label(root, text=text, bg="#2f2f2f", fg="white", wraplength=600)
def sort_treeview_column(treeview, col_index, reverse):
    data = [(treeview.set(child, col_index), child) for child in treeview.get_children('')]
    data.sort(reverse=reverse, key=lambda x: x[0])
    for index, (_, item) in enumerate(data): treeview.move(item, '', index)
    treeview.heading(col_index, command=lambda: sort_treeview_column(treeview, col_index, not reverse))
def filter_treeview(tree, query):
    query = query.lower()
    if not hasattr(filter_treeview, "original_rows"):
        filter_treeview.original_rows = [row for row in tree.get_children()]
    for row in filter_treeview.original_rows:
        tree.reattach(row, '', 'end')
    for row in tree.get_children():
        values = tree.item(row, "values")
        if any(query in str(value).lower() for value in values):
            tree.reattach(row, '', 'end')
        else:
            tree.detach(row)
level_sav_path, host_sav_path, t_level_sav_path, t_host_sav_path = None, None, None, None
level_json, host_json, targ_lvl, targ_json = None, None, None, None
target_section_ranges, target_save_type, target_raw_gvas, targ_json_gvas = None, None, None, None
selected_source_player, selected_target_player = None, None
keep_old_guild_id, output_old_save_version = False, False
TARGET_CNK_DATA_HEADER = None
source_guild_dict, target_guild_dict = dict(), dict()
source_section_load_handle, target_section_load_handle = None, None
root = tk.Tk()
root.title(f"Character Transfer")
root.geometry("")
root.minsize("800", "300")
root.iconbitmap(os.path.join(os.path.dirname(__file__), 'resources', 'pal.ico'))
root.config(bg="#2f2f2f")
root.tk_setPalette(background="#2f2f2f", foreground="white")
font_style = ("Arial", 10)
heading_font = ("Arial", 12, "bold")
status_label = tk.Label(root, text="", font=font_style, bg="#2f2f2f", fg="white")
status_label.grid(row=0, column=0, columnspan=2, pady=20, sticky="ew")
root.columnconfigure(0, weight=3)
root.columnconfigure(1, weight=1)
root.rowconfigure(3, weight=1)
root.rowconfigure(5, weight=1)
source_search_var = tk.StringVar()
source_search_entry = tk.Entry(root, textvariable=source_search_var, font=font_style, bg="#444", fg="white", insertbackground="white")
source_search_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
source_search_var.trace_add("write", lambda *args: filter_treeview(source_player_list, source_search_var.get()))
target_search_var = tk.StringVar()
target_search_entry = tk.Entry(root, textvariable=target_search_var, font=font_style, bg="#444", fg="white", insertbackground="white")
target_search_entry.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
target_search_var.trace_add("write", lambda *args: filter_treeview(target_player_list, target_search_var.get()))
tk.Button(root, text='Select Source Level File', command=source_level_file).grid(row=2, column=1, padx=10, pady=20, sticky="ew")
source_level_path_label = tk.Label(root, text="Please select a file:", font=font_style, bg="#2f2f2f", fg="white", wraplength=600)
source_level_path_label.grid(row=2, column=0, padx=10, pady=20, sticky="ew")
style = ttk.Style()
style.theme_use('clam')
style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#444444", foreground="white")
style.configure("Treeview", background="#333333", foreground="white", rowheight=25, fieldbackground="#333333", borderwidth=0)
source_player_list = ttk.Treeview(root, columns=(0, 1, 2), show='headings', style="Treeview")
source_player_list.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')
source_player_list.tag_configure("even", background="#333333", foreground="white")
source_player_list.tag_configure("odd", background="#444444", foreground="white")
source_player_list.tag_configure("selected", background="#555555", foreground="white")
source_player_list.column(0, anchor='center')
source_player_list.column(1, anchor='center')
source_player_list.column(2, anchor='center')
source_player_list.heading(0, text='Guild ID', command=lambda: sort_treeview_column(source_player_list, 0, False))
source_player_list.heading(1, text='Player UID', command=lambda: sort_treeview_column(source_player_list, 1, False))
source_player_list.heading(2, text='Nickname', command=lambda: sort_treeview_column(source_player_list, 2, False))
source_player_list.column(0, width=100)
source_player_list.column(1, width=100)
source_player_list.column(2, width=100)
source_player_list.bind('<<TreeviewSelect>>', on_selection_of_source_player)
tk.Button(root, text='Select Target Level File', command=target_level_file).grid(row=4, column=1, padx=10, pady=20, sticky="ew")
target_level_path_label = tk.Label(root, text="Please select a file:", font=font_style, bg="#2f2f2f", fg="white", wraplength=600)
target_level_path_label.grid(row=4, column=0, padx=10, pady=20, sticky="ew")
target_player_list = ttk.Treeview(root, columns=(0, 1, 2), show='headings', style="Treeview")
target_player_list.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')
target_player_list.tag_configure("even", background="#333333", foreground="white")
target_player_list.tag_configure("odd", background="#444444", foreground="white")
target_player_list.tag_configure("selected", background="#555555", foreground="white")
target_player_list.column(0, anchor='center')
target_player_list.column(1, anchor='center')
target_player_list.column(2, anchor='center')
target_player_list.heading(0, text='Guild ID', command=lambda: sort_treeview_column(target_player_list, 0, False))
target_player_list.heading(1, text='Player UID', command=lambda: sort_treeview_column(target_player_list, 1, False))
target_player_list.heading(2, text='Nickname', command=lambda: sort_treeview_column(target_player_list, 2, False))
target_player_list.column(0, width=100)
target_player_list.column(1, width=100)
target_player_list.column(2, width=100)
target_player_list.bind('<<TreeviewSelect>>', on_selection_of_target_player)
current_selection_label = tk.Label(root, text=f"Source: N/A, Target: N/A", font=font_style, bg="#2f2f2f", fg="white", wraplength=600)
current_selection_label.grid(row=7, column=0, padx=10, pady=20, sticky="ew")
tk.Button(root, text='Start Transfer!', font=font_style, command=main).grid(row=7, column=1, padx=10, pady=20, sticky="ew")
checkbox_var = tk.IntVar()
keep_old_guild_check = tk.Checkbutton(
    root, 
    text="Keep old Guild ID after Transfer", 
    variable=checkbox_var, 
    command=on_keep_old_guild_check,
    indicatoron=True,
    selectcolor="#2f2f2f",
    activebackground="black",
    activeforeground="white",
    foreground="white", 
    bg="#2f2f2f"
)
keep_old_guild_check.grid(row=8, column=0, columnspan=2, sticky='w', padx=10, pady=5)
root.protocol("WM_DELETE_WINDOW", on_exit)
root.mainloop()