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

    BASE_URL = b"http://localhost:9090/"

    def get_key(self):
        return b"testkey-" + binascii.hexlify(os.urandom(10))

    def get_request_url(self, key):
        return self.BASE_URL + key

    def test_putget(self):
        key = self.get_key()
        url = self.get_request_url(key)

        r = requests.put(url, data=b"testvalue")
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.text, key.decode('utf-8'))
        
        r = requests.get(url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.text, "testvalue")

    def test_putdeleteget(self):
        key = self.get_key()
        url = self.get_request_url(key)

        r = requests.put(url, data=b"testvalue")
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.text, key.decode('utf-8'))

        r = requests.get(url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.text, "testvalue")

        r = requests.delete(url)
        self.assertEqual(r.status_code, 204)
        self.assertEqual(r.text, '')

        r = requests.get(url)
        self.assertEqual(r.status_code, 404)

if __name__ == '__main__':

    unittest.main()
    
