#!/bin/bash

BREW="/usr/local/bin/brew"
if [ -e "$BREW" ]; then
    echo "HomeBrew already installed"
else
    echo "Installing HomeBrew"
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
fi

PYTHON="/usr/local/bin/python3.7"
if [ -e "$PYTHON" ]; then
    echo "Python3.7 already installed"
else
    echo "Installing Python3.7"
    brew install python3
fi

PIP="/usr/local/bin/pip3"
if [ -e "$PIP" ]; then
    echo "pip3 already installed"
else
    echo "Installing Python pip"
    python3 -m pip install pip
fi

echo "Installing virtualenv"
pip3 install virtualenv

git clone https://github.com/marina8888/chemkin-sensitivity-analysis.git

cd command-line-chemkin
virtualenv --python=python3 .
source bin/activate
pip install -r requirements.txt