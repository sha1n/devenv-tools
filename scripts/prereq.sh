#!/usr/bin/env bash

set -e

PYTHON_REQUIRED_MAJOR="3"
PYTHON_REQUIRED_MINOR="7"

if ! command -v python3 &>/dev/null; then
    echo "Python $PYTHON_REQUIRED_MAJOR.x is required to run this program..."
    echo "Trying to install the latest Python $PYTHON_REQUIRED_MAJOR version..."
    brew install python3
fi

PYTHON_ACTUAL_MAJOR=`python3 -c 'import sys; print(sys.version_info[0])'`
PYTHON_ACTUAL_MINOR=`python3 -c 'import sys; print(sys.version_info[1])'`

if [[ "$PYTHON_REQUIRED_MINOR" > "$PYTHON_ACTUAL_MINOR" ]]; then
    echo "Trying to update Python $PYTHON_REQUIRED_MAJOR to the latest version..."

    brew upgrade python3
fi

echo "Installing packages..."
pip3 install --user ./inspector-pkg >/dev/null 2>&1
pip3 install --user ./installer-pkg >/dev/null 2>&1
pip3 install --user ./dump-pkg >/dev/null 2>&1
