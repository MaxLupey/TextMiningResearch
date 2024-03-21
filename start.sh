#!/bin/bash

source activate tmining
cd ./backend
python main.py host &

cd ../client
npm start &

cleanup() {
    echo -e " "
    echo -e "Stopping Flask Server and React App..."
    pkill -P $$ python
    pkill -P $$ npm
    
    exit 0
}

trap cleanup INT
wait

