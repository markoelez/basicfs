#!/usr/bin/env python3
from dataclasses import dataclass


@dataclass(eq=True)
class Record:
    # volume server URLs
    volumes: list[str] = None
    # md5 hash = length of 32
    cs: str = None

    @classmethod
    def from_bytes(cls, data: bytes):
        r = Record(None, None)
        try:
            s = data.decode()
            if s.startswith("HASH"):
                r.cs = s[4:36]
                s = s[36:]
            r.volumes = s.split(',')
            return r
        except Exception:
            return None

    def to_bytes(self):
        return str(self).encode()

    def __str__(self):
        return f'HASH{self.cs}{",".join(self.volumes)}'


if __name__ == "__main__":

    b = b"HASH098f6bcd4621d373cade4e832627b4f6localhost:3000,localhost:3001"
    r = Record.from_bytes(b)
    assert (b.decode('utf-8') == str(r))

    print(r.hash)
    print(r.volumes)
