#!/usr/bin/env python3

import os
import binascii
import logging
import requests


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(name)s %(levelname)s %(message)s')
logger.level = logging.DEBUG


BASE_URL = b"http://localhost:9092/"


def get_key() -> bytes:
    return b"testkey-" + binascii.hexlify(os.urandom(10))


def get_request_url(key: str) -> str:
    return BASE_URL + key


def test_putget():
    key = get_key()
    url = get_request_url(key)

    r = requests.put(url, data=b"testvalue")
    assert r.status_code == 201
    assert r.text == key.decode()

    r = requests.get(url)
    assert r.status_code == 200
    assert r.text == "testvalue"


def test_putdeleteget():
    key = get_key()
    url = get_request_url(key)

    r = requests.put(url, data=b"testvalue")
    assert r.status_code == 201
    assert r.text == key.decode()

    r = requests.get(url)
    assert r.status_code == 200
    assert r.text == "testvalue"

    r = requests.delete(url)
    assert r.status_code == 204
    assert r.text == ""

    r = requests.get(url)
    assert r.status_code == 404
