#!/usr/bin/env python3

from dotenv import load_dotenv
import os
import requests
import subprocess
from time import sleep

load_dotenv()

while True:
    rows = requests.get(os.getenv('API_GET_DRIVER')).json()
    for row in rows:
        if row['operation'][1] == "bronze_01_move.py":
            row['trigger'] = eval(os.getenv('LANDING_ZONE')) + [row['trigger'][2]]
        else:
            row['trigger'] = eval(os.getenv('ROOT_URI')) + row['trigger']
        trigger = os.path.join(*row['trigger'])
        if os.path.isfile(trigger):
            subprocess.run(row['operation'])
            requests.delete(os.getenv('API_DELETE_DRIVER') % row['job_id'])
    sleep(60)
