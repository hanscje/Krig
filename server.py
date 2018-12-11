from network import StreamSocket

sockRecv = StreamSocket(True)
sockRecv.bind(5051)
newSock, addr = sockRecv.accept()
print("Accepted connection from ", addr)

receivedData = newSock.recv_data(20)
print(receivedData)

newSock.close()
sockRecv.close()