[![Build Status](https://travis-ci.org/sha1n/devenv-tools.svg?branch=master)](https://travis-ci.org/sha1n/devenv-tools)

# devenv-tools
This repository contains tools for development workstation configuration management. *Currently only MacOS is supported*

## Tools

### Installer 
The installer (package name 'shminstaller') is a Python 3 package that provides a CLI for inspecting current workstation 
state, installing missing components and configuring specific tools.

#### How To Install
```bash
pip3 install --user shminstaller --install-option="--install-scripts=/usr/local/bin"
```

#### How To Run
```bash
$ envinstall
``` 

### Dump Tool 
The dump tool (package name 'dumpshmamp') is a Python 3 package that provides a CLI for collecting data about installed
development tools from a workstation and packaging them into one tarball.

#### How To Install
```bash
pip3 install --user dumpshmamp --install-option="--install-scripts=/usr/local/bin"
```

#### How To Run
```bash
$ envdump
``` 