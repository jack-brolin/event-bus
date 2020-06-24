#!/usr/bin/env bash
exec gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8080 --workers 10
