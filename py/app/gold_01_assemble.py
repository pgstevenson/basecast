from dotenv import load_dotenv
from moviepy.editor import *
import os
import requests
import sys
import urllib.parse

load_dotenv()

episode = requests.get(os.getenv('API_GET_EPISODE') % sys.argv[1]).json()

filename = episode['bronze'][2].split('.')
uri = episode['bronze'][:]
uri[0] = 'gold'
uri[2] = filename[0] + '.mp3'
path_out = eval(os.getenv('ROOT_URI')) + uri
path_out = os.path.join(*path_out)
write_path = eval(os.getenv('ROOT_URI')) + uri[:2]
write_path = os.path.join(*write_path)
operation = ['python', '02_post.py', sys.argv[1]]

if episode['clips'] is None:
    sys.exit(1)

for param in ('intro', 'outro', 'bronze'):
    episode[param] = eval(os.getenv('ROOT_URI')) + episode[param]
    episode[param] = os.path.join(*episode[param])
episode['podcast_id'] = str(episode['podcast_id'])

content = VideoFileClip(episode['bronze'])

segments = []
if os.path.isfile(episode['intro']):
    segments.append(AudioFileClip(episode['intro']))
for clip in episode['clips']:
    subclip = content.subclip(clip[0], clip[1]).set_duration(clip[1]-clip[0])
    segments.append(subclip.audio)
if os.path.isfile(episode['outro']):
    segments.append(AudioFileClip(episode['outro']))

out = concatenate_audioclips(segments)
if not os.path.exists(write_path):
    os.mkdir(write_path)
out.write_audiofile(path_out)

requests.patch(os.getenv('API_PATCH_EPISODE') % (
    sys.argv[1],
    'gold',
    urllib.parse.quote_plus(','.join(uri))
))

requests.post(os.getenv('API_POST_DRIVER') % (
    urllib.parse.quote_plus(','.join(operation)),
    urllib.parse.quote_plus(','.join(uri))
))

content.close()
sys.exit(0)
