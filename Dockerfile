# Lets not just use any old version but pick one
FROM python:3.5-onbuild

# This is needed for flow, and the weirdos that built it in ocaml:
RUN apt-get -y update && apt-get install postgresql postgresql-contrib -y
RUN /etc/init.d/postgresql start
RUN cat /etc/services | grep 5432
RUN service postgresql status
RUN service postgresql start
RUN service postgresql status

RUN useradd jenkins --shell /bin/bash --create-home
USER jenkins