import socket
import threading
import struct
import os
import uuid
import random


global debugmode
debugmode = True
def debug(debmessage):
    if debmessage:
        if debugmode:
            print('[DEBUG]',debmessage)
        else:
            pass
    else:
        pass
def randomBytes(n):
    return bytes(random.getrandbits(8) for i in range(n))
def mockrcv():
    rdata = mock.recv(10086)
    if not rdata:
        return "nulldata"
    return rdata

def serverlisten(client):
    ndata=mockrcv()
    if(ndata=="nulldata"):
        print('[WARNING] Proxy ndata is empty')
        return False
    else:
        lmessage_id = int(str(struct.unpack('>H', ndata[:2]))[1:-2])
        print('[OK] Server => Proxy', lmessage_id)
        response = ndata
        cres = client.send(response)
        if cres:
            print('[OK] Proxy => Client', lmessage_id)
            return True
gl_server_address = ('54.245.151.83', 9339) #gcrs.private-gamers.com
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
            client, address = self.sock.accept()
            print('[INFO] Client =>Proxy Client', address, 'connected')
            client.settimeout(60) #second timeout
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        while True:
            data = client.recv(4098)
            try:
                message_id = int(str(struct.unpack('>H', data[:2]))[1:-2])
            except:
                message_id = 'Unknown Message'
            print('[OK] Client => Proxy', message_id)
            fmessage = data
            mock.sendall(fmessage)
            print('[OK] Proxy => Server', message_id)
            while 1:
                debug('Listening to server')
                r = serverlisten(client);
                if r == False:
                    debug('No data from the server')
                    break
                else:
                    debug('Data received from server')
                    break

if __name__ == "__main__":
    port_num = 9339
    print('[INFO] Proxy Starting on port', port_num)
    ThreadedServer('0.0.0.0',port_num).listen()
