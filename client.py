from network import StreamSocket, ClientSocket

data = "Hello there, server!"
sockSend = ClientSocket("localhost", 5051, True)
sockSend.send(data)
sockSend.close()