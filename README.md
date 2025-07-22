Basecast
================

A python project to prepare podcast mp3 files and uploaded to a host.

A call to the basecast API container will spin up another container to monitor for the raw data file and start processing once it is available. Start the API with:

> docker run -d --restart always -v "//c/PATH/TO/ASSETS:/app/assets" -v "//var/run/docker.sock://var/run/docker.sock" -p  5000:5000 --name basecast_api pgstevenson/basecast_api

The assets foler should contain:

* `accounts.ini`, e.g.:

```
[DEV]
CLIENT_ID=XXX
CLIENT_SECRET=XX
```

* `config.ini`, e.g.:

```
[PROD]
LOCAL_ASSETS=C:/PATH/TO/ASSETS
LOCAL_LZ=C:/PATH/TO/DOWNLOADS

[FEATURES]
PROCESS_PODCAST=True
UPLOAD_PODCAST=True
```

The assets folder should also include other static files needed for the podcast, i.e. the intro and outro clips.

Currently, the UI for the processing app is `UI.xlsm`, which sends the podcast episode information to the API endpoint.
