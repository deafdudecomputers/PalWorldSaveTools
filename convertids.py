from internal_libs.import_libs import *
def steamIdToPlayerUid(steam_id):
    encoded_id = str(steam_id).encode("utf-16-le")
    hash_value = CityHash64(encoded_id)
    u32 = lambda x: x & 0xFFFFFFFF
    combined_hash = u32(u32(hash_value) + (hash_value >> 32) * 23)
    uid_bytes = struct.pack('<I', combined_hash) + b"\x00" * 12
    return uuid.UUID(bytes=uid_bytes)
steam_input = input("Enter Steam ID (with or without 'steam_'): ")
if steam_input.startswith("steam_"):
    steam_input = steam_input[6:]
try:
    steam_id = int(steam_input)
    palworld_uid = steamIdToPlayerUid(steam_id)
    print("Palworld UID:", palworld_uid)
except ValueError:
    print("Invalid Steam ID entered. Please provide a valid number.")