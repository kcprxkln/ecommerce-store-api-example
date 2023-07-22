#!/bin/bash

log_file="./api_requests.log"
max_lines=10000

if [ -f "$log_file" ]; then
    current_lines=$(wc -l < "$log_file")
    lines_to_remove=$((current_lines - max_lines))

    if [ "$lines_to_remove" -gt 0 ]; then
        tail -n "$lines_to_remove" "$log_file" > "$log_file.tmp"
        mv "$log_file.tmp" "$log_file"
    fi
else
    echo "Log file not found: $log_file"
fi