import logging
import os
import csv 
import requests
import sys
from pathlib import Path
import subprocess
import time

# Usage: python3 photo_download.py proxy_credential PROJECT_PATH WEBSITE_NAME max_simultaneous_requests stop_at

# Making sure we have everything we need from the command line arguments
if len(sys.argv) < 4:
    logging.error("Usage: python3 photo_download.py proxy_credential PROJECT_PATH WEBSITE_NAME max_simultaneous_requests stop_at")
    sys.exit(1)

# Assign proxy_credential to command line argument 1
proxy_credential = sys.argv[1]

# Assign PROJECT_PATH to command line argument 3
PROJECT_PATH = sys.argv[2]

# Assign WEBSITE_NAME to command line argument 2
WEBSITE_NAME = sys.argv[3]

# Assign maximum_simultaneous_requests to command line argument 4, but if that is empty, assign a default value of 15
max_simultaneous_requests = int(sys.argv[4]) if len(sys.argv) > 4 else 15

# Assign stop_at to command line argument 5, but if that is empty, assign a default value of 100
stop_at = int(sys.argv[5]) if len(sys.argv) > 5 else 21783

def request_photo(photo_address, photo_download_output_path):

    if os.path.exists(photo_download_output_path) and os.stat(photo_download_output_path).st_size > 157861:
        logging.error(f"O arquivo {photo_download_output_path} existe e tem tamanha maior que 157861 bytes.")
    else:
        logging.debug(f"Requisitando {photo_address}")
        proxies = {"https": proxy_credential}
        response = requests.get(photo_address, proxies=proxies, verify=False)
        with open(photo_download_output_path, "wb") as f:
            f.write(response.content)
        logging.debug(f"{photo_download_output_path} [OK]")

def download_all_photos():
    output_directory = os.path.join(PROJECT_PATH, "data", WEBSITE_NAME, "fotos")
    Path(output_directory).mkdir(parents=True, exist_ok=True)

    csv_file_path = os.path.join(PROJECT_PATH, "data", WEBSITE_NAME, "csvs", "fotos.csv")

    iterations = 0
    with open(csv_file_path, "r") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            if iterations >= stop_at:
                break
            url, desired_output_file_path = row

            desired_output_file_path = os.path.join(PROJECT_PATH, desired_output_file_path)

            while int(subprocess.run(["pgrep", "-c", "python3"], capture_output=True, text=True).stdout.strip()) >= max_simultaneous_requests:
                time.sleep(0.1)

            request_photo(photo_address=url,
                         photo_download_output_path=desired_output_file_path)

            iterations += 1

    logging.debug("Done downloading photos")

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    download_all_photos()