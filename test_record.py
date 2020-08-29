#!/usr/bin/env python3
import os
import hashlib
import base64
import unittest
import binascii
import logging
from record import Record

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(name)s %(levelname)s %(message)s')
logger.level = logging.DEBUG

class TestRecord(unittest.TestCase):
    
    def get_key(self):
        return b"testkey-" + binascii.hexlify(os.urandom(10))

    def get_hash(self, s):
        return hashlib.md5(s).hexdigest()

    def test_constructors(self):
        key = self.get_key()

        volumes = ['localhost:9091', 'localhost:9092']
        rhash = self.get_hash(key)

        rec = Record(volumes, rhash)

        self.assertEqual(rhash, rec.hash)
        self.assertEqual(volumes, rec.volumes)
        self.assertEqual(rec, Record.from_bytes(rec.to_bytes()))
        self.assertEqual(rec.to_bytes(), Record.from_bytes(rec.to_bytes()).to_bytes())
        self.assertEqual(str(rec), str(Record.from_bytes(rec.to_bytes())))


if __name__ == '__main__':

    unittest.main()
    
