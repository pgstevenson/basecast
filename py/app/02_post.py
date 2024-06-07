#!/usr/bin/env python3

from datetime import datetime
from dotenv import load_dotenv
import os
import requests
import sys


class Podbean:
    def __init__(self, token_endpoint, upload_endpoint, episode_endpoint, client_id, client_secret, title, content,
                 status, publish_type, logo_url):
        self.token_endpoint = token_endpoint
        self.upload_endpoint = upload_endpoint
        self.episode_endpoint = episode_endpoint
        self.client_id = client_id
        self.client_secret = client_secret
        self.title = title
        self.content = content
        self.status = status
        self.type = publish_type
        self.token = None
        self.media_key = None
        self.remote_logo_url = logo_url

    def request_token(self):
        params = {"grant_type": "client_credentials"}
        r = requests.post(self.token_endpoint,
                          auth=(self.client_id, self.client_secret),
                          data=params)
        print(datetime.now(), f" Token request status code: {r.status_code}")
        x = r.json()
        self.token = x["access_token"]
        if r.status_code != 200:
            print(x["error"])
            print(x["error_description"])
        return 0

    def upload_auth(self, file, content_type):
        params = {"access_token": self.token,
                  "filename": os.path.basename(file),
                  "filesize": os.path.getsize(file),
                  "content_type": content_type}
        r = requests.get(self.upload_endpoint, params=params)
        x = r.json()
        print(datetime.now(), f" Authorise file upload status code: {r.status_code}")
        if r.status_code != 200:
            print(x["error"])
            print(x["error_description"])
        return x

    def publish(self):
        data = {"access_token": self.token,
                "title": self.title,
                "content": self.content,
                "status": self.status,
                "type": self.type}
        if self.media_key is not None:
            data["media_key"] = self.media_key
        if self.remote_logo_url is not None:
            data["remote_logo_url"] = self.remote_logo_url
        r = requests.post(self.episode_endpoint, data=data)
        print(datetime.now(), f" Episode status code: {r.status_code}")
        if r.status_code != 200:
            x = r.json()
            print(x["error"])
            print(x["error_description"])


def upload(url, file, content_type) -> int:
    headers = {"Content-Type": content_type}
    files = {"file": (os.path.basename(file), open(file, 'rb'))}
    r = requests.put(url, headers=headers, files=files)
    print(datetime.now(), f" {os.path.basename(file)} Upload status code: {r.status_code}")
    if r.status_code != 200:
        x = r.json()
        print(x["error"])
        print(x["error_description"])
    return 0


load_dotenv()

episode = requests.get(os.getenv('API_GET_EPISODE') % (sys.argv[1], sys.argv[2])).json()
podcast = requests.get(os.getenv('API_GET_PODCAST') % str(episode['podcast_id'])).json()

path_uri = eval(os.getenv('ROOT_URI')) + episode['gold']
path_uri = os.path.join(*path_uri)

load = Podbean(
    os.getenv('PODBEAN_API_TOKEN'),
    os.getenv('PODBEAN_API_UPLOAD'),
    os.getenv('PODBEAN_API_EPISODE'),
    podcast['host_id'],
    podcast['host_secret'],
    episode['title'],
    episode['description'],
    episode['status'],
    episode['type'],
    episode['logo']
)

# load.request_token()
# media = load.upload_auth(path_uri, "audio/mpeg")
# load.media_key = media["file_key"]
# upload(media["presigned_url"], path_uri, "audio/mpeg")
# load.publish()
print("OK")
sys.exit(0)
