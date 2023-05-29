import socket

class eudpyBase:
    def __init__(self, _ip, _port):
        self.ip = _ip
        self.port = _port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)

    def send(self, data):
        return

    def receive(self, buffer):
        return

class eudpyClient(eudpyBase):
    def __init__(self, _ip, _port):
        super().__init__(_ip, _port)
        
    def connect(self):
        return

    def close(self):
        return

class eudpyServer(eudpyBase):
    def __init__(self, _ip, _port):
        super().__init__(_ip, _port)
    
    def open(self):
        return
    
    def close(self):
        return
