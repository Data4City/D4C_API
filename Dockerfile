#!/bin/bash

FROM balenalib/rpi-raspbian:latest

#FROM python:3



RUN apt-get update -y
RUN apt-get install -y python3 python-pip-whl python3-pip python3-setuptools curl
RUN rm -rf /var/lib/apt/lists/*

COPY ./app /app
WORKDIR /app
RUN pip3 install wheel
RUN pip3 install -r /app/requirements.txt
RUN python3 models.py

CMD ["gunicorn", "-b", "0.0.0.0:80", "main:app"]