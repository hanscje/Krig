from network import StreamSocket, ServerSocket

sockRecv = ServerSocket(5051, True)
newSock, addr = sockRecv.accept()
print("Accepted connection from ", addr)

receivedData = newSock.recv()
print(receivedData)

newSock.close()
sockRecv.close()