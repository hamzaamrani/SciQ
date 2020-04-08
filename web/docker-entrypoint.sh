#!/usr/bin/env bash
echo "Waiting for MySQL..."
while ! nc -z db 3306; do
    sleep 0.5
done
echo "MySQL started"
#flask db init || true 
sleep 0.5
cd ./web
flask db migrate 
flask db upgrade
cd ..
#cd /sciq
python -m web.run