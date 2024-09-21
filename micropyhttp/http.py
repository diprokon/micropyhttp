from .utils import parse_query, http_codes


class HTTPRequest:
    def __init__(self, reader):
        self._reader = reader
        self.method = None
        self.path = None
        self.headers = {}
        self.query = {}
        self.proto = None

    async def read(self):
        request_line = await self._read_line()
        line = request_line.split()
        if len(request_line) == 0 or len(line) == 0:
            return
        self.method, path, self.proto = line
        path = path.split("?")
        self.path = path[0]
        if len(path) > 1:
            self.query = parse_query(path[1])
        self.headers = await self._read_headers()

    async def _read_headers(self):
        headers = {}
        while True:
            line = await self._read_line()
            if line == "":
                break
            key, value = line.split(": ")
            headers[key] = value
        return headers

    async def _read_line(self):
        line = await self._reader.readline()
        return line.decode().strip()


class HTTPResponse:
    def __init__(self, writer):
        self.writer = writer
        self.status = 200
        self.content_type = "text/html; charset=utf-8"
        self.headers = {}
        pass

    async def write(self, data):
        self.writer.write(data.encode('utf-8'))
        await self.writer.drain()

    async def done(self):
        try:
            await self.writer.aclose()
        except:
            try:
                self.writer.close()
            except:
                pass

    async def send_headers(self):
        await self.write(f"HTTP/1.0 {self.status} {http_codes[self.status]}\r\n")
        await self.write(f"Content-Type: {self.content_type}\r\n")
        for k, v in self.headers.items():
            await self.write(f"{k}: {v}\r\n")
        await self.write("\r\n")

    async def send(self, data=""):
        await self.send_headers()
        await self.write(data)
        await self.done()


class HTTPError(Exception):
    def __init__(self, error: Exception):
        self.message = str(error)
        self.status = 500


class HTTPNotFound(HTTPError):
    def __init__(self, path):
        super(HTTPNotFound, self).__init__(Exception("Not found: " + path))
        self.status = 404
