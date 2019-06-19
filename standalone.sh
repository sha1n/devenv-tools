#!/usr/bin/env bash

TMP_DIR=`mktemp -d`
CLONE_DIR=macos-devenv-dump-poc

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

curl -Ls https://github.com/sha1n/macos-devenv-dump-poc/tarball/master | tar zx -C ./${CLONE_DIR} --strip-components=1

cd ${CLONE_DIR}

source ./scripts/prereq.sh

echo "Executing..."

source run dump $@

