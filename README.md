# BasicFS

[![CircleCI](https://circleci.com/gh/markoelez/basicfs.svg?style=svg&circle-token=0433e74d7d98b4b5f5814f7f2badac548c7d8bbd)](https://app.circleci.com/pipelines/github/markoelez/basicfs)

## Introduction

BasicFS is a very simple distributed key value store optimized for small files (i.e. photos), inspired by Facebook's [Haystack](https://www.usenix.org/legacy/event/osdi10/tech/full_papers/Beaver.pdf) object store and [SeaweedFS](https://github.com/chrislusf/seaweedfs).

## Usage

By default, volume servers will run on port 9091. When using multiple volume servers, their respective ports should be specified. The master server will default to port 9090 and should be initialized with a "&" separated string containing all volume server urls.

### Build and run docker image

```
./docker.sh
```
Dependencies are tracked/installed using [Pipenv](https://pipenv.pypa.io/en/stable/) and [Pipfile](https://github.com/pypa/pipfile).

Dependencies can be installed manually using:

```
pipenv lock --requirements > requirements.txt && pip install -r /tmp/requirements.txt
```

### Start Volume Server

```
PORT=9092 VOLUME=/tmp/v1 ./volume
```

### Start Master Server

```
PORT=9090 DB=/tmp/db ./master localhost:9090&localhost:9091
```

### Write File

To write a file, send a HTTP PUT request containing the filedata.

```
curl -X PUT -d filedata localhost:9090/fileID
```

### Read File

To read a file, send a HTTP GET request to the `fileID`.

```
curl localhost:9090/fileID
```

You can use this URL to read directly from the volume server:

```
http://localhost:9090/fileID
```

### Delete File

To delete a file, send a HTTP DELETE request to the `fileID`.

```
curl -X DELETE localhost:9090/fileID
```

## Architecture

BasicFS is designed to handle small files efficiently.

Currently fileID's are mapped to volume servers with the master. Eventually, this should be changed so that the master is only aware of volumeIDs which are mapped to their respective urls. Since objects will be written once and read often, the fileID and volumeID should be cached in a local database after the initial write and used in subsequent GET requests.

## In Development

Currently working on adding/refactoring several features:

- RAFT consensus protocol in order to achieve fault tolerance
- User specified replication protocols
- RPC communication for master --> volume relationship (using gRPC, protocol buffers)
- Allow for incorporation of additional volumes to master index (using rebuild, RPC heartbeat)

## License

All code is MIT licensed. Libraries follow their respective licenses.

