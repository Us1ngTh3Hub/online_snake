import struct

header_format = "!HHHH"  # Format string for the header fields

def unpack_header(header_data):
    header = struct.unpack(header_format, header_data)
    return header

def create_udp_header(source_port, destination_port, length, checksum):
    # UDP header structure: 2 bytes for source port, 2 bytes for destination port,
    # 2 bytes for length, and 2 bytes for checksum
    udp_header = struct.pack(header_format, source_port, destination_port, length, checksum)
    return udp_header
