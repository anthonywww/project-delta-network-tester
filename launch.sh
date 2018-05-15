#!/bin/bash

# Set the directory to this script's current directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Default coords
x=0
y=0

# Apply parameters
if [ $# -eq 2 ]; then
	x=${1}
	y=${2}
fi

# Launch client
python3 src/client.py ${x} ${y}
