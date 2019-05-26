from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="devenv-tools-pkg-sha1n",
    version="0.0.1",
    author="Shai Nagar",
    author_email="shain@wix.com",
    description="Development environment management tools",
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