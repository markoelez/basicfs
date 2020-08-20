#!/usr/bin/env python3

import os
import sys
import random
import plyvel
import requests
import hashlib
import base64
from helpers import respond
from leveldb import LevelDB


class Master:

    def __init__(self, db_dir, volumes):
        # index maps fileIDs --> volume server URLs
        self.db = LevelDB(db_dir)
        print("Index in %s" % self.db.path)
        
        self.volumes = volumes
        print("Configuring master with volumes: ", self.volumes)

    def id2path(self, fileID):
        # 1 layer deep = 128 byte spread
        md5 = hashlib.md5(fileID).hexdigest()
        key64 = base64.b64encode(fileID).decode('utf-8')
        return f'/{md5[:2]}/{key64}'
        
    def get_volume(self):
        # TODO: intelligently select volume
        return random.choice(self.volumes)

    def get_remote_url(self, fileID):
        try:
            return self.db.get(fileID).decode('utf-8')
        except AttributeError:
            # key not found for some reason
            return None

    def get_remote(self, fileID):
        try:
            # get volume url
            volume = self.get_remote_url(fileID)
            remote = f'http://{volume}{self.id2path(fileID)}'
            return requests.get(remote).text.encode('utf-8')
        except requests.exceptions.ConnectionError:
            print(f"Error retrieving key {fileID.decode('utf-8')} from server {remote}")
            return None

    def put_remote(self, fileID, dat):
        try:
            # get destination volume
            volume = self.get_volume()
            remote = f'http://{volume}{self.id2path(fileID)}'
            print(f'Sending {dat.decode("utf-8")} to {remote}')
            # store in volume server
            requests.put(remote, data=dat).status_code
            # index locally
            self.db.put(fileID, volume.encode('utf-8'))
            return True
        except requests.exceptions.ConnectionError:
            print(f"Error connecting to volume server at {remote}")
            return False

volumes = os.environ["VOLUMES"].split(",")
m = Master(os.getenv("DB", "/tmp/db"), volumes)

def master(env, sr):
    
    # just work with bytes
    key = env['PATH_INFO'][1:].encode('utf-8')


    if env['REQUEST_METHOD'] == 'GET':
        ret = m.get_remote(key)
        if not ret:
            return respond(sr, '404 The requested resource was not found.', body=b'Key does not exist.')
        print(f"Received {ret}. Sending response.")
        return respond(sr, '200 OK', body=ret)

    if env['REQUEST_METHOD'] == 'PUT':
        flen = int(env.get('CONTENT_LENGTH', '0'))
        if flen <= 0:
            return respond(sr, '411 Length Required')

        dat = env['wsgi.input'].read()
        if len(dat) != flen:
            return respond(sr, '500 Internal Server Error (length mismatch)')

        ret = m.put_remote(key, dat)
        if not ret:
            return respond(sr, '404 The requested resource was not found.', body=b'Key does not exist.')
    
        return respond(sr, '201 OK', body=b"Success")

