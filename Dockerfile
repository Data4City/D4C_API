#!/bin/bash

#FROM balenalib/rpi-raspbian:latest

FROM python:3



RUN apt-get update -y
RUN apt-get install -y python3 python-pip-whl python3-pip python3-setuptools curl
RUN apt-get -y install libgeos-c1
RUN apt-get -y install libgeos-dev


RUN rm -rf /var/lib/apt/lists/*

COPY ./app /app
WORKDIR /app
RUN pip3 install wheel
RUN pip3 install -r /app/requirements.txt


CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:app"]