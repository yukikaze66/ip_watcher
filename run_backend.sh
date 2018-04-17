#!/bin/bash

git pull
pip install -r gear/requirements.txt
python gear/export.py
chmod 777 _data/*
git add .
git commit -m 'update ping test'
git config --global user.name "thiswind"
git config --global user.email thiswind@gmail.com
git config --global push.default simple
git push
