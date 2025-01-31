Basecast
================

A python project to prepare podcast mp3 files and uploaded to a host.

## Set-up

> docker network create cassandra
> 

### 1. Cassandra

> docker run -v C:\basecast\cql:/root -v C:\basecast\cql\data:/var/lib/cassandra -p 9042:9042 -d --restart always --name cassandra --hostname cassandra --network cassandra cassandra
> 

[exec]
> cqlsh
> 
> source  '~/init.cql';
> 

### 2. API

> docker build -t pgstevenson/basecast_api:1.0 api/.
> 
> docker run -d --restart always -v C:\Users\pstev\downloads:/landing_zone --name basecast_api --network cassandra -p 5000:5000 pgstevenson/basecast_api:1.0
> 

### 3. Engine

> docker build -t pgstevenson/basecast_engine:1.0 py/.
> 
> docker run --rm -v C:\Users\pstev\downloads:/landing_zone -v C:\basecast\data:/data --network cassandra pgstevenson/basecast_engine:1.0
> 
