#!/usr/bin/env python3
import os
import hashlib
import binascii
import logging
from basicfs.record import Record

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(name)s %(levelname)s %(message)s')
logger.level = logging.DEBUG


def get_key() -> bytes:
    return b"testkey-" + binascii.hexlify(os.urandom(10))


def get_hash(s: str) -> bytes:
    return hashlib.md5(s).hexdigest()


def test_basic():
    key = get_key()

    volumes = ['localhost:9091', 'localhost:9092']
    cs = get_hash(key)

    rec = Record(volumes, cs)

    assert cs == rec.cs
    assert volumes == rec.volumes
    assert rec == Record.from_bytes(rec.to_bytes())
    assert rec.to_bytes() == Record.from_bytes(rec.to_bytes()).to_bytes()
    assert str(rec) == str(Record.from_bytes(rec.to_bytes()))
