#!/usr/bin/env python3

import os
from helpers import respond, key2path
from filecache import FileCache


class Volume:

    def __init__(self, vid, basedir):
        self.id = vid
        self.fc = FileCache(basedir)

    def get(self, key):
        return self.fc.get(key)

    def put(self, key, dat):
        return self.fc.put(key, dat)


vid = os.environ['ID']
basedir = os.environ['VOLUME']

v = Volume(vid, basedir)

def volume(env, sr):
    """A volume stores file metadata in local filesystem"""

    key = env['PATH_INFO'][1:]

    if env['REQUEST_METHOD'] == 'GET':
        ret = v.get(key)
        return respond(sr, '200 OK', body=ret)

    elif env['REQUEST_METHOD'] == 'PUT':
        flen = int(env.get('CONTENT_LENGTH', '0'))
        if flen <= 0:
            return respond(sr, '411 Length Required')

        dat = env['wsgi.input'].read()
        if len(dat) != flen:
            return respond(sr, '500 Internal Server Error (length mismatch)')

        v.put(key, dat)
    
        return respond(sr, '200 OK', body=b"Success")

