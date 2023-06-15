#!/bin/bash

csv_file="data/csvs/final.csv"
output_directory="data/htmls"

mkdir -p "$output_directory"

while IFS="," read -r address filename; do
    # Remove leading/trailing whitespace from the address and filename
    address=$(echo "$address" | awk '{$1=$1};1')
    filename=$(echo "$filename" | awk '{$1=$1};1')

    # Construct the output file path
    output_path="$output_directory/$filename"

    # Download the HTML content using cURL and save it to the output file
    curl -sS "$address" > "$output_path"

    # Check the file size after downloading
    file_size=$(stat -c %s "$output_path")
    if [ "$file_size" -eq 0 ]; then
        echo "Error: Webpage '$address' doesn't exist or couldn't be downloaded."
        rm "$output_path"  # Remove the empty file
    else
        echo "Downloaded $filename"
    fi
done < "$csv_file"