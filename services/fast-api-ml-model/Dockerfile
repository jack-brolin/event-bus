FROM python:3.7.3
MAINTAINER Strahinja Demic <strahinja.dem@gmail.com>

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN apt-get update
RUN apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev -y

ADD app /app
ADD resources /resources

ADD requirements.txt /
ADD main.py /

ADD model_service.sh /

WORKDIR /

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080
