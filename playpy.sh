#!/bin/bash

# Play our AI against lookt9
# Example:
# ./test9.sh 12345

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <port>" >&2
  exit 1
fi

bin/servt9 -p $1 & sleep 0.1
./agent.py   -p $1 & sleep 0.1
bin/lookt9 -p $1
