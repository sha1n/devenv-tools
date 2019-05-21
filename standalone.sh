#!/usr/bin/env bash

TMP_DIR=`mktemp -d`

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

echo "Deploying program code into '$TMP_DIR'..."
echo
cd "$TMP_DIR"
mkdir ./dump
curl -L https://github.com/sha1n/macos-devenv-dump-poc/tarball/master | tar zx -C ./dump --strip-components=1

cd "dump"

echo
echo "Executing..."
echo
bash -c ./dump