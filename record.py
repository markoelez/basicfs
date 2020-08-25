#!/usr/bin/env python3

class Record:
    
    def __init__(self, volumes=None, rhash=None):
        # volume server URLs
        self.volumes = volumes
        # md5 hash = length of 32
        self.hash = rhash

    def from_bytes(data):
        r = Record(None, None)
        try:
            s = data.decode('utf-8')
            if s.startswith("HASH"):
                r.hash = s[4:48] 
                s = s[48:]
            r.volumes = s.split(',')
            return r 
        except:
            return None

    def to_bytes(self):
        return str(self).encode('utf-8')

    def __eq__(self, other):
        return self.volumes == other.volumes and self.hash == other.hash

    def __str__(self):
        return f'HASH{self.hash}{",".join(self.volumes)}'

if __name__ == "__main__":

    b = "HASH098f6bcd4621d373cade4e832627b4f6localhost:3000,localhost:3001".encode('utf-8')

    r = Record.from_bytes(b)

    print(r)

    t = r.to_bytes()

    print(t)

