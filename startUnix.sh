#!/bin/bash

# quick starting script
echo ""
echo "======= Starting ======="
echo "Open @ http://localhost:8080"
echo "========================"
echo "Run with -v to get all logging output"
#start Flask api
cd api
export FLASK_APP=api.py
if [ "$1" == "-v" ] ;
then
    python3 -m flask run &
else
    python3 -m flask run &> /dev/null &
fi

FLASK_PID=$!

function killFlask {
    kill $FLASK_PID
}

trap killFlask EXIT

#start d3js websever
if [ "$1" == "-v" ] ;
then
    cd ../ui && python3 -m http.server 8080 
else
    cd ../ui && python3 -m http.server 8080 &> /dev/null 
fi