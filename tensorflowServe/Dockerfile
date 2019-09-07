FROM tensorflow/serving:latest

COPY ./urbanSound /models/urbanSound

COPY ./config.conf /config/config.conf

ENV MODEL_CONFIG_FILE=/config/config.conf