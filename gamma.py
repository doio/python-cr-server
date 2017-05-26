import socket
import sys
import zlib
import time

server_address = ('gcrs.private-gamers.com', 9339)
mock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Connecting to server",server_address[0],'on port',server_address[1])
mock.connect(server_address)
print('Connected to server!')

while 1:
    
    message = 
    try:
        mock.sendall(message)
    except:
        print('ERROR: there was a problem connecting to the server!')
        print('Kill in 15 seconds...')
        time.sleep(15)
        quit()
    print('Message Sent. Awaiting Response.')
    data = mock.recv(4096)
    zdata = str(data)[2:-1]
    sresp = zdata
