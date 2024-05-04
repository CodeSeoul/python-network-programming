from src.simple_server.http_server import HTTPServer
from src.simple_server.tcp_server import TCPServer


def main():
    print("hello world")


if __name__ == "__main__":
    server = HTTPServer()
    server.start()
