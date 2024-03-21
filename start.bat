@echo off
start cmd /k "conda activate tmining && cd ./backend && python main.py host"
start cmd /k "cd ./client && npm start"