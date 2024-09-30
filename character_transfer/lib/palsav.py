import zlib
# from isal import isal_zlib as zlib


def decompress_sav_to_gvas(data: bytes) -> tuple[bytes, int]:
    uncompressed_len = int.from_bytes(data[0:4], byteorder="little")
    compressed_len = int.from_bytes(data[4:8], byteorder="little")
    magic_bytes = data[8:11]
    save_type = data[11]
    data_start_offset = 12
    # Check for magic bytes
    if magic_bytes == b"CNK":
        uncompressed_len = int.from_bytes(data[12:16], byteorder="little")
        compressed_len = int.from_bytes(data[16:20], byteorder="little")
        magic_bytes = data[20:23]
        save_type = data[23]
        data_start_offset = 24
    if magic_bytes != b"PlZ":
        raise Exception(
            f"not a compressed Palworld save, found {magic_bytes} instead of P1Z"
        )
    # Valid save types
    if save_type not in [0x30, 0x31, 0x32]:
        raise Exception(f"unknown save type: {save_type}")
    # We only have 0x31 (single zlib) and 0x32 (double zlib) saves
    if save_type not in [0x31, 0x32]:
        raise Exception(f"unhandled compression type: {save_type}")
    if save_type == 0x31:
        # Check if the compressed length is correct
        if compressed_len != len(data) - data_start_offset:
            raise Exception(f"incorrect compressed length: {compressed_len}")
    # Decompress file
    uncompressed_data = zlib.decompress(data[data_start_offset:])
    if save_type == 0x32:
        # Check if the compressed length is correct
        if compressed_len != len(uncompressed_data):
            raise Exception(f"incorrect compressed length: {compressed_len}")
        # Decompress file
        uncompressed_data = zlib.decompress(uncompressed_data)
    # Check if the uncompressed length is correct
    if uncompressed_len != len(uncompressed_data):
        raise Exception(f"incorrect uncompressed length: {uncompressed_len}")

    return uncompressed_data, save_type, data[:12]


def compress_gvas_to_sav(data: bytes, save_type: int, cnk_header=None) -> bytes:
    uncompressed_len = len(data)
    compressed_data = zlib.compress(data)
    compressed_len = len(compressed_data)
    if save_type == 0x32:
        compressed_data = zlib.compress(compressed_data)

    # Create a byte array and append the necessary information
    result = bytearray()
    if cnk_header:
        result.extend(cnk_header)
    result.extend(uncompressed_len.to_bytes(4, byteorder="little"))
    result.extend(compressed_len.to_bytes(4, byteorder="little"))
    result.extend(b"PlZ")
    result.extend(bytes([save_type]))
    result.extend(compressed_data)

    return bytes(result)
