#!/usr/bin/bash

git pull
sudo pip install -r requirements.txt
sudo python gear/export.py
sudo chmod 777 _data/*
git commit -m 'update ping test'
git push