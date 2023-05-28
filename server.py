import socket
#import ipaddress
import headercreator

class udpserver():
    
    def __init__(self, _ip, _port, _server):
        self.serverip = _server
        self.ip = _ip
        self.port = _port
        self.server_address = (_ip, _port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)

    def send(self, _message):
        encoded_message = _message.encode('utf-8')
        header = self.getheader(encoded_message)
        complete_message = header + encoded_message
        if(len(complete_message)>1024):
            for part in split_into_fixed_parts(complete_message,1024):
                self.sock.sendto(part, self.server_address)

        else:
            self.sock.sendto(complete_message, self.server_address)

    def getheader(self, encoded_message):
        len = len(encoded_message)
        summ = headercreator.calculate_checksum(encoded_message)
        return headercreator.create_udp_header(self.port, self.port, len, summ)

    def recieve(self):
        # Receive the response from the server
        data, address = self.sock.recvfrom(1024)
        print("Received response:", data.decode('utf-8'))


        return 1

#splits byte string into parts of part_size
def split_into_fixed_parts(data, part_size):
    num_parts = (len(data) + part_size - 1) // part_size
    return [data[i*part_size:(i+1)*part_size] for i in range(num_parts)]


