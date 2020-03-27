#!/usr/bin/env bash

docker-compose up -d --build && docker exec web python -m pytest ./