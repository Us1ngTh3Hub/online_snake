import socket
import checksum
import headercreator

# base class for client and server shared functions
class eudpyBase:
    def __init__(self, _ip, _port):
        self.ip = _ip
        self.port = _port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)

    def send(self, data):
        # encode message
        encoded_data = data.encode('utf-8')
        # generate header
        
        # generate checksum

        # construct data

        # split data if it is too big for single packet

        # transmit data
        return

    def receive(self, buffer):
        # receive message

        # check header

        # join data if it was split before

        # review checksum

        # decrypt data
        return

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
