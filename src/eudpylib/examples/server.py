import eudpylib

server = eudpylib.eudpyServer()

if server.open() != -1:
    print("connection opened")

    data, address = server.receive()
    print("received packet")
    
    print(data)

    server.close