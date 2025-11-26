#!/bin/bash

PROJECT_DIR="/home/ubuntu/Linux/cron_assignment"
VENV_DIR="$PROJECT_DIR/venv"

if [ ! -d "$VENV_DIR" ]; then
    /usr/bin/python3 -m venv "$VENV_DIR"
fi


source "$VENV_DIR/bin/activate"

if [ -f "$PROJECT_DIR/requirements.txt" ]; then
    pip install --upgrade pip
    pip install -r "$PROJECT_DIR/requirements.txt"
fi


python "$PROJECT_DIR/fetch_weather.py"
