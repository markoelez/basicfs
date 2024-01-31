import hashlib


def respond(start_response, code, headers=None, body=b''):
    headers = headers or [('Content-type', 'text/plain')]
    start_response(code, headers)
    return [body]


def key2path(key):
    b = key.encode('utf-8')
    return hashlib.md5(b).digest()
