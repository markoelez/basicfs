#!/usr/bin/env python3
import os


# Represents a volume's local filesystem
class FileCache:
    def __init__(self, basedir: str):
        self.basedir = os.path.realpath(basedir)

        if not os.path.isdir(self.basedir):
            os.mkdir(self.basedir)

        assert os.path.isdir(self.basedir)

        print(f"FileCache initialized in {basedir}")

    def _k2p(self, key: str) -> str:
        return os.path.join(self.basedir, key)

    def get(self, key: str) -> bytes | None:
        try:
            with open(self._k2p(key), "rb") as f:
                return f.read()
        except FileNotFoundError:
            return None

    def put(self, key: str, dat: bytes) -> bool:
        # create subdirs if not exist
        p = self._k2p(key)
        os.makedirs(os.path.dirname(p), exist_ok=True)

        with open(p, 'wb+') as f:
            f.write(dat)

        return True

    def delete(self, key: str) -> bool:
        try:
            p = self._k2p(key)
            os.remove(p)
            return True
        except Exception:
            return False
