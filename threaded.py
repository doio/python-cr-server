import socket
import threading
import struct
import os
import uuid
import random

def randomBytes(n):
    return bytes(random.getrandbits(8) for i in range(n))

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        print('Server bound to port ', self.port)
    def listen(self):
        self.sock.listen(5)
        while True:
            print('Listening for new connections!')
            client, address = self.sock.accept()
            print('new connection from ', address, '!')
            client.settimeout(600) #10 minute timeout
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        size = 2048
        while True:
            try:
                print('\r\nWaiting for the Data to arrive from ', address)
                data = client.recv(size)
                message_id = int(str(struct.unpack('>H', data[:2]))[1:-2])
                content = {}
                if message_id == 10100:
                    content = {'protocol': int(str(struct.unpack('>I', data[7:11]))[1:-2]),
                           'keyVersion': int(str(struct.unpack('>I', data[11:15]))[1:-2]),
                           'majorVersion': int(str(struct.unpack('>I', data[15:19]))[1:-2]),
                           'minorVersion': int(str(struct.unpack('>I', data[19:23]))[1:-2]),
                           'build': int(str(struct.unpack('>I', data[23:27]))[1:-2]),
                           'contentHash': str(data[31:71])[2:],
                           'deviceType': int(str(struct.unpack('>I', data[71:75]))[1:-2]),
                           'appStore': int(str(struct.unpack('>I', data[75:79]))[1:-2]),
                    }
                    
                    resd = bytes(b'\x4e\x84\x00\x00\x1c\x00\x00\x00\x00\x00\x18\x62\xaf\x74\x94\x14\x06\xe5\x5a\x5e\x9a\x14\x13\x9c\xa9\xe4\x7f\x7e\x0a\xbd\xe5\xab\xfa\x74\x90')
                    #TO DO: send response.
                if message_id == 10101:
                    resd = data
                print('Got Data from ', address, ':\r\n', 'message-id: ', message_id,'\r\n')
                if content:
                    print(content)
                if data:
                    print('\r\nGenerated Response:\r\n', resd)
                    
                    response = resd
                    cres = client.send(response)
                    if cres:
                        print('sent: ', response)
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                return False

if __name__ == "__main__":
    port_num = 9339
    print('Starting server on port ', port_num)
    ThreadedServer('0.0.0.0',port_num).listen()
