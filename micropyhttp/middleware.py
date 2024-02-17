from abc import abstractmethod
from typing import Callable, Awaitable

from .http import HTTPRequest, HTTPResponse


class Middleware:
    @abstractmethod
    async def __call__(self, req: HTTPRequest, res: HTTPResponse, _next: Callable[[], None]) -> Awaitable[None]:
        pass
