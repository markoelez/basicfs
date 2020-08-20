# BasicFS

Table of Contents
=================

* [Introduction](#introduction)
* [Architecture](#architecture)

## Introduction

BasicFS is a very simple distributed key value store optimized for small files (i.e. photos), inspired by Facebook's [Haystack](https://www.usenix.org/legacy/event/osdi10/tech/full_papers/Beaver.pdf) object store and [SeaweedFS](https://github.com/chrislusf/seaweedfs).

## Architecture

BasicFS is designed to handle small files efficiently. File metadata is managed by an unspecified number of volume servers while the central master manages the volumes themselves. Volume servers are identified by volume id's which are mapped to volume servers in the master server.

