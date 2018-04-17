#!/usr/bin/bash

git pull
sudo pip install -r gear/requirements.txt
sudo python gear/export.py
sudo chmod 777 _data/*
git add .
git commit -m 'update ping test'
git push