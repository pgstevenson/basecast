#!/usr/bin/env python3

from dotenv import load_dotenv
import os
import requests
import shutil
import sys
import urllib.parse

load_dotenv()

episode = requests.get(os.getenv('API_GET_EPISODE') % (sys.argv[1], sys.argv[2])).json()
move_from = eval(os.getenv('LANDING_ZONE')) + [episode['bronze'][2]]
move_to_dir = eval(os.getenv('ROOT_URI')) + episode['bronze'][:2]
move_to = eval(os.getenv('ROOT_URI')) + episode['bronze']

path_move_from = os.path.join(*move_from)

if os.path.isfile(path_move_from):

    operation = ['python', 'gold_01_assemble.py', sys.argv[1], sys.argv[2]]
    path_move_to_dir = os.path.join(*move_to_dir)
    path_move_to = os.path.join(*move_to)

    if not os.path.isdir(path_move_to_dir):
        os.mkdir(path_move_to_dir)

    shutil.copy(path_move_from, path_move_to)

    requests.patch(os.getenv('API_PATCH_EPISODE') % (
        sys.argv[1],
        sys.argv[2],
        'bronze',
        urllib.parse.quote_plus(','.join(episode['bronze']))
    ))

    requests.post(os.getenv('API_POST_DRIVER') % (
        urllib.parse.quote_plus(",".join(operation)),
        urllib.parse.quote_plus(','.join(episode['bronze']))
    ))
