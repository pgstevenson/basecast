import configparser
import logging
import os
from re import sub
import requests
from time import sleep
import shutil
import subprocess

class Episode:
  def __init__(self, intro, outro, filename, start_time,
               end_time, clip_timestamps, title, description, status, type, logo):
    self.intro = intro
    self.outro = outro
    self.filename = filename
    self.start_time = start_time
    self.end_time = end_time
    self.clip_timestamps = self.unmarshal_clips(clip_timestamps)
    self.title = title
    self.description = description
    self.status = status
    self.type = type
    self.logo = logo
    
  def update_filename(self, new_value):
    self.filename = new_value
    return None

  def process(self):
    clips = []
    for i in range(0, len(self.clip_timestamps)):
        clip = self.clip_timestamps[i]
        fn = os.path.join(os.getenv('PODCAST_DATA'), f'{i}.mp3')
        clips.append(fn)
        subprocess.run(['ffmpeg', '-y', '-ss', str(clip[0]), '-to', str(clip[1]),
                        '-i', self.filename, '-vn', '-codec:a', 'libmp3lame', '-qscale:a', '6',
                        '-b:a', '128k', fn])
    self.clips = clips
    return None
  
  @staticmethod
  def unmarshal_clips(d):
      o = []
      for i in d.split(';'):
          o.append(list(int(e) for e in i.split(',')))
      return(o)

  def assemble(self):
    self.podcast_path = os.path.join(os.getenv('PODCAST_DATA'), self.filename).replace('.mp4', '.mp3')

    # List of files that combined make up the podcast episode, intro, clips, and outro
    files = [os.path.join(os.getenv('PODCAST_ASSETS'), f'{self.intro}')] + self.clips + [os.path.join(os.getenv('PODCAST_ASSETS'), f'{self.outro}')]

    # Normalize loudness
    files = [os.path.join(os.getenv('PODCAST_ASSETS'), f'{self.intro}')] + self.clips + [os.path.join(os.getenv('PODCAST_ASSETS'), f'{self.outro}')]
    subprocess.run(['ffmpeg-normalize', '-f', '-t', '-14', '-lrt', '11', '-tp', '-1'] + files +
                  ['-c:a', 'libmp3lame', '-ext', 'mp3', '-of', os.getenv('PODCAST_DATA')])
    
    # Combine files into 1 clip
    files = [os.path.join(os.getenv('PODCAST_DATA'), f'{self.intro}')] + self.clips + [os.path.join(os.getenv('PODCAST_DATA'), f'{self.outro}')]
    files = list(x.replace(".wav", ".mp3") for x in files)
    files = list(f"file '{x}'" for x in files)

    with open(os.path.join(os.getenv('PODCAST_DATA'), 'parts.txt'), 'w') as f:
        f.write("\n".join(map(str, files)))

    if os.path.exists(self.podcast_path):
      os.remove(self.podcast_path)

    subprocess.run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', os.path.join(os.getenv('PODCAST_DATA'), 'parts.txt'),
                    '-codec:a', 'libmp3lame', '-qscale:a', '6', '-b:a', '128k', self.podcast_path])
    
    return None

if __name__ == '__main__':

  logging.basicConfig(filename='/app/engine.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)03d %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)
  
  accounts = configparser.ConfigParser()
  accounts.read('/app/assets/accounts.ini')

  config = configparser.ConfigParser()
  config.read('/app/assets/config.ini')

  episode = Episode(
    os.getenv('INTRO'),
    os.getenv('OUTRO'),
    os.getenv('FILENAME'),
    os.getenv('START_TIME'),
    os.getenv('END_TIME'),
    os.getenv('CLIP_TIMESTAMPS'),
    os.getenv('TITLE'),
    os.getenv('DESCRIPTION'),
    os.getenv('STATUS'),
    os.getenv('TYPE'),
    os.getenv('LOGO')
    )
  
  found = False
  while not found:
    print('Looking for raw input file...', flush=True) # print not printing in real time
    files = os.listdir(os.getenv('PODCAST_LZ'))
    idx = [i for i, x in enumerate(files) if sub("\\s+", " ", x) == episode.filename]
    if len(idx) > 0:
      print('Raw input file found.', flush=True)
      found = True
      lz_path = os.path.join(os.getenv('PODCAST_LZ'), files[idx[0]])
      episode.update_filename(os.path.join(os.getenv('PODCAST_DATA'), files[idx[0]]))
      if config['FEATURES']['PROCESS_PODCAST'].lower()=='true':
        shutil.copy(lz_path, episode.filename)
        print('Bronze: Done', flush=True)
        episode.process()
        print('Silver: Done', flush=True)
        episode.assemble()
        logging.info(f'File path: {episode.podcast_path}')
        logging.info(f'File name: {os.path.basename(episode.podcast_path)}')
        logging.info(f'File size: {os.path.getsize(episode.podcast_path)}')
        print('Gold: Done', flush=True)
      if config['FEATURES']['PROCESS_PODCAST'].lower()=='true' and config['FEATURES']['UPLOAD_PODCAST'].lower()=='true':
        print('Requesting Podbean upload...', flush=True)
        
        token_resp = requests.post('https://api.podbean.com/v1/oauth/token', auth=(accounts[os.getenv('PODCAST_ACCOUNT')]['CLIENT_ID'], accounts[os.getenv('PODCAST_ACCOUNT')]['CLIENT_SECRET']), data={'grant_type': 'client_credentials'})
        token_dat = token_resp.json()
        if token_resp.status_code != 200:
          logging.debug(f'uploadAuthorize: {token_resp.status_code}')
          logging.debug(f'uploadAuthorize: {token_dat["error"]}')
          logging.debug(f'uploadAuthorize: {token_dat["error_description"]}')
        
        media_resp = requests.get('https://api.podbean.com/v1/files/uploadAuthorize', params={'access_token': token_dat['access_token'], 'filename': os.path.basename(episode.podcast_path), 'filesize': os.path.getsize(episode.podcast_path), 'content_type': 'audio/mpeg'})
        media_dat = media_resp.json()
        if media_resp.status_code != 200:
          logging.debug(f'uploadAuthorize: {media_resp.status_code}')
          logging.debug(f'uploadAuthorize: {media_dat["error"]}')
          logging.debug(f'uploadAuthorize: {media_dat["error_description"]}')
        
        print('Upload started...', flush=True)
        requests.put(media_dat['presigned_url'], headers={'Content-Type': 'audio/mpeg'}, files={'file': (os.path.basename(episode.podcast_path), open(episode.podcast_path, 'rb'))})
        
        episodes_resp = requests.post('https://api.podbean.com/v1/episodes', data={'access_token': token_dat['access_token'], 'title': episode.title, 'content': episode.description, 'status': episode.status, 'type': episode.type, 'media_key': media_dat['file_key'], 'remote_logo_url': episode.logo})
        episodes_dat = episodes_resp.json()
        if episodes_resp.status_code != 200:
          logging.debug(f'Episodes: {episodes_resp.status_code}')
          logging.debug(f'Episodes: {episodes_dat["error"]}')
          logging.debug(f'Episodes: {episodes_dat["error_description"]}')
        
        logging.info('Upload complete.')
        print('Upload complete.', flush=True)
      print('Done.', flush=True)
    logger = logging.getLogger()
    sleep(5)
  if config['FEATURES']['IDLE_ENGINE'].lower()=='true':
    sleep(9999)
