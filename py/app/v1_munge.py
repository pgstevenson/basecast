#!/usr/bin/env python3

import os
from pathlib import Path
import shutil
# from pedalboard import Pedalboard, Compressor, HighpassFilter, NoiseGate, Limiter
# from pedalboard.io import AudioFile
import subprocess
from string import ascii_lowercase as letter


def concat(files, out):
    subprocess.run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', files,
                    '-codec:a', 'libmp3lame', '-qscale:a', '6', '-b:a', '128k', out])
    return True


def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)
    return True


def bronze_01_sanitise(job):
    try:
        path = ['bronze', job['podcast_id'], job['filename']]
        source = eval(os.getenv('LANDING_ZONE')) + [job['filename']]
        dir_out = eval(os.getenv('ROOT_URI')) + path[:2]
        out = eval(os.getenv('ROOT_URI')) + path
        tmp_out = eval(os.getenv('TMP_URI')) + ['bronze.mp4']
        create_dir(os.path.join(*dir_out))
        shutil.copy(os.path.join(*source), os.path.join(*tmp_out))
        shutil.copy(os.path.join(*tmp_out), os.path.join(*out))
        return os.path.join(*tmp_out)
    except:
        return None


def silver_01_process(dat, content):
    j = 0
    clip_list = eval(os.getenv('TMP_URI')) + ['list.txt']
    out_uri = eval(os.getenv('TMP_URI')) + ['silver.mp3']

    # board = Pedalboard([
    #     Compressor(threshold_db=4, ratio=10, attack_ms=1, release_ms=30),
    #     HighpassFilter(cutoff_frequency_hz=100),
    #     NoiseGate(threshold_db=-30, ratio=2.5, release_ms=60),
    #     Limiter(threshold_db=-0.2)
    # ])

    cl = open(os.path.join(*clip_list), "w")
    for clip in dat['clips']:
        # filename_tmp = eval(os.getenv('TMP_URI')) + [letter[j] + "_o.mp3"]
        filename = eval(os.getenv('TMP_URI')) + [letter[j] + ".mp3"]
        cl.write("file '" + letter[j] + ".mp3'\n")
        j += 1

        # 1. strip clip(s)
        subprocess.run(['ffmpeg', '-y', '-ss', str(clip[0]), '-to', str(clip[1]),
                        '-i', content, '-vn', '-codec:a', 'libmp3lame', '-qscale:a', '6',
                        '-b:a', '128k', os.path.join(*filename)])

        # 2. apply effects
        # with AudioFile(os.path.join(*filename_tmp)) as f:
        #     with AudioFile(os.path.join(*filename), 'w', f.samplerate, f.num_channels) as o:
        #         while f.tell() < f.frames:
        #             chunk = f.read(f.samplerate)
        #             effected = board(chunk, f.samplerate, reset=False)
        #             o.write(effected)
    cl.close()
    concat(os.path.join(*clip_list), os.path.join(*out_uri))
    return os.path.join(*out_uri)


def gold_01_assemble(episode, content):
    episode['content'] = content
    files = []
    filename = episode['filename'].split('.')
    out = eval(os.getenv('TMP_URI')) + [filename[0] + '.mp3']
    output_dir = eval(os.getenv('TMP_URI')) + ['normalized']
    part_list = eval(os.getenv('TMP_URI')) + ['normalized', 'parts.txt']
    create_dir(os.path.join(*output_dir))
    cl = open(os.path.join(*part_list), "w")
    for param in ['intro', 'content', 'outro']:
        if param in ['intro', 'outro']:
            path = eval(os.getenv('ROOT_URI')) + ['bronze', episode['podcast_id'], episode[param]]
            episode[param] = os.path.join(*path)
        if os.path.isfile(episode[param]):
            files.append(episode[param])
            file = Path(episode[param]).name.split(".")
            cl.write("file '" + file[0] + ".mp3'\n")
    cl.close()

    # 3. Normalize loudness
    subprocess.run(['ffmpeg-normalize', '-f', '-t', '-14', '-lrt', '11', '-tp', '-1'] + files +
                   ['-c:a', 'libmp3lame', '-ext', 'mp3', '-of', os.path.join(*output_dir)])
    concat(os.path.join(*part_list), os.path.join(*out))

    return os.path.join(*out)
