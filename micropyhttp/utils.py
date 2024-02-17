http_codes = {
    100: 'Continue',
    101: 'Switching protocols',
    102: 'Processing',
    200: 'Ok',
    201: 'Created',
    202: 'Accepted',
    203: 'Non authoritative information',
    204: 'No content',
    205: 'Reset content',
    206: 'Partial content',
    207: 'Multi status',
    208: 'Already reported',
    226: 'Im used',
    300: 'Multiple choices',
    301: 'Moved permanently',
    302: 'Found',
    303: 'See other',
    304: 'Not modified',
    305: 'Use proxy',
    307: 'Temporary redirect',
    308: 'Permanent redirect',
    400: 'Bad request',
    401: 'Unauthorized',
    402: 'Payment required',
    403: 'Forbidden',
    404: 'Not found',
    405: 'Method not allowed',
    406: 'Not acceptable',
    407: 'Proxy authentication required',
    408: 'Request timeout',
    409: 'Conflict',
    410: 'Gone',
    411: 'Length required',
    412: 'Precondition failed',
    413: 'Request entity too large',
    414: 'Request uri too long',
    415: 'Unsupported media type',
    416: 'Request range not satisfiable',
    417: 'Expectation failed',
    418: 'I am a teapot',
    422: 'Unprocessable entity',
    423: 'Locked',
    424: 'Failed dependency',
    426: 'Upgrade required',
    428: 'Precondition required',
    429: 'Too many requests',
    431: 'Request header fields too large',
    500: 'Internal micropyhttp error',
    501: 'Not implemented',
    502: 'Bad gateway',
    503: 'Service unavailable',
    504: 'Gateway timeout',
    505: 'Http version not supported',
    506: 'Variant also negotiates',
    507: 'Insufficient storage',
    508: 'Loop detected',
    510: 'Not extended',
    511: 'Network authentication required',
}

mime_types = {
    ".html": "text/html",
    ".css": "text/css",
    ".js": "application/javascript",
    ".json": "application/json",
    ".xml": "application/xml",
    ".jpeg": "image/jpeg",
    ".jpg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".pdf": "application/pdf",
    ".txt": "text/plain",
    ".csv": "text/csv",
    ".mp4": "video/mp4",
    ".mp3": "audio/mp3",
    ".wav": "audio/wav",
    ".ppt": "application/vnd.ms-powerpoint",
    ".xls": "application/vnd.ms-excel",
    ".doc": "application/msword",
    ".svg": "image/svg+xml",
    ".zip": "application/zip"
}


def unquote_plus(s):
    # TODO: optimize
    s = s.replace("+", " ")
    arr = s.split("%")
    arr2 = [chr(int(x[:2], 16)) + x[2:] for x in arr[1:]]
    return arr[0] + "".join(arr2)


def parse_query(query):
    res = {}
    if query:
        pairs = query.split("&")
        for p in pairs:
            vals = [unquote_plus(x) for x in p.split("=", 1)]
            if len(vals) == 1:
                vals.append(True)
            old = res.get(vals[0])
            if old is not None:
                if not isinstance(old, list):
                    old = [old]
                    res[vals[0]] = old
                old.append(vals[1])
            else:
                res[vals[0]] = vals[1]
    return res
