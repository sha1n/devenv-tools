#!/usr/bin/env bash

TMP_DIR=`mktemp -d`
CLONE_DIR=devenv-tools

if [[ ! "$TMP_DIR" || ! -d "$TMP_DIR" ]]; then
  echo "Failed to create temporary directory..."
  exit 1
fi

function onexit() {
  echo
  echo "Cleaning up..."
  rm -rf "$TMP_DIR"
}

trap onexit EXIT


cd ${TMP_DIR}
mkdir ./${CLONE_DIR}

echo "Deploying program code into '$TMP_DIR'..."

curl -Ls https://github.com/sha1n/devenv-tools/tarball/master | tar zx -C ./${CLONE_DIR} --strip-components=1

cd ${CLONE_DIR}

source ./scripts/prereq.sh

echo "Executing..."

source run $@

