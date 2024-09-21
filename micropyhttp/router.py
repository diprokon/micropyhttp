from .http import HTTPRequest, HTTPResponse
from .middleware import Middleware
from .route import Route


class RouterMiddleware(Middleware):
    def __init__(self):
        pass

    async def __call__(self, req: HTTPRequest, res: HTTPResponse, _next):
        route = self._find_route(req)
        if route:
            await route.handle(req, res)
        else:
            _next()

    def _find_route(self, req: HTTPRequest):
        for route in self.routes():
            if route.is_match(req):
                return route
        return None

    def routes(self):
        return list(Route._instances.values())


router = RouterMiddleware()
