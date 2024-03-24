from typing import Any
import json


class HTTPRequest:
    def __init__(
        self,
        headers: dict[str, Any],
        method: str,
        body: dict[str, Any],
        uri: str | None = None,
        http_version: bytes = b"1.1",
    ):
        # call self.parse() method to parse the request data
        self.headers: dict[str, Any] = headers
        self.method: str = method
        self.uri: str | None = uri
        self.http_version: bytes = http_version
        self.body = body

    @classmethod
    def new_request(cls, data: bytes) -> "HTTPRequest":
        headers, method, body, uri, http_version = cls.parse(data=data)
        return cls(
            headers=headers,
            method=method,
            body=body,
            uri=uri,
            http_version=http_version,
        )

    @staticmethod
    def parse(data: bytes) -> tuple[dict, str, dict, str | None, bytes]:
        lines: list[bytes] = data.split(b"\r\n")
        request_lines: bytes = lines[0]

        body = {}
        headers = {}
        for line in lines[1:]:
            if b":" in line:
                try:
                    body = json.loads(line.decode())
                except ValueError:
                    key, value = line.decode().split(": ")
                    headers[key] = value

        words: list[bytes] = request_lines.split(b" ")
        method: str = words[0].decode()  # call decode to convert bytes to str

        # we put this in an if-block because sometimes
        # browsers don't send uri for homepage
        if len(words) > 1:
            uri = words[1].decode()  # call decode to convert bytes to str
        else:
            uri = None

        if len(words) > 2:
            http_version = words[2]
        else:
            http_version = b"1.1"

        return headers, method, body, uri, http_version
