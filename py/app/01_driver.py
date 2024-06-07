#!/usr/bin/env python3

from dotenv import load_dotenv
import os
import requests
import subprocess
from time import sleep

load_dotenv()

i = 0
while i < 5:
    rows = requests.get(os.getenv('API_GET_DRIVER')).json()
    for row in rows:
        if row['operation'][1] == "bronze_01_move.py":
            row['trigger'] = eval(os.getenv('LANDING_ZONE')) + [row['trigger'][2]]
        else:
            row['trigger'] = eval(os.getenv('ROOT_URI')) + row['trigger']
        trigger = os.path.join(*row['trigger'])
        if os.path.isfile(trigger):
            row['operation'][1] = eval(os.getenv('SCRIPT_ROOT')) + [row['operation'][1]]
            row['operation'][1] = os.path.join(*row['operation'][1])
            subprocess.run(" ".join(row['operation']))
            requests.delete(os.getenv('API_DELETE_DRIVER') % row['job_id'])
    sleep(1)
    i += 1
