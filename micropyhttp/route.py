from .http import HTTPRequest, HTTPResponse


class Route:
    _instances = {}

    def __new__(cls, handler):
        if handler not in cls._instances:
            cls._instances[handler] = super(Route, cls).__new__(cls)
        return cls._instances[handler]

    def __init__(self, handler):
        if hasattr(self, "_inited"):
            return
        self._inited = True
        self.method = None
        self.handler = handler
        self.path = None
        self.content_type = None

        self.mappers = []

    def is_match(self, req: HTTPRequest):
        return self.method == req.method and self.path == req.path

    async def handle(self, req: HTTPRequest, res: HTTPResponse):
        res.content_type = self.content_type
        result = await self.handler(req=req, res=res)
        for mapper in self.mappers:
            result = mapper(result)
        await res.send(result)

