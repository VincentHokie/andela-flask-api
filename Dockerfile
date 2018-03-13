# Lets not just use any old version but pick one
FROM ubuntu:16.04

# This is needed for flow, and the weirdos that built it in ocaml:
RUN apt-get -y update && apt-get install postgresql postgresql-contrib -y
RUN /etc/init.d/postgresql start
RUN apt-get install build-essential checkinstall -y
RUN apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev -y
RUN wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz
RUN tar xzf Python-3.5.2.tgz
RUN cd Python-3.5.2
RUN ./configure --enable-optimizations
RUN make altinstall


RUN useradd jenkins --shell /bin/bash --create-home
USER jenkins