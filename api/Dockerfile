FROM python:3.11-bookworm

RUN apt-get update && apt-get install -y
RUN pip install --upgrade pip

COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

ARG PODCAST_LZ="/app/landing_zone"
ARG PODCAST_ASSETS="/app/assets"

ENV PODCAST_LZ=${PODCAST_LZ}
ENV PODCAST_ASSETS=${PODCAST_ASSETS}

RUN mkdir ${PODCAST_ASSETS}

COPY main.py /app/

WORKDIR /app

EXPOSE 5000

CMD [ "python", "main.py" ]
