#!/usr/bin/env bash
pip install -r requirements.txt --upgrade
cd ./web
export FLASK_APP=run_prod.py
flask db migrate 
flask db upgrade
cd ..
#cd /sciq