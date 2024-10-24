#!/bin/bash

set -e

python3 server/server.py 8080 4 &

srv_pid=$!

python3 client/client.py 127.0.0.1:8080 client/note1.txt &
python3 client/client.py 127.0.0.1:8080 client/note2.txt &
python3 client/client.py 127.0.0.1:8080 client/note2.txt &
python3 client/client.py 127.0.0.1:8080 client/note4.txt &
python3 client/client.py 127.0.0.1:8080 client/note5.txt &
python3 client/client.py 127.0.0.1:8080 client/note6.txt &
python3 client/client.py 127.0.0.1:8080 client/note7.txt &
python3 client/client.py 127.0.0.1:8080 client/note8.txt &
python3 client/client.py 127.0.0.1:8080 client/note9.txt &
python3 client/client.py 127.0.0.1:8080 client/note10.txt &
python3 client/client.py 127.0.0.1:8080 client/note11.txt &

sleep 5

pids="$(pgrep -P $$)"

pkill -P $$

echo "$pids" > /tmp/kostil
first_child="$(sed -n 1p /tmp/kostil)"


if [ "$srv_pid" != "$pids" ]
then
    echo something went wrong
    exit 1
else
    echo all good
fi
