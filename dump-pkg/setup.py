from setuptools import setup, find_packages

PKG_NAME="workstation-support-dump-sha1n"
PKG_VERSION="0.0.1"

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name=PKG_NAME,
    version=PKG_VERSION,
    author="Shai Nagar",
    author_email="shain@wix.com",
    description="Development environment support dump tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sha1n/macos-devenv-dump-poc",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
    ],
)
