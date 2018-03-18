#!/usr/bin/env bash

sudo su postrges
sudo sed -i 's/peer/trust/g' /etc/postgresql/9.5/main/pg_hba.conf

sudo /etc/init.d/postgresql restart

# change postgres' password to a known value and create the test database
echo '' | psql --username=postgres --command="ALTER USER postgres WITH PASSWORD 'postgres';"
echo '' | psql --username=postgres --command="create database testdb;"

sudo sed -i 's/trust/peer/g' /etc/postgresql/9.5/main/pg_hba.conf
sudo /etc/init.d/postgresql restart
