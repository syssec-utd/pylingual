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
        
        # Run cflow.py, capture equivalence report lines, replace <module> with module name
        output=$(uv run dev_scripts/cflow.py "$file" --version "$1" 2>&1)
        
        # Check for module-level result lines
        module_lines=$(echo "$output" | grep '<module>')
        if [ -n "$module_lines" ]; then
            echo "$module_lines" | sed "s/<module>/$modname/g" >> results.txt
        else
            # No module lines means compile error - report module-level failure
            echo "$modname: Failure: CompileError" >> results.txt
        fi
    fi
done

echo ""
echo "Results saved to results.txt"