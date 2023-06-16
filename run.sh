#!/bin/bash

# Check if lxml is installed
if ! python3 -c 'import lxml' &> /dev/null; then
    echo "lxml not found. Installing..."
    pip install lxml
    echo "lxml installed successfully."
fi
command python3 XmlToCsvConvertor.py $1 $2
