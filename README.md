# BasicFS

[![CI](https://github.com/markoelez/basicfs/actions/workflows/ci.yaml/badge.svg)](https://github.com/markoelez/basicfs/actions/workflows/ci.yaml)


## Introduction

BasicFS is a very simple distributed key value store optimized for small files (i.e. photos), inspired by Facebook's [Haystack](https://www.usenix.org/legacy/event/osdi10/tech/full_papers/Beaver.pdf) object store and [SeaweedFS](https://github.com/chrislusf/seaweedfs).

## Usage

By default, volume servers will run on port 9091. When using multiple volume servers, their respective ports should be specified. The master server will default to port 9090 and should be initialized with a comma separated string containing all volume server urls.

### Build and run docker image

```
./docker.sh
```
Dependencies are tracked/installed using [Pipenv](https://pipenv.pypa.io/en/stable/) and [Pipfile](https://github.com/pypa/pipfile).

Dependencies can be installed manually using:

```
pipenv lock --requirements > requirements.txt && pip install -r /tmp/requirements.txt
```

### Start Two Volume Servers

```
PORT=9090 VOLUME=/tmp/v1 ./scripts/volume
PORT=9091 VOLUME=/tmp/v1 ./scripts/volume
```

### Start Master Server

Must have more volumes than replicas. 

```
PORT=9092 DB=/tmp/db REPLICAS=2 ./scripts/master localhost:9090,localhost:9091
```

### Write File

To write a file, send a HTTP PUT request containing the filedata to the master server.

```
curl -X PUT -d filedata localhost:9092/fileID
```

### Read File

To read a file, send a HTTP GET request to the `fileID`.

```
curl localhost:9092/fileID
```

You can use also use this URL to read directly from the volume server:

```
http://localhost:9090/fileID
```

### Delete File

To delete a file, send a HTTP DELETE request to the `fileID`.

```
curl -X DELETE localhost:9092/fileID
```

## Architecture

BasicFS is designed to handle small files efficiently.

Currently fileID's are mapped to volume servers with the master. Eventually, this should be changed so that the master is only aware of volumeIDs which are mapped to their respective urls. Since objects will be written once and read often, the fileID and volumeID mapping should be cached in a local database after the initial write and used in subsequent GET requests. Uploaded key/value pairs will be replicated accross the specified volume servers based on the user specified replication protocol.

## In Development

Currently working on adding/refactoring several features:

- Consistent hashing scheme (rather than choosing volume randomly)
- RAFT consensus protocol
- RPC communication for master --> volume relationship (using gRPC, protocol buffers)
- Allow for incorporation of additional volumes to master index (using rebuild, RPC heartbeat)

## License

All code is MIT licensed. Libraries follow their respective licenses.

