Basecast
================

A python project to prepare podcast mp3 files and uploaded to a host.

## Set-up

> docker network create cassandra
> 

### 1. Cassandra

> docker run -v C:\...\cql:/root -v C:\...\cql\data:/var/lib/cassandra -p 9042:9042 -d --restart always --name cassandra
> --hostname cassandra --network cassandra cassandra
> 

[exec]
> cqlsh
> 
> \# source  '~/init.cql';
> 

### 2. API

> docker build -t pgstevenson/basecast_api api/.
> 
> docker run -d --restart always --name basecast_api --network cassandra -p 5000:5000 pgstevenson/basecast_api
> 

### 3. Engine

> docker build -t pgstevenson/basecast_engine py/.
> 
> docker run -d --restart always -v C:\Users\pstev\downloads:/landing_zone -v C:\basecast\data:/data --name basecast_engine --network cassandra pgstevenson/basecast_engine
> 
