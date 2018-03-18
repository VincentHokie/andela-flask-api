# Lets not just use any old version but pick one
FROM ubuntu:latest

USER root
# This is needed for flow, and the weirdos that built it in ocaml:
RUN apt-get -y update && apt-get install postgresql postgresql-contrib -y
RUN /etc/init.d/postgresql start

RUN \
  apt-get update -y && \
  apt-get install -y python python-dev python-pip python-virtualenv && \
  apt-get install -y sudo curl wget unzip && \
  apt-get install python3.5 python3-pip -y && \
  apt-get upgrade -y && \
  rm -rf /var/lib/apt/lists/*

RUN wget https://releases.hashicorp.com/packer/0.12.0/packer_0.12.0_linux_amd64.zip && \
  unzip packer_0.12.0_linux_amd64.zip -d packer && \
  sudo mv packer /usr/local/ && \
  export PATH="$PATH:/usr/local/packer"

RUN curl https://sdk.cloud.google.com | bash

RUN useradd jenkins --shell /bin/bash --create-home
RUN echo "jenkins ALL=NOPASSWD: ALL" >> /etc/sudoers


RUN mkdir /.local && chmod 777 /.local

RUN usermod -u 115 jenkins

USER jenkins