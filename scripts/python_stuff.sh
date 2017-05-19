#!/bin/bash

# build project
python3 setup.py build

# install project
python3 setup.py install

# install with pip
pip install .
