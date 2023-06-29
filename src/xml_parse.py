import sys
import os
from pathlib import Path
import logging
from bs4 import BeautifulSoup as bs
import csv
import time
from datetime import datetime as dt

# Command line arguments
PROJECT_PATH = sys.argv[1]
WEBSITE_NAME = sys.argv[2]

# Get the xml folder
xmls_folder = os.path.join(PROJECT_PATH, "data", WEBSITE_NAME, "xmls")

# Get the csvs folder
urls_folder = os.path.join(PROJECT_PATH, "data", WEBSITE_NAME, "csvs", "urls")

def add_xml_to_csv(xml_filepath, output_csv_filepath, known_rows):
    logging.debug(f"Parsing xml file {xml_filepath}")

    content = []
    with open(xml_filepath, "r") as f_xml:
        content = f_xml.readlines()
    content = "".join(content)
    bs_content = bs(content, "xml")

    url_tags = bs_content.find_all("url")

    for url_tag in url_tags:

        url = url_tag.find("loc").text
        lastmod = url_tag.find("lastmod").text
        filename = url.split("/")[-2]

        new_row = [url, filename + ".html", lastmod, time.time()]
        
        row_to_add = get_correct_row(new_row, known_rows)

        with open(output_csv_filepath, "a") as f_csv:
            writer = csv.writer(f_csv)
            writer.writerow(row_to_add)

def get_correct_row(new_row, known_rows):
    for index, other_row in enumerate(known_rows):
        if new_row[0] == other_row[0]:
            new_row_date = dt.strptime(new_row[2], "%Y-%m-%d")
            other_row_date = dt.strptime(other_row[2], "%Y-%m-%d")
            if new_row_date <= other_row_date:
                return known_rows[index]
            else:
                return new_row
    return new_row

# Returns true if it can find any .xml file in xml_folder
def xmls_exist():
    for file_name in os.listdir(xmls_folder):
        if file_name.endswith(".xml"): 
            return True
    return False

def update_known_rows(csv_file_path, curr_known_rows):

    new_curr_known_rows = curr_known_rows
    csv_file_rows = []

    if os.path.exists(csv_file_path):
        with open(csv_file_path, "r") as f_csv:
            reader = csv.reader(f_csv)
            csv_file_rows.extend(reader)

    curr_known_urls = [curr_known_row[0] for curr_known_row in new_curr_known_rows]
    for index, csv_file_row in enumerate(csv_file_rows):
        if csv_file_row[0] in curr_known_urls:
            continue
        else:
            new_curr_known_rows.append(csv_file_row)

    return new_curr_known_rows

# Function call add_xml_to_csv if any xml files exist
def create_product_urls_csv():
    
    if xmls_exist():

        urls_csv_file_path = os.path.join(urls_folder, "product_urls.csv")

        for index, xml_file_name in enumerate(os.listdir(xmls_folder)):

            if index == 0:

                # Add the rows of the existing csv file to our currently known rows
                known_rows = update_known_rows(urls_csv_file_path, [])

                Path(urls_folder).mkdir(parents=True, exist_ok=True)
                with open(urls_csv_file_path, "w"):
                    pass 

            else:
                known_rows = update_known_rows(urls_csv_file_path, known_rows)

            add_xml_to_csv(xml_filepath=            os.path.join(xmls_folder, xml_file_name), 
                           output_csv_filepath=     urls_csv_file_path,
                           known_rows=              known_rows)
        
    # In case we have no xml files, let's log an error
    else:
        logging.error(f"XML files do not exist, cannot generate product_urls.csv for {WEBSITE_NAME}")

    current_rows  = []
    with open(urls_csv_file_path, "r") as f_csv:
        reader = csv.reader(f_csv)
        current_rows.extend(reader)
    for known_row, curr_row in zip(known_rows, current_rows):
        if known_row[3] != curr_row[3]:
            print("diff between")
            print(known_row)
            print(curr_row)
            print()

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    create_product_urls_csv()