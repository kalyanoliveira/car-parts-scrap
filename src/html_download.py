"""
Using product_urls.csv, downloads/redownloads the HTMLs of all product webpages
in a website as needed.

Usage is:
$ python3 html_download.py proxy_credential path/to/project/here website_name max_simultaneous_requests stop_at
"""

import os
import sys
import subprocess
import csv
from pathlib import Path
import requests
import time
import pickle

def request_html(html_address, html_download_output_path):
    """
    Given the URL to an HTML and a path to save it to, downloads that file 

    Args:
        URL to the HTML file to request, path to location to save download
    
    Returns:
        void
    """

    logger.info(f"Requesting {html_address}")

    # Create a request to the URL of the HTML file, and save the response
    # contents to the correct path.
    proxies = {"https": proxy_credential}
    if proxy:
        response = requests.get(html_address, proxies=proxies, verify=False)
    else:
        response = requests.get(html_address, verify=False)
    with open(html_download_output_path, "wb") as f_html:
        f_html.write(response.content)

    logger.info(f"Saved to {html_download_output_path}")

    requested_webpages.append(html_download_output_path.split("/")[-1])

def download_all_htmls():
    """
    Using the URLs and timestamps in product_urls.csv, downloads all HTML files
    of the website as necessary.

    Args:
        void
    
    Returns:
        void
    """

    logger.info(f"Starting HTML download of {WEBSITE_NAME}")

    # Create a directory to store all downloaded HTML files.
    output_directory = os.path.join(PROJECT_PATH, "data", WEBSITE_NAME, "htmls")
    Path(output_directory).mkdir(parents=True, exist_ok=True)

    # Get the path to product_urls.csv.
    csv_file_path = os.path.join(PROJECT_PATH, "data", WEBSITE_NAME, "csvs", "urls", "product_urls.csv")

    # Loop through each line of product_urls.csv.
    # If the specified HTML for a line already exists, check the timestamp in
    # that line and the last modified data of the HTML file. 
    # If the HTML file is older than the timestamp, re-download it.
    iterations = 0
    with open(csv_file_path, "r") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:

            # We add a hard stop to the download process here, just in case we 
            # want to debug stuff.
            if iterations >= stop_at:
                break
            
            # Each line in product_urls.csv has a URL, a FILENAME, a LASTMOD, 
            # and a TIMESTAMP.
            url, desired_output_file_name, timestamp = row[0], row[1], row[3]
            desired_output_file_path = os.path.join(output_directory, desired_output_file_name)

            logger.debug(f"Currently looking at product_urls.csv line of {desired_output_file_name}")

            # If we are trying to download more than 15 HTML files at once, wait
            # until one of them is done.
            while int(subprocess.run(["pgrep", "-c", "python3"], capture_output=True, text=True).stdout.strip()) >= max_simultaneous_requests:
                time.sleep(0.1)

            # If the HTML file specified in the URL is already downloaded, we 
            # need to compare the date that it was last modified with the 
            # timestamp of when the URL in the product_urls.csv was added.
            # This allows us to know if we need to re-download the HTML file.
            if os.path.exists(desired_output_file_path):
                if os.path.getmtime(desired_output_file_path) < float(timestamp):
                    logger.debug("File already exists and is older than timestamp in product_urls.csv")
                    request_html(html_address=              url, 
                                 html_download_output_path= desired_output_file_path)
                else:
                    logger.debug("File already exists and is newer than timestamp in product_urls.csv")
                    iterations += 1
                    continue
            else:
                logger.debug("File does not exist")
                request_html(html_address=              url, 
                             html_download_output_path= desired_output_file_path)

            iterations += 1

if __name__ == "__main__":

    import logging
    import logging.config
    logging.config.fileConfig('./src/logging.conf')
    logger = logging.getLogger("html_download")
    
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    # Command-line arguments.
    if len(sys.argv) < 4:
        # log an error, improper usage
        sys.exit(1)
    # Assign proxy_credential to command line argument 1.
    proxy_credential = sys.argv[1]
    # Assign PROJECT_PATH to command line argument 3.
    PROJECT_PATH = sys.argv[2]
    # Assign WEBSITE_NAME to command line argument 2.
    WEBSITE_NAME = sys.argv[3]
    # Assign maximum_simultaneous_requests to command line argument 4, but if 
    # that is empty, assign a default value of 15.
    max_simultaneous_requests = int(sys.argv[4]) if len(sys.argv) > 4 else 15
    # Assign stop_at to command line argument 5, but if that is empty, assign 
    # a default value of 20.
    stop_at = int(sys.argv[5]) if len(sys.argv) > 5 else 20

    proxy = False

    if not proxy:
        logger.warning("Not using a proxy")

    requested_webpages = []

    download_all_htmls()

    pickles_dir = os.path.join(PROJECT_PATH, "data", WEBSITE_NAME, "pickles")
    Path(pickles_dir).mkdir(parents=True, exist_ok=True)
    with open(os.path.join(pickles_dir, "requested.pkl"), "wb") as f_pickle:
        pickle.dump(requested_webpages, f_pickle)