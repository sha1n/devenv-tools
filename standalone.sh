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
    pip3 uninstall -y workstation-support-dump-sha1n >/dev/null 2>&1
    pip3 uninstall -y workstation-installer-sha1n >/dev/null 2>&1
    pip3 uninstall -y workstation-inspector-dump-sha1n >/dev/null 2>&1
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
echo
python3 -c 'from dump.tarball import tarball; tarball()'
