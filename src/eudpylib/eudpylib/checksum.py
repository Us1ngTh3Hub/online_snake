def calculate_checksum(message):
    checksum = 0

    for i in range(0, len(message), 2):
        # Get the current 16-bit chunk from the message
        chunk = (message[i] << 8) + message[i + 1]
        checksum += chunk

        # Wrap around if the sum exceeds 16 bits
        checksum = (checksum & 0xFFFF) + (checksum >> 16)

    # One's complement the checksum
    checksum = ~checksum & 0xFFFF

    return checksum