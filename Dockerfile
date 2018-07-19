FROM python:3

COPY  . /jokebot

RUN pip install -r jokebot/requirements.txt
