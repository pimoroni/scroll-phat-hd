#!/bin/bash

if [ ! -d "../sphinx.virtualenv" ]; then
  sudo pip install virtualenv
  python -m virtualenv ../sphinx.virtualenv
fi
source ../sphinx.virtualenv/bin/activate
pip install -r requirements.txt
make html
deactivate
