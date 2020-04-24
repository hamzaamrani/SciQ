#!/usr/bin/env bash
pip install -r requirements.txt --upgrade
cd ./web
echo "$STEP"
export FLASK_APP=run_prod.py
flask db upgrade
cd ..
#cd /sciq