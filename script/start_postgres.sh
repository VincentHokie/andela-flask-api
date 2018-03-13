#!/usr/bin/env bash

echo '' | sudo -S -u postgres psql -c 'ALTER USER postgres WITH PASSWORD postgres;'