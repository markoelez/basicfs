#!/usr/bin/env python3

import os
import tempfile
from helpers import respond, key2path


class FileCache:
    """Represents a volume's local filesystem"""

    def __init__(self, basedir):
        self.basedir = os.path.realpath(basedir)

        assert os.path.isdir(self.basedir)

        print("FileCache initialized in %s" % basedir)

    def _k2p(self, key):
        return os.path.join(self.basedir, key)

    def get(self, key):
        try:
            print(self._k2p(key))
            with open(self._k2p(key), "rb") as f:
                ret = f.read()
                f.close()
                return ret
        except FileNotFoundError:
            return None

    def put(self, key, dat):
        p = self._k2p(key)
        print(p)
        with open(p, 'wb+') as f:
            f.write(dat)
            f.close()
            return True


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

