#!/usr/bin/bash

git pull
sudo -H pip install -r gear/requirements.txt
sudo -H python gear/export.py
sudo -H chmod 777 _data/*
git add .
git commit -m 'update ping test'
git push