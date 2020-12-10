#!/bin/bash


gunicorn config.wsgi:application --bind=unix:/var/run/gunicorn/gunicorn.sock
