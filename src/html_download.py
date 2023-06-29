import os
import sys
import subprocess
import csv
from pathlib import Path
import logging
import requests
import time

# Usage: python3 html_download.py proxy_credential PROJECT_PATH WEBSITE_NAME max_simultaneous_requests stop_at

# Making sure we have everything we need from the command line arguments
if len(sys.argv) < 4:
    logging.error("Usage: python3 html_download.py proxy_credential PROJECT_PATH WEBSITE_NAME max_simultaneous_requests stop_at")
    sys.exit(1)

# Assign proxy_credential to command line argument 1
proxy_credential = sys.argv[1]

# Assign PROJECT_PATH to command line argument 3
PROJECT_PATH = sys.argv[2]

# Assign WEBSITE_NAME to command line argument 2
WEBSITE_NAME = sys.argv[3]

# Assign maximum_simultaneous_requests to command line argument 4, but if that is empty, assign a default value of 15
max_simultaneous_requests = int(sys.argv[4]) if len(sys.argv) > 4 else 15

# Assign stop_at to command line argument 5, but if that is empty, assign a default value of 20
stop_at = int(sys.argv[5]) if len(sys.argv) > 5 else 20

def request_html(html_address, html_download_output_path):

    # If the html file already exists and its size is large enough
    if os.path.exists(html_download_output_path) and os.stat(html_download_output_path).st_size > 157861:
        logging.error(f"O arquivo {html_download_output_path} existe e tem tamanho maior que 157861 bytes.")
    else:
        # Downloading file
        logging.debug(f"Requisitando {html_address}")
        proxies = {"https": proxy_credential}
        response = requests.get(html_address, proxies=proxies, verify=False)
        with open(html_download_output_path, "wb") as f:
            f.write(response.content)
        logging.debug(f"{html_download_output_path} [OK]")

def download_all_htmls():
    output_directory = os.path.join(PROJECT_PATH, "data", WEBSITE_NAME, "htmls")
    Path(output_directory).mkdir(parents=True, exist_ok=True)

    csv_file_path = os.path.join(PROJECT_PATH, "data", WEBSITE_NAME, "csvs", "urls", "product_urls.csv")

    iterations = 0
    with open(csv_file_path, "r") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if iterations >= stop_at:
                break
            url, desired_output_file_name, timestamp = row[0], row[1], row[3]

            desired_output_file_path = os.path.join(output_directory, desired_output_file_name)

            while int(subprocess.run(["pgrep", "-c", "python3"], capture_output=True, text=True).stdout.strip()) >= max_simultaneous_requests:
                time.sleep(0.1)

            if os.path.exists(desired_output_file_path):
                if os.path.getmtime(desired_output_file_path) < float(timestamp):
                    request_html(html_address=url,
                                html_download_output_path=desired_output_file_path)
                else:
                    print(f"not requesting {desired_output_file_name}")
                    iterations += 1
                    continue
            else:
                request_html(html_address=url,
                            html_download_output_path=desired_output_file_path)

            iterations += 1

    logging.debug("Done downloading htmls")

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    download_all_htmls()