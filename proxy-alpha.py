import socket
import threading
import struct
import os
import uuid
import random

def randomBytes(n):
    return bytes(random.getrandbits(8) for i in range(n))
    
gl_server_address = ('gcrs.private-gamers.com', 9339)
mock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("[INFO] Proxy =><= Server Connecting to",gl_server_address[0],'on port',gl_server_address[1])
mock.connect(gl_server_address)
print('[INFO] Proxy =><= Server Connected')
class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        print('[OK] Proxy Running')
    def listen(self):
        self.sock.listen(5)
        while True:
            print('[INFO] Proxy Listening')
            client, address = self.sock.accept()
            print('[INFO] Client =>Proxy Client', address, 'connected')
            client.settimeout(60) #10 second timeout
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        while True:
            try:
                print('[STATUS] Client => Proxy Waiting\r\n')
                data = client.recv(4098)
                message_id = int(str(struct.unpack('>H', data[:2]))[1:-2])
                print('[OK] Client => Proxy', message_id)
                if 1:
                    fmessage = data
                    try:
                        mock.sendall(fmessage)
                    except:
                        print('ERROR: there was a problem connecting to the server!')
                        print('Kill in 15 seconds...')
                        time.sleep(15)
                        quit()
                    print('[OK] Proxy => Server', message_id)
                    
                    while 1:
                        ndata=None
                        ndata = mock.recv(10086)
                        if not ndata:
                            print('[WARNING] Proxy ndata is empty')
                            break
                        lmessage_id = int(str(struct.unpack('>H', ndata[:2]))[1:-2])
                        print('[OK] Server => Proxy', lmessage_id)
                        response = ndata
                        cres = client.send(response)
                        if cres:
                            print('[OK] Proxy => Client', lmessage_id)
            except:
                client.close()
                return False

if __name__ == "__main__":
    port_num = 9339
    print('[INFO] Proxy Starting on port', port_num)
    ThreadedServer('0.0.0.0',port_num).listen()
