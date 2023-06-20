import os
import sys
import subprocess
from multiprocessing import Pool
from pathlib import Path
import logging

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

# Assign stop_at to command line argument 5, but if that is empty, assign a default value of 100
stop_at = int(sys.argv[5]) if len(sys.argv) > 5 else 100

# Usage: request_html(html_address, html_download_output_path)
def request_html(args):
    html_address, html_download_output_path = args

    # If the html file already exists and its size is large enough
    if os.path.exists(html_download_output_path) and os.stat(html_download_output_path).st_size > 157861:
        logging.error(f"O arquivo {html_download_output_path} existe e tem tamanho maior que 157861 bytes.")
    else:
        # Downloading file
        logging.debug(f"Requisitando {html_address}")
        subprocess.run(["curl", "-sS", "-x", proxy_credential, "-k", html_address, "-o", html_download_output_path])
        logging.debug(f"{html_download_output_path} [OK]")

def download_all_htmls():
    output_directory = os.path.join(PROJECT_PATH, "data", WEBSITE_NAME, "htmls")
    Path(output_directory).mkdir(parents=True, exist_ok=True)

    csv_file_path = os.path.join(PROJECT_PATH, "data", WEBSITE_NAME, "csvs", "product_urls.csv")

    iterations = 0
    jobs = []

    with open(csv_file_path, "r") as f_csv:
        for line in f_csv:
            url, desired_output_file_name = line.strip().split(',')

            desired_output_file_path = os.path.join(output_directory, desired_output_file_name)

            while len(jobs) >= max_simultaneous_requests:
                for job in jobs:
                    job.join(0.1)
                    if not job.is_alive():
                        jobs.remove(job)

            p = Pool(processes=1)
            p.apply_async(request_html, [(url, desired_output_file_path)])
            jobs.append(p)

            iterations += 1
            if iterations >= stop_at:
                break

    for job in jobs:
        job.join()

    logging.debug("Done downloading htmls")

if __name__ == "__main__":
    download_all_htmls()