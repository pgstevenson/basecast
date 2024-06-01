FROM python:3.11-bookworm

WORKDIR /usr/src/app

RUN python3 -m pip install --upgrade pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./

CMD [ "python", "./01_driver.py" ]
