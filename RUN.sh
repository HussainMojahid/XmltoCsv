#!/bin/bash

if command -v python3 &>/dev/null; then

    command python3 XmlToCsvConvertor.py $1 $2
else

    echo "Python is not installed."
fi
