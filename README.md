# BasicFS

## Introduction

BasicFS is a very simple distributed key value store optimized for small files (i.e. photos), inspired by Facebook's [Haystack](https://www.usenix.org/legacy/event/osdi10/tech/full_papers/Beaver.pdf) object store and [SeaweedFS](https://github.com/chrislusf/seaweedfs).

## Architecture

BasicFS is designed to handle small files efficiently.

Currently fileID's are mapped to volume servers with the master. Eventually, this should be changed so that the master is only aware of volumeIDs which are mapped to their respective urls. Since objects will be written once and read often, the fileID and volumeID should be cached in a local database after the initial write and used in subsequent GET requests.

## Usage

By default, volume servers will run on port 9091. When using multiple volume servers, their respective ports should be specified. The master server will default to port 9090 and should be initialized with a comma separate string containing all volume server urls.

### Start Volume Server

```
PORT=9092 VOLUME=/tmp/v1 ./volume
```

### Start Master Server

```
PORT=9090 DB=/tmp/db ./master localhost:9090,localhost:9091
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

## License

All code is MIT licensed. Libraries follow their respective licenses.

