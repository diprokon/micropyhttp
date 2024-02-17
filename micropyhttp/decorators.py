import json
from .route import Route


def get(path):
    def dec(handler):
        route = Route(handler)
        route.method = "GET"
        route.path = path
        return handler

    return dec


def post(path):
    def dec(handler):
        route = Route(handler)
        route.method = "POST"
        route.path = path
        return handler

    return dec


def jsonify():
    def dec(handler):
        route = Route(handler)
        route.content_type = "application/json"
        route.mappers.append(lambda x: json.dumps(x))
        return handler

    return dec
