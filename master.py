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
from record import Record

class Master:

    def __init__(self, db_dir, volumes, replicas):
        # index maps fileIDs --> volume server URLs
        self.db = LevelDB(db_dir)
        print(f"Index in {self.db.path}")
        
        self.volumes = volumes
        self.replicas = replicas
        print(f"Configuring master with volumes: {self.volumes} and {self.replicas} replicas")

    def id2path(self, fileID):
        md5 = self.compute_hash(fileID)
        key64 = base64.b64encode(fileID).decode('utf-8')
        return f'/{md5[:2]}/{key64}'

    def compute_hash(self, s):
        if type(s) == str:
            s = s.encode('utf-8')
        return hashlib.md5(s).hexdigest()
        
    def get_volumes(self):
        # TODO: intelligently select volumes
        volumes = set()
        while len(volumes) != self.replicas:
            volumes.add(random.choice(self.volumes))
        return list(volumes)

    def get_record(self, fileID):
        try:
            return Record.from_bytes(self.db.get(fileID))
        except AttributeError:
            # key not found for some reason
            return None

    def get_remote(self, fileID):
        try:
            # get volume url
            record = self.get_record(fileID)
            # pick one of the volumes
            volume = random.choice(record.volumes)
            remote = f'http://{volume}{self.id2path(fileID)}'
            return requests.get(remote).text.encode('utf-8')
        except (requests.exceptions.ConnectionError, AttributeError) as error :
            print(f"Error retrieving key {fileID.decode('utf-8')} from server. {error}")
            return None

    def put_remote(self, fileID, dat):
        try:
            volumes = self.get_volumes()
            path = self.id2path(fileID)
            buf = []
            for volume in volumes:
                remote = f'http://{volume}{path}'
                buf.append(remote)
                print(f'Sending {dat.decode("utf-8")} to {remote}')
                requests.put(remote, data=dat).status_code
            # get hash
            file_hash = self.compute_hash(''.join(buf))
            rec = Record(rhash=file_hash, volumes=volumes)
            # index locally
            self.db.put(fileID, rec.to_bytes())
            r = Record.from_bytes(self.db.get(fileID))
            return fileID 
        except requests.exceptions.ConnectionError:
            print(f"Error connecting to volume server at {remote}")
            return False

    def delete_remote(self, fileID):
        try:
            # get volume url
            record = self.get_record(fileID)
            file_hash = self.id2path(fileID)
            # delete from all volumes
            for volume in record.volumes:
                remote = f'http://{volume}{file_hash}'
                requests.delete(remote).text.encode('utf-8')
            # delete local index
            self.db.delete(fileID)
            return True
        except requests.exceptions.ConnectionError:
            print(f"Error deleting key {fileID.decode('utf-8')} from server {remote}")
            return None

volumes = os.environ["VOLUMES"].split(",")
replicas = int(os.getenv("REPLICAS", 2))
assert len(volumes) >= replicas, "Must have more volumes than replicas"
m = Master(os.getenv("DB", "/tmp/db"), volumes, replicas)

def master(env, sr):
    
    # just work with bytes
    key = env['PATH_INFO'][1:].encode('utf-8')


    if env['REQUEST_METHOD'] == 'GET':
        ret = m.get_remote(key)
        if not ret:
            return respond(sr, '404 The requested resource was not found.', body=b'Key does not exist.')
        print(f"Received {ret}. Sending response.")
        return respond(sr, '200 OK', body=ret)

    if env['REQUEST_METHOD'] == 'DELETE':
        ret = m.delete_remote(key)
        if not ret:
            return respond(sr, '404 The requested resource was not found.', body=b'Key does not exist.')
        print(f"Received {ret}. Sending response.")
        return respond(sr, '204')

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
    
        return respond(sr, '201 OK', body=ret)

