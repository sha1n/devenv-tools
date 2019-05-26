#!/usr/bin/env bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

PYTHONPATH=${SCRIPT_DIR}/pkg python3 -m unittest discover -p "*_test.py"