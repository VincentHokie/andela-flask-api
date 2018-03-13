# Lets not just use any old version but pick one
FROM ubuntu:latest

# This is needed for flow, and the weirdos that built it in ocaml:
RUN apt-get -y update && apt-get install postgresql postgresql-contrib -y
RUN /etc/init.d/postgresql start

RUN \
  apt-get update && \
  apt-get install -y python python-dev python-pip python-virtualenv && \
  rm -rf /var/lib/apt/lists/*

RUN curl https://bootstrap.pypa.io/get-pip.py | python3.5

RUN useradd jenkins --shell /bin/bash --create-home
USER root