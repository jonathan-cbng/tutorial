#!/usr/bin/env sh
cd database
alembic upgrade head
cd ..
./main.py
