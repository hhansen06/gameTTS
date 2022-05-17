FROM python:3.8

WORKDIR /usr/src/app

RUN git clone https://github.com/lexkoro/GameTTS.git /usr/src/app
RUN pip install -r /usr/src/app/Resources/requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg -y
RUN pip install flask
RUN mkdir -p /usr/src/app/GameTTS/vits/model/
#RUN wget https://github.com/lexkoro/GameTTS/releases/download/v0.0.1/G_600000.pth -O /usr/src/app/GameTTS/vits/model/G_600000.pth

COPY main.py /usr/src/app/GameTTS/main.py

EXPOSE 5000
ENTRYPOINT ["python","/usr/src/app/GameTTS/main.py"]