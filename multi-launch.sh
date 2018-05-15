#!/bin/bash

# Set the directory to this script's current directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Launch client
max_x=6
max_y=4

for x in $(seq 0 $max_x); do
	for y in $(seq 0 $max_y); do
		echo -e "Starting client [${x},${y}]..."
		python3 src/client.py ${x} ${y} &
	done
done
