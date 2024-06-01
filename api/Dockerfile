FROM python:3.11-bookworm

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY .env ./
COPY api.py ./

EXPOSE 5000/tcp

CMD [ "python", "./api.py" ]
