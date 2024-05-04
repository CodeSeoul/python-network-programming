import os
from socket import socket
from typing import Callable

from src.simple_server.http_request import HTTPRequest
from src.simple_server.http_response import HTTPResponse
from src.simple_server.tcp_server import TCPServer


class HTTPServer(TCPServer):
    @staticmethod
    def handle_get(request: HTTPRequest) -> bytes:
        assert request.uri is not None
        filename = request.uri.strip("/")  # remove the slash from the request URI

        path: str = f"{os.getcwd()}/files/{filename}"
        if os.path.exists(path):
            status_code = 200
            with open(path, "rb") as f:
                response_body = f.read()
        else:
            status_code = 404
            response_body = b"<h1>404 Not Found</h1>"

        return HTTPResponse.encode_to_response(
            status_code=status_code,
            extra_headers=None,
            response_body=response_body,
        )

    @staticmethod
    def handle_post(request: HTTPRequest) -> bytes:
        path: str = f"{os.getcwd()}/files/hello_{request.body['name'].lower()}.html"
        data = f"""
<html>
    <head>
        <title>Hello {request.body["name"]}</title>
    </head>
    <body>
        <h1>{request.body["name"]}'s page</h1>
        <p>{request.body["name"]} created a new post</p>
    </body>
</html>"""

        with open(path, "w+") as f:
            f.write(data.strip())
        return HTTPResponse.encode_to_response(
            status_code=201,
            extra_headers=None,
            response_body=data.strip().encode(),
        )

    @staticmethod
    def handle_501(request: HTTPRequest | None = None, error_message: str | None = None) -> bytes:
        status_code = 501

        response_body = f"<h1>501 Internal Server Error: {error_message}</h1>"

        return HTTPResponse.encode_to_response(
            status_code=status_code,
            extra_headers=None,
            response_body=response_body.encode(),
        )

    def get_handler(self, method: str) -> Callable:
        match method:
            case "GET":
                return self.handle_get
            case "POST":
                return self.handle_post
            case _:
                return self.handle_501

    def handle_request(self, data: bytes, client_socket: socket):
        try:
            # create an instance of `HTTPRequest`
            request = HTTPRequest.new_request(data=data)
            # now, look at the request method and call the
            # appropriate handler
            handler: Callable = self.get_handler(method=request.method)
            response: bytes = handler(request)
            client_socket.sendall(response)
        except Exception as e:  # TODO
            self.handle_501(error_message=str(e))
        finally:
            client_socket.close()
