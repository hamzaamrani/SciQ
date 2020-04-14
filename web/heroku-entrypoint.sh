#!/usr/bin/env bash
cd ./web
flask db migrate 
flask db upgrade
cd ..
#cd /sciq