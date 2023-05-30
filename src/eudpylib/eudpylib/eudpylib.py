import socket
import checksum
import headercreator

# basic functions
def split_into_fixed_parts(data, part_size):
    num_parts = (len(data) + part_size - 1) // part_size
    return [data[i*part_size:(i+1)*part_size] for i in range(num_parts)]

# base class for client and server shared functions
class eudpyBase:
    def __init__(self):
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = 54321
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)

    def send(self, data):
        # encode message
        encoded_data = data.encode('utf-8')
        # generate checksum
        data_checksum = checksum.calculate_checksum(data)
        # generate header
        header = headercreator.create_udp_header(self.port, self.port, len(data), data_checksum)
        # construct data
        send_data = encoded_data + header
        # split data if it is too big for single packet
        if(len(send_data)>1024):
            for part in split_into_fixed_parts(send_data,1024):
                self.sock.sendto(part, self.server_address)
        else:
            # transmit data
            self.sock.sendto(send_data, self.server_address)

    def receive(self, buffer):
        # receive message
        data, address = self.sock.recvfrom(1024)
        header = headercreator.unpack_header(data[:8])
        message = data[8:]
        # check header
        while header[2] != len(message):
            # join data if it was split before
            data, address = self.sock.recvfrom(1024)
            # review checksum
            if header[3] != checksum.calculate_checksum(data):
                return -1
            message += data
        # decrypt data
        return message.decode('utf-8')

# class for client specific functions
class eudpyClient(eudpyBase):
    def __init__(self, _ip, _port):
        super().__init__(_ip, _port)
        
    def connect(self):
        # connect to server

        # send and receive test package
        return

    def close(self):        
        # close connection
        return

# class for server specific functions
class eudpyServer(eudpyBase):
    def __init__(self, _ip, _port):
        super().__init__(_ip, _port)
    
    def open(self):
        return
    
    def close(self):
        return
