#!/usr/bin/env bash

echo "Waiting for MySQL..."

while ! nc -z db 3306; do
    sleep 0.5
done

echo "MySQL started"

#flask db init || true 

sleep 0.5

# check if migrate and upgrade
if [${MIGRATE} == true]; then
    echo "make migration"
    flask db migrate 
    flask db upgrade
else
    echo "not migration"
fi

#cd /sciq
python run.py