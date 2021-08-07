FROM python:3.7

ENV PYTHONUNBUFFERED 1

ADD ./requirements /requirements

RUN apt-get update; apt-get --assume-yes install binutils libproj-dev gdal-bin gettext && \
    pip install --no-cache-dir -r /requirements/common.txt && \
    mkdir /project
WORKDIR /project