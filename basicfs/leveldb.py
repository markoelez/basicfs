#!/usr/bin/env python3
import plyvel


class LevelDB:

    def __init__(self, basedir):
        self.path = basedir
        self.db = plyvel.DB(self.path, create_if_missing=True)

    def get(self, key):
        try:
            return self.db.get(key)
        except Exception:
            return None

    def put(self, key, value):
        return self.db.put(key, value)

    def delete(self, key):
        v = self.get(key)
        self.db.delete(key)
        return v

    def printall(self):
        with self.db.iterator() as it:
            for k, v in it:
                print(k, v)

    def close(self):
        self.db.close()
        return self.db.closed
