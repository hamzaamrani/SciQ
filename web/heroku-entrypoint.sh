#!/usr/bin/env bash
cd ./web
export FLASK_APP=run_prod.py
flask db migrate 
flask db upgrade
cd ..
#cd /sciq