#!/usr/bin/env bash

sudo -u postgres psql -c 'ALTER USER postgres WITH PASSWORD postgres;'