#!/bin/bash

FROM balenalib/rpi-raspbian:latest

EXPOSE 80


RUN apt-get update -y
RUN apt-get install -y python3 python-pip-whl python3-pip python-setuptools curl SQLAlchemy
RUN rm -rf /var/lib/apt/lists/*

# Install gunicorn
RUN pip3 install gunicorn

# Install falcon
RUN pip3 install falcon


# Add demo app
COPY ./app /app
WORKDIR /app
RUN pip3 install -r /app/requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:80", "main:app"]