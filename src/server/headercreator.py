import struct

header_format = "!HHHH"  # Format string for the header fields

#will unpack the header bits to make them readable
def unpack_header(header_data):
    header = struct.unpack(header_format, header_data)
    return header

#will pack the header bits to send them
def create_udp_header(source_port, destination_port, length, checksum):
    # UDP header structure: 2 bytes for source port, 2 bytes for destination port,
    # 2 bytes for length, and 2 bytes for checksum
    udp_header = struct.pack(header_format, source_port, destination_port, length, checksum)
    return udp_header

#calculates checksum for the given message
def calculate_checksum(message):
    checksum = 0

    for i in range(0, len(message), 2):
        # Get the current 16-bit chunk from the message
        chunk = (message[i] << 8) + message[i + 1]
        checksum += chunk

        #Wrap around if the sum exceeds 16 bits (when adding new summs)
        checksum = (checksum & 0xFFFF) + (checksum >> 16)

    #makes sure the chesum has the right format
    checksum = ~checksum & 0xFFFF

    return checksum