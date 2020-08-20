#!/usr/bin/env python3

import os
import time
import unittest
import socket
import binascii
import logging
import requests


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(name)s %(levelname)s %(message)s')
logger.level = logging.DEBUG

class TestBasicFS(unittest.TestCase):

    def get_key(self):
        return b"http://localhost:9090/testkey-" + binascii.hexlify(os.urandom(10))

    def test_putget(self):
        key = self.get_key()

        r = requests.put(key, data=b"testvalue")
        self.assertEqual(r.status_code, 201)

        r = requests.get(key)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.text, "testvalue")


if __name__ == '__main__':

    unittest.main()
    
