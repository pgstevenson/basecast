#!/usr/bin/env python3

from datetime import datetime
import os
import requests


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

    @staticmethod
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
