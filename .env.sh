#!/usr/bin/env bash

# .env defaults:
#   FLASK_APP=.
#   FLASK_ENV=development


if [ ! -f ".env" ]; then
  touch .env
  printf "FLASK_APP=.\nFLASK_ENV=development\n" >> .env
  echo "Made default .env file"
else
  echo ".env already exists"
fi
