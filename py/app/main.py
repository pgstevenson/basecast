#!/usr/bin/env python3

from dotenv import load_dotenv
from moviepy.editor import *
import os
import requests
import shutil
import v1_podbean as pb


def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)
    return


def main():
    job = requests.get(os.getenv('API_GET_DRIVER')).json()
    if job['response'] == 200:
        v1_bronze_01_sanitise(job)
        episode = requests.get(os.getenv('API_GET_EPISODE') % (job['data']['podcast_id'],
                                                               job['data']['episode_id'])).json()
        if episode['response'] == 200:
            file_uri = v1_gold_01_assemble(episode['data'])
            v1_podbean_upload(episode['data'], file_uri)
    return


def v1_bronze_01_sanitise(job):
    try:
        path = ['bronze', job['podcast_id'], job['filename']]
        source = eval(os.getenv('LANDING_ZONE')) + [job['filename']]
        dir_out = eval(os.getenv('ROOT_URI')) + path[:2]
        out = eval(os.getenv('ROOT_URI')) + path
        create_dir(os.path.join(*dir_out))
        shutil.copy(os.path.join(*source), os.path.join(*out))
        return 1
    except:
        return 0


# def v1_silver_01_sanitize(episode):
# PLACEHOLDER
# 1. Strip audio
# 2. Remove reverb
# 3. Apply noise gate
# 4. Apply sound compression - might need to be included in assemble after
#    adding intro and outro


def v1_gold_01_assemble(episode):
    segments = []
    filename = episode['filename'].split('.')
    path = ['gold', episode['podcast_id'], filename[0] + '.mp3']
    out = eval(os.getenv('ROOT_URI')) + path
    dir_out = eval(os.getenv('ROOT_URI')) + path[:2]

    episode['podcast_id'] = str(episode['podcast_id'])
    for param in ('intro', 'outro', 'filename'):
        episode[param] = ['bronze', episode['podcast_id'], episode[param]]
        episode[param] = eval(os.getenv('ROOT_URI')) + episode[param]
        episode[param] = os.path.join(*episode[param])

    content = VideoFileClip(episode['filename'])
    if os.path.isfile(episode['intro']):
        segments.append(AudioFileClip(episode['intro']))
    for clip in episode['clips']:
        subclip = content.subclip(clip[0], clip[1]).set_duration(clip[1] - clip[0])
        segments.append(subclip.audio)
    if os.path.isfile(episode['outro']):
        segments.append(AudioFileClip(episode['outro']))
    blob = concatenate_audioclips(segments)

    create_dir(os.path.join(*dir_out))
    blob.write_audiofile(os.path.join(*out), logger=None)
    content.close()
    return os.path.join(*out)


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
