
def respond(start_response, code, headers=[('Content-type', 'text/plain')], body=b''):
    start_response(code, headers)
    return [body]

def key2path(key):
    b = key.encode('utf-8')
    return hashlib.md5(b).digest()

