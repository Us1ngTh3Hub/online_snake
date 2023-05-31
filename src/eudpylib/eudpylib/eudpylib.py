import socket
import threading
import time
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
        self.connection_request = b'connection request'
        self.connection_confirmation = b'connection confirmation'
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)

    def send(self, data):
        # encode message
        encoded_data = data.encode('utf-8')
        # generate checksum
        data_checksum = checksum.calculate_checksum(encoded_data)
        # generate header
        packet_type = 0x02
        header = headercreator.create_udp_header(self.port, self.port, len(encoded_data), packet_type, data_checksum)
        # construct data
        send_data = header + encoded_data
        # split data if it is too big for single packet
        if(len(send_data)>1024):
            for part in split_into_fixed_parts(send_data,1024):
                self.socket.sendto(part, self.communication_socket_address)
        else:
            # transmit data
            self.socket.sendto(send_data, self.communication_socket_address)
        
    # function which tracks keep alive packet traffic
    def send_keep_alive_packet(self):
        # set keep alive data
        data = 0xFFFF
        encoded_data = data.encode('utf-8')
        # set packet type in Header
        packet_type = 0x01
        packet_checksum = checksum.calculate_checksum(data)
        header = headercreator.create_udp_header(self.port, self.port, 0, packet_type, packet_checksum)
        # construct packet
        send_data = header + encoded_data
        # send packet
        self.socket.send(send_data)
                
    # check if keep alive packet was received in given interval
    def check_keep_alive_packet_reception(self, interval):
        # last_received_time is automatically updated by normal receive function
        elapsed_time = time.time() - self.last_received_time if self.last_received_time else float('inf')
        if elapsed_time > interval: 
            self.close()
    
    def receive(self):
        # receive message
        data, address = self.sock.recvfrom(1024)
        header = headercreator.unpack_header(data[:8])
        # check header for packet type
        if header[3] == 0x01:
            self.last_received_time = time.time()
            return
        # save packet data field
        message = data[8:]
        # check header for split packet
        while header[2] != len(message):
            # join data if it was split before
            data, address = self.sock.recvfrom(1024)
            # review checksum
            if header[4] != checksum.calculate_checksum(data):
                return -1
            message += data
        # decrypt data
        return (message.decode('utf-8'), address)   
    
    def close(self):        
        # close connection
        self.socket.close()
        return

# class for client specific functions
class eudpyClient(eudpyBase):
    def __init__(self, _ip, _port):
        super().__init__(_ip, _port)
        
    def connect(self, server_host, server_port):
        # connect to server
        self.communication_socket_address = (server_host, server_port)
        self.socket.connect(self.communication_socket_address)
        # send connection request
        self.send(self.connection_request)
        data, address = self.receive()
        if data == self.connection_confirmation:
            return 1
        return 0

# class for server specific functions
class eudpyServer(eudpyBase):
    def __init__(self, _ip, _port):
        super().__init__(_ip, _port)
    
    def open(self):
        counter = 0
        while(True):
            counter+=1
            data, address = self.receive
            header = headercreator.unpack_header(data[:8])
            # check if packet is connection request
            if(data[8:] == self.connection_request):
                # save client address information
                self.client_ip = address
                self.client_port = header[1]
                self.communication_socket_address = (self.ip, self.port)
                # send confirmation packet
                self.send(self.connection_confirmation)
                return
            if(counter >= 1000):
                return -1