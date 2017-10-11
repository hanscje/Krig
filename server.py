import socket

TCP_IP = '127.0.01'
TCP_PORT = 5050
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print('starting a war')

while 1:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    print("received data:", data)
    conn.send(data)
conn.close()



"""
class MySocket(object):

    def __init__(self, sock = None):
        if not sock:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        selc.sock.bind((TCP_IP, TCP_PORT))
        s.listen(1)
"""
