#!/bin/bash

# Usage: nohup ./download_html_new.sh proxy_credential max_simultaneous_requests stop_at

# Assign proxy_credential to command line argument 1
proxy_credential=$1 

# Assign maximum_simultaneous_requests to command line argument 2, but if that is empty, assign a default value of 15
max_simultaneous_requests=${2:-15}

# Assign stop_at to command line argument 3, but if that is empty, assign a default value of 100
stop_at=${3:-100}

# Assign output_directory to command line argument 4, but if that is empty, assign a default value of "data/htmls"
output_directory="temp_data/htmls"

csv_file="car_parts_scrap/data/csvs/final.csv"

# Making sure proxy_credential is provided in the command line argument
if [ -z "$proxy_credential" ]; then
    echo "Informe o proxy_credential"
    echo "Usage: nohup ./download_html_new.sh proxy_credential max_simultaneous_requests stop_at"
    exit 1
fi

# Usage: request_html html_address html_download_output_path
request_html() {
    html_address=$1
    html_download_output_path=$2

    # If the html file already exists and its size is large enough
    if [ -e "$html_download_output_path" ] && [ $(stat -c %s "$html_download_output_path") -gt 157861 ]; then
        echo "O arquivo $html_download_output_path existe e tem tamanho maior que 157861 bytes."
    # If the html file already exists
    elif [ -e "$html_download_output_path" ]; then
        if grep -q "An error occurred in the application and your page could not be served" "$html_download_output_path"; then
            echo "O arquivo $html_download_output_path contém um item INEXISTENTE."
        fi
        # If some Amazon stuff I don't quite get went wrong, re-download the file
        if grep -q "The Amazon CloudFront distribution is configured to block access from your country" "$html_download_output_path"; then
            echo "O arquivo $html_download_output_path contém um item BLOQUEADO."
			echo "Requisitando $html_download_output_path"
            curl -sS -x "$proxy_credential" -k "$html_address" > "$html_download_output_path"
        fi
    else
        # Downloading file
		echo "Requisitando $html_address"
        curl -sS -x "$proxy_credential" -k "$html_address" > "$html_download_output_path"
    fi
}

# Looping the CSV file and obtaining the html addresseses and the desired output file names
iterations=0
while IFS="," read -r address filename && [ "$iterations" -lt "$stop_at" ]; do

    # Removing any white space
    html_address=$(echo "$address" | awk '{$1=$1};1')
    output_file_name=$(echo "$filename" | awk '{$1=$1};1')

    # Creating the output file path, that is under a specified directory
    html_download_output_path="$output_directory/$output_file_name"

    # Making sure to sleep if we reach the maximum number of jobs
    while [ $(jobs -r | wc -l) -ge $max_simultaneous_requests ]; do
        sleep 0.1
    done

    # We are not sleeping, so let's create a new job to download html content

    request_html "$html_address" "$html_download_output_path" &

    iterations=$((iterations + 1))
done < "$csv_file"

# Yeah just waiting stuff to finish downloading
wait


