from .http import HTTPRequest, HTTPResponse


class Middleware:
    async def __call__(self, req: HTTPRequest, res: HTTPResponse, _next):
        pass
