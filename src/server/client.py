import socket
#import ipaddress
import headercreator

'''
Not used anymore but first iteration for the server.
Is not like the name implies a client but rather works a bit like a client would(the funktions do not form a working client for this application tho)
Problems:
-can only connect to certain ip
-need separate application for different clients
'''




class udpserver():
    def __init__(self, _ip = None, _port = None):
        self.connectionrequest = b'connection request'
        self.ip = _ip
        self.port = _port
        self.server_address = (self.ip, self.port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        self.sock.sendto(self.connectionrequest, self.server_address)

    def connect(self):
        counter = 0
        while(True):
            counter+=1
            data, address = self.sock.recvfrom(1024)
            header = headercreator.unpack_header(data[:8])
            if(data[8:] == self.connectionrequest):
                self.ip = address
                self.port = header[1]
                self.server_address = (self.ip, self.port)
                return
            if(counter >= 1000):
                return -1

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
        header = headercreator.unpack_header(data[:8])
        message = data[8:]
        #Recieve new data until its the supposed length
        while header[2] != len(message):
            data, address = self.sock.recvfrom(1024)
            message += data
        print("Received response:", message.decode('utf-8'))
        return message.decode('utf-8')

#splits byte string into parts of part_size
def split_into_fixed_parts(data, part_size):
    num_parts = (len(data) + part_size - 1) // part_size
    return [data[i*part_size:(i+1)*part_size] for i in range(num_parts)]
