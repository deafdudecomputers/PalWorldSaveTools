import zlib
MAGIC_BYTES = b'PlZ'
def decompress_sav_to_gvas(data: bytes) -> tuple[bytes, int, bytes]:
    uncompressed_len = int.from_bytes(data[0:4], byteorder="little")
    compressed_len = int.from_bytes(data[4:8], byteorder="little")
    magic_bytes = data[8:11]
    save_type = data[11]
    data_start_offset = 12
    if magic_bytes == b"CNK":
        uncompressed_len = int.from_bytes(data[12:16], byteorder="little")
        compressed_len = int.from_bytes(data[16:20], byteorder="little")
        magic_bytes = data[20:23]
        save_type = data[23]
        data_start_offset = 24
    if magic_bytes != MAGIC_BYTES:
        raise Exception(f"Not a compressed Palworld save, found {magic_bytes} instead of {MAGIC_BYTES}")
    if save_type not in [0x30, 0x31, 0x32]:
        raise Exception(f"Unknown save type: {save_type}")
    try:
        if save_type == 0x31:
            if compressed_len != len(data) - data_start_offset:
                raise Exception(f"Incorrect compressed length: {compressed_len}")
            uncompressed_data = zlib.decompress(data[data_start_offset:])
        elif save_type == 0x32:
            first_decompressed = zlib.decompress(data[data_start_offset:])
            if compressed_len != len(first_decompressed):
                raise Exception(f"Incorrect compressed length after first decompression: {compressed_len}")
            uncompressed_data = zlib.decompress(first_decompressed)
        else:
            raise Exception(f"Unhandled compression type: {save_type}")
        if uncompressed_len != len(uncompressed_data):
            raise Exception(f"Incorrect uncompressed length: {uncompressed_len}")
        return uncompressed_data, save_type, data[:data_start_offset]
    except Exception as e:
        print(f"Exception encountered: {e}")
        raise
def compress_gvas_to_sav(data: bytes, save_type: int, cnk_header: bytes = None) -> bytes:
    uncompressed_len = len(data)
    compressed_data = zlib.compress(data)
    compressed_len = len(compressed_data)
    if save_type == 0x32:
        compressed_data = zlib.compress(compressed_data)
    result = bytearray()
    if cnk_header:
        result.extend(cnk_header)
    result.extend(uncompressed_len.to_bytes(4, byteorder="little"))
    result.extend(compressed_len.to_bytes(4, byteorder="little"))
    result.extend(MAGIC_BYTES)
    result.extend(bytes([save_type]))
    result.extend(compressed_data)
    return bytes(result)