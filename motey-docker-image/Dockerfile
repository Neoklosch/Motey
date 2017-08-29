FROM ubuntu:xenial

MAINTAINER Neoklosch version: 0.0.1

ADD ./setup.sh /tmp/setup.sh
ADD ./requirements.txt /tmp/requirements.txt
RUN /bin/bash /tmp/setup.sh

EXPOSE 5023 5091 5092 5094 5094 1883
