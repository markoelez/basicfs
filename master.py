#!/usr/bin/env python3

import os
import sys
import random
import plyvel
import requests
import hashlib
from enum import Enum
from helpers import respond


class LevelCache:

    def __init__(self, basedir):
        self.db = plyvel.DB(basedir, create_if_missing=True)

    def get(self, key):
        k = self._str2bytes(key)
        try:
            v = self.db.get(k)
            return self._bytes2str(v)
        except:
            return None
    
    def put(self, key, value):
        k, v = self._str2bytes(key), self._str2bytes(value)
        return self.db.put(k, v)

    def delete(self, key):
        k = self._str2bytes(key)
        v = self.get(key)
        self.db.delete(k)
        # return most recent value
        return v

    def close(self):
        self.db.close()
        return self.db.closed

    def _str2bytes(self, s):
        return s.encode('utf_8')

    def _bytes2str(self, b):
        return b.decode('utf_8')

class Master:

    def __init__(self, db_dir, volumes):
        # db maps fileIDs --> volume server URLs
        self.db = LevelCache(db_dir)
        
        # assign arithmetic id to each volume
        self.volumes = volumes

    def get_volume(self):
        # TODO: intelligently select volume
        return random.choice(self.volumes)

    def get_fvolume(self, fileID):
        return self.db.get(fileID)

    def get_remote(self, fileID):
        # get volume url
        url = "http://%s/%s" % (self.get_fvolume(fileID), fileID)
        print("Requesting %s from %s" % (fileID, url))
        return requests.get(url).text.encode('utf-8')

    def put_remote(self, fileID, dat):
        # cache destination volume
        vurl = self.get_volume()
        self.db.put(fileID, vurl)
        # send to volume
        print("Sending %s to %s" % (dat, vurl))
        return requests.put("http://%s/%s" % (vurl, fileID), data=dat)

volumes = os.environ["VOLUMES"].split(",")
print("Configuring master with volumes ", volumes)
m = Master("tmp/db", volumes)

def master(env, sr):

    key = env['PATH_INFO'][1:]

    if env['REQUEST_METHOD'] == 'GET':
        ret = m.get_remote(key)
        print(ret)
        return respond(sr, '200 OK', body=ret)

    elif env['REQUEST_METHOD'] == 'PUT':
        flen = int(env.get('CONTENT_LENGTH', '0'))
        if flen <= 0:
            return respond(sr, '411 Length Required')

        dat = env['wsgi.input'].read()
        if len(dat) != flen:
            return respond(sr, '500 Internal Server Error (length mismatch)')

        m.put_remote(key, dat)
    
        return respond(sr, '200 OK', body=b"Success")

