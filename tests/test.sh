#!/usr/bin/env bash

docker-compose build && docker-compose up -d && docker exec -it web python -m pytest ./