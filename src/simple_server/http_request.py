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

        empty_idx_arr: list[int] = [i for i in range(len(lines)) if len(lines[i].decode()) == 0]
        if empty_idx_arr:
            empty_idx = empty_idx_arr[0]
        else:
            empty_idx = len(lines)

        body: dict[str, Any] = {}
        headers: dict[str, Any] = {}
        for line in lines[1:empty_idx]:
            if b":" in line:
                try:
                    key, value = line.decode().split(": ")
                    headers[key] = value
                except Exception:
                    ...

        if headers.get("Content-Type") == "application/json":
            raw_body_bytes: bytes = lines[empty_idx + 1]
            try:
                body.update(json.loads(raw_body_bytes.decode()))
            except Exception:
                ...

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
