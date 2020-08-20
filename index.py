#!/usr/bin/env python3

import os
import plyvel


class Index:

    def __init__(self, basedir):
        self.path = basedir
        self.db = plyvel.DB(self.path, create_if_missing=True)

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

