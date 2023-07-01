"""
This script updates the product_urls.csv file to contain the latest and
newest URLs to all webpages in the website.

The downloaded .xml files contain a bunch of <url> tags.
Every <url> tag contains a <loc> tag and a <lastmod> tag.
Inside the <loc> tag we can find an URL to one of the many webapges in the
website.
Inside the <lastmod> tag we can find that date of when that webpage was 
last modified. Everytime we see that a webpage was updated, we update
the corresponding timestamp in the product_urls.csv file.

This is what allows the html_download.py script to be more efficient in its
processes.

Usage is:
$ python3 xml_parse.py path/to/project/here website_name
"""

import sys
import os
from pathlib import Path
from bs4 import BeautifulSoup as bs
import csv
import time
from datetime import datetime as dt

def add_xml_to_csv(xml_filepath, output_csv_filepath, known_rows):
    """
    Given the path to an xml file, updates the product_urls.csv file with the
    contents of that xml file whilst taking into account previous versions of
    the product_urls.csv file.

    Args:
        Path to the .xml file, path to the product_urls.csv file, list of 
        previously/currently known rows

    Returns:
        void
    """

    logger.debug(f"Adding to product_urls.csv the URLs from {xml_filepath.split('/')[-1]}")

    # Get the contents of the .xml file.
    content = []
    with open(xml_filepath, "r") as f_xml:
        content = f_xml.readlines()
    content = "".join(content)
    bs_content = bs(content, "xml")

    # Find all <url> tags of the .xml file.
    url_tags = bs_content.find_all("url")

    # For each <url> tag, create a list of what that <url> tag would look like
    # in the product_urls.csv file, and decide if that should be added 
    # to the product_urls.csv file via the get_correct_row function.
    for url_tag in url_tags:

        url = url_tag.find("loc").text
        lastmod = url_tag.find("lastmod").text
        filename = url.split("/")[-2]

        new_row = [url, filename + ".html", lastmod, time.time()]
        
        # Decides if the new_row list should be appended to product_urls.csv or, 
        # if an older version of that new_row list already exists in our list of 
        # known rows, if that older version should be added instead.
        row_to_add = get_correct_row(new_row, known_rows)

        # Adds the correct row to product_urls.csv.
        with open(output_csv_filepath, "a") as f_csv:
            writer = csv.writer(f_csv)
            writer.writerow(row_to_add)
    
    logger.info(f"Done parsing XML file {xml_filepath.split('/')[-1]}")

def get_correct_row(new_row, known_rows):
    """
    Given a potential new row and a list of previously/currently known rows of
    product_urls.csv, decides if the new row should be added, or if a previously
    (or currently) known row should be added instead.
    
    Args:
        The new row (as a list), the list of previously known rows

    Returns:
        The correct row (list) to be added
    """

    logger.debug(f"Deciding what to do with new_row {new_row[1]}")

    # If the new row exists in our list of known rows and its lastmod is newer
    # than the corresponding lastmod of the existing row in our known rows, 
    # return the new row. 
    # If the new row exists in our list of known rows, but it is not newer, 
    # return the old row. 
    # If the new row does not exist in our list of known rows, return the new row.
    for index, other_row in enumerate(known_rows):
        if new_row[0] == other_row[0]:
            new_row_date = dt.strptime(new_row[2], "%Y-%m-%d")
            other_row_date = dt.strptime(other_row[2], "%Y-%m-%d")
            if new_row_date <= other_row_date:
                logger.debug(f"new_row already exists, adding old row")
                return known_rows[index]
            else:
                logger.debug(f"new_row already exists, but has been modified. Adding {new_row[1]}")
                return new_row
    logger.debug(f"new_row does not exist, adding it")
    return new_row

def xmls_exist():
    """
    Returns True if .xml files exist in the xmls_folder, else False.

    Args:
        void
    
    Returns:
        bool
    """

    for file_name in os.listdir(xmls_folder):
        if file_name.endswith(".xml"): 
            return True
    return False

def update_known_rows(csv_file_path, curr_known_rows):
    """
    Given a list of previously (or currently) known rows of product_urls.csv,
    and a new version of product_urls.csv, updates the list of previously
    known rows with the contents of the new product_urls.csv.

    Args:
        Path to product_urls.csv, list of previously/currently known rows

    Returns:
        Updated list of previously/currently known rows
    """
    
    logger.debug("Updating list of known rows")

    # If a new product_urls.csv exists, save its contents.
    csv_file_rows = []
    if os.path.exists(csv_file_path):
        with open(csv_file_path, "r") as f_csv:
            reader = csv.reader(f_csv)
            csv_file_rows.extend(reader)

    # For every row in the new product_urls.csv, if it is not in out list of
    # currently known rows, append it.
    new_curr_known_rows = curr_known_rows
    curr_known_urls = [curr_known_row[0] for curr_known_row in new_curr_known_rows]
    for index, csv_file_row in enumerate(csv_file_rows):
        if csv_file_row[0] in curr_known_urls:
            continue
        else:
            logger.debug(f"Added to known rows {csv_file_row[1]}")
            new_curr_known_rows.append(csv_file_row)

    return new_curr_known_rows

def create_product_urls_csv():
    """
    Updates the contents of product_urls.csv by parsing every existing xml file.

    Args:
        void

    Returns:
        void
    """
    
    logger.info(f"Starting XML parse of {WEBSITE_NAME}")

    if xmls_exist():

        urls_csv_file_path = os.path.join(urls_folder, "product_urls.csv")

        for index, xml_file_name in enumerate(os.listdir(xmls_folder)):

            logger.info(f"Starting parse of {xml_file_name}")

            # If xml_file_name is the first file being parsed, we need to save
            # the contents of the current product_urls.csv (if it exists), and
            # then we can wipe out product_urls.csv.
            if index == 0:

                # Save the current contents of product_urls.csv.
                known_rows = update_known_rows(csv_file_path=   urls_csv_file_path, 
                                               curr_known_rows= [])

                # Wipe out product_urls.csv.

                logger.debug("Wiping out current version of product_urls.csv")

                Path(urls_folder).mkdir(parents=True, exist_ok=True)
                with open(urls_csv_file_path, "w"): pass 

            else:

                # Update our known csv file rows with the additions of the last
                # xml file that was parsed.
                known_rows = update_known_rows(csv_file_path=   urls_csv_file_path, 
                                               curr_known_rows= known_rows)

            # Update product_urls.csv with the contents of the next .xml file,
            # taking into account rows that we have previously known.
            add_xml_to_csv(xml_filepath=            os.path.join(xmls_folder, xml_file_name), 
                           output_csv_filepath=     urls_csv_file_path,
                           known_rows=              known_rows)
        
    else:
        logger.error(f"Could not find any XML files")
        return

    logger.info(f"Done parsing XMLs of {WEBSITE_NAME}")

if __name__ == "__main__":

    import logging
    import logging.config
    logging.config.fileConfig('./src/logging.conf')
    logger = logging.getLogger("xml_parse")

    # Command-line arguments.
    PROJECT_PATH = sys.argv[1]
    WEBSITE_NAME = sys.argv[2]

    # Getting the path to important folders
    xmls_folder = os.path.join(PROJECT_PATH, "data", WEBSITE_NAME, "xmls")
    urls_folder = os.path.join(PROJECT_PATH, "data", WEBSITE_NAME, "csvs", "urls")

    create_product_urls_csv()