#!/bin/bash

source /venv/amy/bin/activate && python /app/manage.py rqworker -v 2
