from .decorators import get, post, jsonify
from .http import HTTPRequest, HTTPResponse
from .server import server as _server


async def run(host="127.0.0.1", port=80, static_path=None):
    await _server.run(host, port, static_path)


# def start(host="127.0.0.1", port=80, static_path=None):
#     loop = new_event_loop()
#     set_event_loop(loop)
#     loop.create_task(_server.run(host, port, static_path))
#     try:
#         loop.run_forever()
#         loop.close()
#     except KeyboardInterrupt:
#         pass
