#!/bin/bash

VENV_DIR="../sphinx.virtualenv"

echo "Checking for ${VENV_DIR}"

function install_requirements {
  echo "Installing requirements..."
  source ${VENV_DIR}/bin/activate
  pip install -r requirements.txt
  cp requirements.txt ${VENV_DIR}/requirements.txt
  deactivate
}

if [ ! -d "${VENV_DIR}" ]; then
  sudo pip install virtualenv
  python -m virtualenv ${VENV_DIR}
  install_requirements
else
  echo "Checking requirements..."
  diff requirements.txt ${VENV_DIR}/requirements.txt > /dev/null 2>&1
  ERROR=$?
  if [ $ERROR -gt 0 ]; then
    install_requirements
  fi
fi

source ${VENV_DIR}/bin/activate
make clean
make html
deactivate
