import socket
import pickle
import struct


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
        return b''.join(data)

    def dprint(self, fstr, *args):
        """
        Prints the input if the debug flag is set.
        """
        if self._debug:
            print(fstr, *args)


class ClientSocket(StreamSocket):

    def __init__(self, ip, port, debug=False, sock=None):
        """
        Initialize client to connect to the specified ip and port.
        """
        super().__init__(debug, sock)
        self.connect(ip, port)
    
    def send(self, data):
        """
        Send the data as a string.
        """
        payload = pickle.dumps(data)
        payload_len = int(len(payload))
        self.dprint("Sending payload of size ", payload_len)
        self.send_data(struct.pack("I", socket.htonl(payload_len)), 4)
        self.send_data(payload, payload_len)

    def connect(self, host, port):
        """
        Connect the socket to the specified host and port.
        """
        if host == "localhost" or host == "127.0.0.1":
            host = socket.gethostname()
        self._sock.connect((host, port))
        self._socket_inited = True
        self.dprint("StreamSocket: Connected to host ", host, "on port", port)


class ServerSocket(StreamSocket):

    def __init__(self, port, debug=False, sock=None):
        """
        Initialize server to listen to the specified port.
        """
        super().__init__(debug, sock)
        if port is not None:
            self.bind(port)

    def recv(self):
        """
        Receive data based on the length sent first.
        """
        data = struct.unpack("I", self._sock.recv(4))
        payload_len = socket.ntohl(data[0])
        self.dprint("Receiving payload of size ", payload_len)
        payload = pickle.loads(self.recv_data(payload_len))
        self.dprint("Data: ", payload)

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
        new_sock = ServerSocket(None, self._debug, accepted)
        new_sock._socket_inited = True
        self.dprint("StreamSocket: Accepted connect from ", client_address)
        return (new_sock, client_address)

        

if __name__ == "__main__":
    print("Running 'network.py' standalone...")
    port = 5054
    sockRecv = ServerSocket(True)
    sockRecv.bind(port)
    
    data = "Hello there, server!"
    sockSend = ClientSocket("localhost", port, True)
    newSock, addr = sockRecv.accept()

    #try:
    sockSend.send(data)

    receivedData = newSock.recv()
    print(receivedData)
    #except Exception as e:
    #    print(e)

    newSock.close()
    sockRecv.close()
    sockSend.close()
