#!/usr/bin/env bash

docker-compose up -d --build && docker exec -it web python -m pytest ./