import eudpylib

ip_address = '10.5.0.2'
client = eudpylib.eudpyClient()

client.connect(ip_address, 54321)
print("connection established")

client.send("Hello server!")
print("packet sent")

data, address = client.receive
print(data)

client.close