import sys
import os
from pathlib import Path
import logging
from bs4 import BeautifulSoup as bs

# Command line arguments
PROJECT_PATH = sys.argv[1]
WEBSITE_NAME = sys.argv[2]

# Get the xml folder
xmls_folder = os.path.join(PROJECT_PATH, "data", WEBSITE_NAME, "xmls")

# Get the csvs folder
csvs_folder = os.path.join(PROJECT_PATH, "data", WEBSITE_NAME, "csvs")

def add_xml_to_csv(xml_filepath, output_csv_filepath):
    logging.debug(f"Parsing xml file {xml_filepath}")

    content = []
    with open(xml_filepath, "r") as f_xml:
        content = f_xml.readlines()
    content = "".join(content)
    bs_content = bs(content, "xml")

    locs = bs_content.find_all("loc")
    urls = []
    for loc in locs:
        urls.append(loc.text)
    filenames = [url.split("/")[-2] for url in urls]

    with open(output_csv_filepath, "a") as f_csv:
        for url, filename in zip(urls, filenames):
            string = f"{url},{filename}.html\n"
            f_csv.write(string) 

# Returns true if it can find any .xml file in xml_folder
def xmls_exist():
    for file_name in os.listdir(xmls_folder):
        if file_name.endswith(".xml"): 
            return True
    return False

# Function call add_xml_to_csv if any xml files exist
def create_product_urls_csv():
    
    if xmls_exist():

        # Clear the existing product_urls.csv
        Path(csvs_folder).mkdir(parents=True, exist_ok=True)
        with open(os.path.join(csvs_folder, "product_urls.csv"), "w"):
            pass 

        # Parse each xml file in xml_folder
        for xml_file in os.listdir(xmls_folder):
            add_xml_to_csv(xml_filepath = os.path.join(xmls_folder, xml_file), 
                           output_csv_filepath = os.path.join(csvs_folder, "product_urls.csv"))

    # In case we have not xml files, let's log an error
    else:
        logging.error(f"XML files do not exist, cannot generate product_urls.csv for {WEBSITE_NAME}")


if __name__ == "__main__":
    create_product_urls_csv()