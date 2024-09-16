import zlib

MAGIC_BYTES = b'PlZ'  # Adjust if necessary

def decompress_sav_to_gvas(data: bytes) -> tuple[bytes, int]:
    uncompressed_len = int.from_bytes(data[0:4], byteorder="little")
    compressed_len = int.from_bytes(data[4:8], byteorder="little")
    magic_bytes = data[8:11]
    save_type = data[11]
    data_start_offset = 12

    #print(f"Magic Bytes: {magic_bytes}")
    #print(f"Save Type: {save_type}")
    #print(f"Uncompressed Length: {uncompressed_len}")
    #print(f"Compressed Length: {compressed_len}")

    if magic_bytes != MAGIC_BYTES:
        if (
            magic_bytes == b"\x00\x00\x00"
            and uncompressed_len == 0
            and compressed_len == 0
        ):
            raise Exception(
                "Not a compressed Palworld save, found too many null bytes, this is likely corrupted"
            )
        raise Exception(
            f"Not a compressed Palworld save, found {magic_bytes!r} instead of {MAGIC_BYTES!r}"
        )

    try:
        if save_type == 0x31 or save_type == 49:  # Handle both 0x31 and 49
            if compressed_len != len(data) - data_start_offset:
                raise Exception(f"Incorrect compressed length: {compressed_len}")
            uncompressed_data = zlib.decompress(data[data_start_offset:])
            #print(f"Decompressed Data Length (0x31/49): {len(uncompressed_data)}")
        elif save_type == 0x32 or save_type == 50:  # Handle both 0x32 and 50
            uncompressed_data = zlib.decompress(data[data_start_offset:])
            if compressed_len != len(uncompressed_data):
                raise Exception(f"Incorrect compressed length after first decompression: {compressed_len}")
            # Decompress again if needed
            uncompressed_data = zlib.decompress(uncompressed_data)
            #print(f"Decompressed Data Length (0x32/50): {len(uncompressed_data)}")
        else:
            raise Exception(f"Unknown save type: {save_type}")

        if uncompressed_len != len(uncompressed_data):
            raise Exception(f"Incorrect uncompressed length: {uncompressed_len}")

        return uncompressed_data, save_type

    except Exception as e:
        print(f"Exception encountered: {e}")
        raise


def compress_gvas_to_sav(data: bytes, save_type: int) -> bytes:
    uncompressed_len = len(data)
    compressed_data = zlib.compress(data)
    compressed_len = len(compressed_data)
    if save_type == 0x32:
        compressed_data = zlib.compress(compressed_data)

    result = bytearray()
    result.extend(uncompressed_len.to_bytes(4, byteorder="little"))
    result.extend(compressed_len.to_bytes(4, byteorder="little"))
    result.extend(MAGIC_BYTES)
    result.extend(bytes([save_type]))
    result.extend(compressed_data)

    return bytes(result)
