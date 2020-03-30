#!/usr/bin/env bash

MIGRATE=true docker-compose up -d --build && docker exec web python -m pytest ./