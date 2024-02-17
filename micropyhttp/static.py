import sys
from os import path

from aiofiles import open

from .http import HTTPResponse, HTTPRequest
from .middleware import Middleware
from .utils import mime_types


def get_mime_type(ext: str):
    if ext in mime_types:
        return mime_types[ext]
    return "text/plain"


class StaticMiddleware(Middleware):
    def __init__(self, static_path=None):
        self.static_path = path.normpath(path.join(path.dirname(sys.argv[0]), static_path))

    async def __call__(self, req: HTTPRequest, res: HTTPResponse, _next):
        full_path = "./" + req.path
        if full_path.endswith("/"):
            full_path = full_path + "index.html"
        full_path = path.join(self.static_path, full_path)
        full_path = path.normpath(full_path)
        try:
            if len(path.commonprefix([self.static_path, full_path])) != len(self.static_path):
                raise Exception()

            if not path.isfile(full_path):
                raise Exception()

            res.content_type = get_mime_type(path.splitext(full_path)[1])
            res.status = 200
            await res.send_headers()
            async with open(full_path, mode='r') as f:
                async for line in f:
                    await res.write(line)
            await res.done()
            print("-serve static: ", path.relpath(full_path, self.static_path))

        except Exception:
            _next()
