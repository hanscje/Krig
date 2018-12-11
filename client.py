from network import StreamSocket

data = "Hello there, server!"
sockSend = StreamSocket(True)
sockSend.connect("localhost", 5051)
sockSend.send_data(data.encode('ascii'), len(data))
sockSend.close()