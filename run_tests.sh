#!/bin/sh

sudo python setup.py install
nosetests --with-doctest --with-coverage --cover-html --cover-package=fuzzyparsers --cover-tests --cover-erase --verbose
python -m doctest README.txt

xdg-open cover/index.html
