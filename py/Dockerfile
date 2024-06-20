FROM python:3.11-bookworm

WORKDIR /usr/src/app

RUN apt update && apt -y install dos2unix ffmpeg

RUN python3 -m pip install --upgrade pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache
COPY ./app ./
RUN find . -type f -print0 | xargs -0 dos2unix

CMD [ "python3", "-u", "./main.py" ]
