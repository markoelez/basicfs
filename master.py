#!/usr/bin/env python3

import os
import sys
import random
import plyvel
import requests
import hashlib
from helpers import respond
from index import Index


class Master:

    def __init__(self, db_dir, volumes):
        # index maps fileIDs --> volume server URLs
        self.db = Index(db_dir)
        print("Index in %s" % self.db.path)
        
        self.volumes = volumes
        print("Configuring master with volumes: ", self.volumes)

    def get_volume(self):
        # TODO: intelligently select volume
        return random.choice(self.volumes)

    def get_fvolume(self, fileID):
        return self.db.get(fileID)

    def get_remote(self, fileID):
        # get volume url
        vurl = self.get_fvolume(fileID)
        if not vurl: return None
        try:
            url = "http://%s/%s" % (vurl, fileID)
            print("Requesting %s from %s" % (fileID, url))
            return requests.get(url).text.encode('utf-8')
        except requests.exceptions.ConnectionError:
            print("Error connecting to volume server at %s" % url)
            return None

    def put_remote(self, fileID, dat):
        # cache destination volume
        vurl = self.get_volume()
        self.db.put(fileID, vurl)
        # send to volume
        print("Sending %s to %s" % (dat, vurl))
        return requests.put("http://%s/%s" % (vurl, fileID), data=dat)

volumes = os.environ["VOLUMES"].split(",")
m = Master(os.getenv("DB", "/tmp/db"), volumes)

def master(env, sr):

    key = env['PATH_INFO'][1:]

    if env['REQUEST_METHOD'] == 'GET':
        ret = m.get_remote(key)
        if not ret:
            return respond(sr, '404 The requested resource was not found.', body=b'Key does not exist.')
        print("Received %s. Sending response." % ret)
        return respond(sr, '200 OK', body=ret)

    elif env['REQUEST_METHOD'] == 'PUT':
        flen = int(env.get('CONTENT_LENGTH', '0'))
        if flen <= 0:
            return respond(sr, '411 Length Required')

        dat = env['wsgi.input'].read()
        if len(dat) != flen:
            return respond(sr, '500 Internal Server Error (length mismatch)')

        m.put_remote(key, dat)
    
        return respond(sr, '200 OK', body=b"Success")

