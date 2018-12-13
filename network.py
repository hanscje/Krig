import socket

class StreamSocket(object):

    def __init__(self, debug=False, sock=None):
        """
        Creates a new client or server socket.
        """
        if sock is None:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self._sock = sock
        
        self._debug = debug
        self._socket_inited = False
        
    def connect(self, host, port):
        """
        Connect the socket to the specified host and port.
        """
        if host == "localhost" or host == "127.0.0.1":
            host = socket.gethostname()
        self._sock.connect((host, port))
        self._socket_inited = True
        self.dprint("StreamSocket: Connected to host ", host, "on port", port)
    
    def bind(self, port):
        """
        Binds and listens to the specified port.
        """
        self._sock.bind((socket.gethostname(), port))
        self._sock.listen(5)
        self._socket_inited = True
        self.dprint("StreamSocket: Bound and listens to ", port, "with hostname",
            socket.gethostname())

    def accept(self):
        """
        Waits for a new connection to accept.
        """
        accepted, client_address = self._sock.accept()
        new_sock = StreamSocket(self._debug, accepted)
        new_sock._socket_inited = True
        self.dprint("StreamSocket: Accepted connect from ", client_address)
        return (new_sock, client_address)

    def close(self):
        """
        Closes the socket gracefully.
        """
        try:
            if self._socket_inited:
                self._sock.shutdown(1)
            self._sock.close()
        except:
            pass
        
        self._inited = False
        self.dprint("StreamSocket: Closing socket")

    def send_data(self, data, data_size):
        """
        Attempts to send 'data' if the socket is connected.
        """
        if self._socket_inited is False:
            raise RuntimeError("StreamSocket: Attempting to send data with uninitialized socket!")
        
        sent_total = 0
        while sent_total < data_size:
            sent = self._sock.send(data[sent_total:])
            if sent == 0:
                self.close()
                raise RuntimeError("StreamSocket: Connection broken while sending!")
            sent_total = sent_total + sent
        self.dprint("StreamSocket: Sent data of length ", data_size)

    def recv_data(self, data_size):
        """
        Attempts to receive data from the socket if connected.
        """
        if self._socket_inited is False:
            raise RuntimeError("StreamSocket: Attempting to receive data with uninitialized socket!")
        data = []
        received_total = 0
        while received_total < data_size:
            current_data = self._sock.recv(data_size - received_total)
            if current_data == b'':
                self.close()
                raise RuntimeError("StreamSocket: Connection broken while receiving!")
            data.append(current_data)
            received_total = received_total + len(current_data)
        self.dprint("StreamSocket: Received data of length ", received_total)
        return ''.join(str(data))

    def dprint(self, fstr, *args):
        """
        Prints the input if the debug flag is set.
        """
        if self._debug:
            print(fstr, *args)


if __name__ == "__main__":
    print("Running 'network.py' standalone...")
    port = 5054
    sockRecv = StreamSocket(True)
    sockRecv.bind(port)
    
    data = "Hello there, server!"
    sockSend = StreamSocket(True)
    sockSend.connect("localhost", port)
    newSock, addr = sockRecv.accept()

    #try:
    sockSend.send_data(data.encode('ascii'), len(data))

    receivedData = newSock.recv_data(len(data))
    print(receivedData)
    #except Exception as e:
    #    print(e)

    newSock.close()
    sockRecv.close()
    sockSend.close()
