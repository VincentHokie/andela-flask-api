# Lets not just use any old version but pick one
FROM ubuntu:16.04

# This is needed for flow, and the weirdos that built it in ocaml:
RUN apt-get -y update && apt-get install postgresql postgresql-contrib -y
RUN /etc/init.d/postgresql start
RUN apt-get install python3.5.* -y

RUN useradd jenkins --shell /bin/bash --create-home
USER jenkins