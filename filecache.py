#!/usr/bin/env python3

import os


class FileCache:
    """Represents a volume's local filesystem"""

    def __init__(self, basedir):
        self.basedir = os.path.realpath(basedir)

        if not os.path.isdir(self.basedir):
            os.mkdir(self.basedir)

        assert os.path.isdir(self.basedir)

        print(f"FileCache initialized in {basedir}")

    def _k2p(self, key):
        return os.path.join(self.basedir, key)

    def get(self, key):
        try:
            with open(self._k2p(key), "rb") as f:
                ret = f.read()
                f.close()
                return ret
        except FileNotFoundError:
            return None

    def put(self, key, dat):
        # create subdirs if not exist
        p = self._k2p(key)
        os.makedirs(os.path.dirname(p), exist_ok=True)

        with open(p, 'wb+') as f:
            f.write(dat)
            f.close()
            return True
        return False

    def delete(self, key):
        try:
            p = self._k2p(key)
            os.remove(p)
            return True
        except:
            return False

