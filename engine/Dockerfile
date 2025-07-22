FROM python:3.11-bookworm

RUN apt-get update && apt-get install -y
RUN apt -y install ffmpeg
RUN pip install --upgrade pip

COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

ENV PODCAST_LZ=/app/landing_zone
ENV PODCAST_ASSETS=/app/assets
ENV PODCAST_DATA=/app/data

COPY main.py /app/

ARG PODCAST_LZ="/app/landing_zone"
ARG PODCAST_ASSETS="/app/assets"
ARG PODCAST_DATA="/app/data"

ENV PODCAST_LZ=${PODCAST_LZ}
ENV PODCAST_ASSETS=${PODCAST_ASSETS}
ENV PODCAST_DATA=${PODCAST_DATA}

RUN mkdir ${PODCAST_LZ}
RUN mkdir ${PODCAST_ASSETS}
RUN mkdir ${PODCAST_DATA}

WORKDIR /app

CMD [ "python", "main.py" ]