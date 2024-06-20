#!/usr/bin/env python3

from dotenv import load_dotenv
import os
import requests
import v1_munge as mg
import v1_podbean as pb


def main():
    job = requests.get(os.getenv('API_GET_DRIVER')).json()
    if job['response'] == 200:
        bronze_uri = mg.bronze_01_sanitise(job['data'])
        if bronze_uri is not None:
            episode = requests.get(os.getenv('API_GET_EPISODE') % (job['data']['podcast_id'],
                                                                   job['data']['episode_id'])).json()
            if episode['response'] == 200:
                silver_uri = mg.silver_01_process(episode['data'], bronze_uri)
                gold_uri = mg.gold_01_assemble(episode['data'], silver_uri)
                v1_podbean_upload(episode['data'], gold_uri)
    return True


def v1_podbean_upload(episode, file):
    podcast = requests.get(os.getenv('API_GET_PODCAST') % str(episode['podcast_id'])).json()
    if podcast['response'] == 200:
        ep = pb.Podbean(
            os.getenv('PODBEAN_API_TOKEN'),
            os.getenv('PODBEAN_API_UPLOAD'),
            os.getenv('PODBEAN_API_EPISODE'),
            podcast['data']['host_id'],
            podcast['data']['host_secret'],
            episode['title'],
            episode['description'],
            episode['status'],
            episode['type'],
            episode['logo']
        )
        ep.request_token()
        media = ep.upload_auth(file, "audio/mpeg")
        ep.media_key = media["file_key"]
        ep.upload(media["presigned_url"], file, "audio/mpeg")
        ep.publish()


if __name__ == "__main__":
    load_dotenv()
    main()
