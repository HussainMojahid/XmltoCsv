#!/bin/bash

# Check if xmltocsvConvertor is present
if [ ! -d "xmltocsvConvertor" ]; then
    echo "xmltocsvConvertor not found. Creating it..."
    mkdir xmltocsvConvertor
    chmod +x xmltocsvConvertor
    echo "xmltocsvConvertor created successfully."
fi

if  [  -d "xmltocsvConvertor" ]; then

    cd xmltocsvConvertor
    # Check if repository is cloned
    if [ ! -d "XmltoCsv" ]; then
        echo "Cloning XmltoCsv repository..."
        git clone https://github.com/HussainMojahid/XmltoCsv.git
    fi

    # Move into the repository directory
    cd XmltoCsv
    # Checkout updatedCode branch
    echo "Checking out updatedCode branch..."
    git checkout UpdatedCode

    # Check if lxml is installed
    if ! python3 -c 'import lxml' &> /dev/null; then
        echo "lxml not found. Installing..."
        pip install lxml
        echo "lxml installed successfully."
    fi
    command python3 XmlToCsvConvertor.py $1 $2
fi
