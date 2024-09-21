import asyncio

from .http import HTTPRequest, HTTPResponse, HTTPNotFound, HTTPError
from .middleware import Middleware
from .router import router
from .static import StaticMiddleware


class WebServer:
    def __init__(self):
        self.middlewares: list[Middleware] = []

    def add_middlewares(self, *middlewares: Middleware):
        self.middlewares.extend(middlewares)

    async def _handle(self, reader, writer):
        res = HTTPResponse(writer)
        try:
            req = HTTPRequest(reader)
            await req.read()

            handled = False
            for middleware in self.middlewares:
                end = True

                def _next():
                    nonlocal end
                    end = False

                await middleware(req, res, _next)
                if end:
                    handled = True
                    break

            if not handled:
                raise HTTPNotFound(req.path)
        except HTTPError as error:
            await self._handle_error(res, error)
        except Exception as e:
            await self._handle_error(res, HTTPError(e))
            raise e

    async def run(self, host="127.0.0.1", port=80, static_path=None):
        if static_path:
            server.add_middlewares(StaticMiddleware(static_path))

        print("WebServer: Starting micropyhttp on", host, "port", port)
        await asyncio.start_server(self._handle, host, port)

    async def _handle_error(self, res: HTTPResponse, error: HTTPError):
        res.status = error.status
        await res.send(error.message)


server = WebServer()

server.add_middlewares(
    router,
)
