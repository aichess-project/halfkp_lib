#!/bin/bash

# Set the path of the directory you want to add to PYTHONPATH
directory_to_add="/Users/littlecapa/GIT/python/halfkp_research"

# Check if the directory exists
if [ -d "$directory_to_add" ]; then
    # Add the directory to PYTHONPATH if it exists
    export PYTHONPATH="$directory_to_add:$PYTHONPATH"
    echo "Directory added to PYTHONPATH: $directory_to_add"
    echo "$PYTHONPATH"
else
    # Display an error message if the directory does not exist
    echo "Error: Directory does not exist - $directory_to_add"
fi
