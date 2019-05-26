#!/bin/bash


FROM pypy:3.6


RUN apt-get update -y
#RUN apt-get install -y python3 python-pip-whl python3-pip python3-setuptools curl
RUN apt-get -y install libgeos-c1v5
RUN apt-get -y install libgeos-dev


RUN rm -rf /var/lib/apt/lists/*

COPY ./app /app
WORKDIR /app
#RUN pip3 install wheel
RUN pip install --no-cache-dir -r /app/requirements.txt


CMD ["pypy3", "standalone_debug.py"]