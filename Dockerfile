# Lets not just use any old version but pick one
FROM python:3.5-onbuild

# This is needed for flow, and the weirdos that built it in ocaml:
RUN apt-get update && apt-get install postgresql postgresql-contrib
RUN sh 'psql postgres -c "ALTER USER user_name WITH PASSWORD \'new_password\'"'

RUN useradd jenkins --shell /bin/bash --create-home
USER jenkins