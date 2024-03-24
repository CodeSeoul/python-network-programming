class HTTPResponse:
    headers: dict[str, str] = {
        "Server": "CrudeServer",
        "Content-Type": "text/html",
    }

    status_codes: dict[int, str] = {
        200: "OK",
        201: "Created",
        404: "Not Found",
        501: "Not Implemented",
    }

    blank_line: bytes = b"\r\n"

    def __init__(
        self,
        status_code: int,
        extra_headers: dict | None,
        response_body: bytes,
    ):
        self.status_code = status_code
        self.extra_headers = extra_headers
        self.response_body = response_body

    @classmethod
    def encode_to_response(
        cls,
        status_code: int,
        extra_headers: dict | None,
        response_body: bytes,
    ) -> bytes:
        temp = cls(
            status_code=status_code,
            extra_headers=extra_headers,
            response_body=response_body,
        )
        return temp.to_response()

    def to_response(self):
        response_line: bytes = self.get_response_line(status_code=self.status_code)
        response_headers: bytes = self.get_response_headers(extra_headers=self.extra_headers)
        return b"".join([response_line, response_headers, self.blank_line, self.response_body])

    def get_response_line(self, status_code) -> bytes:
        """Returns response line"""
        reason = self.status_codes[status_code]
        line = "HTTP/1.1 %s %s\r\n" % (status_code, reason)

        return line.encode()  # call encode to convert str to bytes

    def get_response_headers(self, extra_headers: dict | None = None) -> bytes:
        """Returns headers
        The `extra_headers` can be a dict for sending
        extra headers for the current response
        """
        headers_copy = self.headers.copy()  # make a local copy of headers

        if extra_headers:
            headers_copy.update(extra_headers)

        headers = ""

        for h in headers_copy:
            headers += "%s: %s\r\n" % (h, headers_copy[h])

        return headers.encode()  # call encode to convert str to bytes
