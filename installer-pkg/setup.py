from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import setup, find_packages

PKG_NAME = "shminstaller"
PKG_VERSION = "0.0.5"

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name=PKG_NAME,
    version=PKG_VERSION,
    author="Shai Nagar",
    author_email="shain@wix.com",
    description="Development environment installation tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sha1n/devenv-tools",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
    ],
    install_requires=[
        'shminspector>=0.0.4',
        'networkx>=2.2,<3',
    ],
    test_suite="tests"
)
