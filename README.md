[![Build Status](https://travis-ci.org/sha1n/devenv-tools.svg?branch=master)](https://travis-ci.org/sha1n/devenv-tools)

# devenv-tools

## Running Tools From Source

```bash
./run <module-name> [options]
```

Examples:
```bash

# dump tool
./run dump

# installer
./run installer --help


# inspector
./run inspector --help

```

## Running Tools from Any Workstation

`curl https://raw.githubusercontent.com/sha1n/devenv-tools/master/standalone.sh | bash -s -- <module-name> [options]`
