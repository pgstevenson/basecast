@ECHO OFF

docker run --rm -v C:\Users\pstev\downloads:/landing_zone -v C:\basecast\data:/data --network cassandra pgstevenson/basecast_engine:1.0
