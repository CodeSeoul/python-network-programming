from _socket import SOL_SOCKET, SO_REUSEADDR
from socket import socket, AF_INET, SOCK_STREAM


class TCPServer:
    recv_size: int = 8192

    def __init__(self, host: str = "127.0.0.1", port: int = 8888):
        self.host = host
        self.port = port

    def buffer_read(self, client_socket: socket):
        client_socket.setblocking(False)
        result = client_socket.recv(self.recv_size)
        buffering = True
        while buffering:
            try:
                more_data: bytes = client_socket.recv(self.recv_size)
                result += more_data
            except BlockingIOError:
                buffering = False
        return result

    def start(self):
        # create a socket object
        server = socket(AF_INET, SOCK_STREAM)
        server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        # bind the socket object to the address and port
        server.bind((self.host, self.port))
        # start listening for connections
        server.listen(5)

        print("Listening at", server.getsockname())

        while True:
            # accept any new connection
            client_socket, address = server.accept()
            print("Connected by", address)
            data: bytes = self.buffer_read(client_socket=client_socket)
            self.handle_request(data=data, client_socket=client_socket)
            # threading.Thread(
            #     target=self.handle_request,
            #     args=(data, connection),
            #     daemon=True
            # ).start()

    def handle_request(self, data: bytes, client_socket: socket):
        try:
            client_socket.sendall(data)
        except Exception as e:
            client_socket.sendall(str(e).encode("utf-8"))
        finally:
            client_socket.close()
