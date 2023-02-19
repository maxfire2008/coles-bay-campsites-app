# syntax=docker/dockerfile:1

FROM python:3.11-slim

LABEL org.opencontainers.image.source https://github.com/maxfire2008/coles-bay-campsites-app

RUN apt-get update && apt-get install -y git

ENV TZ="Australia/Hobart"

RUN mkdir /repositories

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# git clone maxfire2008/coles-bay-campsites into /data/coles-bay-campsites
RUN git clone https://github.com/maxfire2008/coles-bay-campsites.git /repositories/coles-bay-campsites

COPY . /app

CMD [ "gunicorn", "-b" , "0.0.0.0:80", "--workers=4", "coles_bay_campsites_app.wsgi", "--log-level", "DEBUG", "--reload"]
