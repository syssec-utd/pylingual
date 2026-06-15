#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <python_version>"
    echo "Please provide a Python version (e.g., 3.14, 3.10, 3.8)"
    exit 1
fi

# Clear/create results file
> results.txt

# List test directory
echo "Files in test directory:"
ls test/
echo ""

# Iterate through each file in test directory
for file in test/*.py; do
    if [ -f "$file" ]; then
        # Extract module name (filename without path and extension)
        modname=$(basename "$file" .py)
        
        echo "Processing: $file"
        
        # Run cflow.py, grep for equivalence report lines, replace <module> with module name
        uv run dev_scripts/cflow.py "$file" --version "$1" | \
            grep '<module>' | \
            sed "s/<module>/$modname/g" >> results.txt
    fi
done

echo ""
echo "Results saved to results.txt"