import hashlib


def respond(start_response, code: str, headers: list[tuple[str, str]] = None, body: bytes = b''):
    headers = headers or [('Content-type', 'text/plain')]
    start_response(code, headers)
    return [body]


def key2path(key: str) -> bytes:
    b = key.encode('utf-8')
    return hashlib.md5(b).digest()
