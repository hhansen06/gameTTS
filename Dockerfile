FROM python:3.8

WORKDIR /usr/src/app

RUN git clone https://github.com/lexkoro/GameTTS.git /usr/src/app
RUN pip install -r /usr/src/app/Resources/requirements.txt