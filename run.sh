#!/usr/bin/env sh
alembic upgrade head
python -m uvicorn main:app
