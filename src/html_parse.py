"""
Given any downloaded html files, parses them to create raw JSON files which
contain interesting data to us.

Usage:
$ python3 html_parse.py path/to/project/here website_name
"""

import json
from bs4 import BeautifulSoup as bs
import re
from js2py import eval_js
import sys
import os
from pathlib import Path
import pickle

def get_images(bs_content):
    ul_element = bs_content.find("ul", {"class":"thumbs"})
    img_elements = bs_content.find_all("a", {"id":"botaoZoom"})
    images = []
    for image in img_elements:
        images.append(image["zoom"])
    return images

def get_caracteristics(bs_content):
    classes = ["TIPO-DE-PRODUTO", "QUANTIDADE-POR-EMBALAGEM", "COR", "PESO-APROXIMADO", "DIMENSOES-DO-PRODUTO", "DIMENSOES-DA-EMBALAGEM", "GARANTIA"]
    CARACTERISTICAS = {}
    for class_name in classes:
        CARACTERISTICAS[class_name] = found.text if (found := bs_content.find("td", {"class": class_name})) else "n/a"
    CARACTERISTICAS = [CARACTERISTICAS]
    return CARACTERISTICAS

def get_specifications(bs_content):
    classes = ["ESPECIFICACOES-TECNICAS", "INDICACOES", "CONTRA-INDICACOES"]
    tds = {}
    for class_name in classes:
        tds[class_name] = found.text if (found := bs_content.find("td", {"class": class_name})) else "n/a"
    tds = [tds]
    return tds

def regex_to_json_dict(html_content: str, regex_pattern: str) -> dict:
    if (match := re.search(regex_pattern, html_content)):
        search_result = match.group(1)
    else:
        search_result = {"n/a": "n/a"}
    
    # We could technically stop here, and already do a json.loads(search_result).
    # The only reason we do all this below is to return a sorted dict that is 
    # also inside a list.
    # I guess you could also argue for some JSON error checking with 
    # the try-except.

    js_code = f"""
        var result = {search_result};
        JSON.stringify(result);
    """
    json_string = eval_js(js_code)

    if json_string:
        try:
            data = json.loads(json_string)
            if isinstance(data, list):
                return data
            else:
                return [data]
        except json.JSONDecodeError:
            return None
    else:
        return None

def parse_html_to_json(html_file_path, output_json_file_path):
    """
    Creates the raw JSON version of an HTML file by parsing it, given the path
    to a downloaded HTML file and a path to save the raw JSON.

    Args:
        Path to the downloaded HTML file, path to save the generated raw JSON

    Returns:
        void
    """

    # Give the contents of the downloaded HTML file to bs4.
    with open(html_file_path, "r") as f_html:
        html_contents = f_html.read()
    bs_content = bs(html_contents, features="lxml")

    """
    I've taken a bit liberty in the following steps.
    There's really not a right way of doing it, and I'm sure that I can still 
    make improvements. 
    However, this is such a boring process to document and structure that 
    I'll just leave it like this.
    At least everything is compartmentalized in functions, so that should make
    it easier to follow through.
    """

    skuJson_0_pattern = r'var skuJson_0 = ({.+});CATALOG'
    vtxctx_pattern = r'vtxctx = ({.+});</script'
    vtex_events_addData_pattern = r'<script>\nvtex.events.addData\(({.+})\);\n</script>'

    itemprop_pattern = r'<meta itemprop="description" content="(.+)" \/><meta itemprop="url" '
    itemprop = found.group(1) if (found := re.search(itemprop_pattern, html_contents)) else "n/a"

    data = {
        "CARACTERISTICAS":                      get_caracteristics(bs_content),
        "ESPECIFICACOES":                       get_specifications(bs_content),
        "skuJson_0":                            regex_to_json_dict(html_contents, skuJson_0_pattern),
        "vtxctx":                               regex_to_json_dict(html_contents, vtxctx_pattern),
        "vtex.events.addData":                  regex_to_json_dict(html_contents, vtex_events_addData_pattern),
        "itemprop":                             itemprop,
        "images":                               get_images(bs_content),
    }
    
    with open(output_json_file_path, "w") as f_json:
        json.dump(data, f_json, indent=4, ensure_ascii=False)

def htmls_exist():
    """
    Returns True if any HTML files exist, else False.

    Args:
        void

    Returns:
        bool
    """

    for file_name in os.listdir(htmls_folder):
        if file_name.endswith(".html"):
            return True
    return False

def not_404(html_file_path) -> bool:
    """
    Returns True if the HTML file located at the provided path is larger
    than 157861 bytes, else False.

    Args:
        Path to a downloaded HTML file
    
    Returns:
        bool
    """

    if os.stat(html_file_path).st_size > 157861:
        return True
    return False

def create_raw_jsons():
    """
    For every downloaded HTML file, if it did not 404, parse it using the
    parse_html_to_json function to generate a raw JSON.
    
    Args:
        void

    Returns:
        void
    """

    if htmls_exist():

        # Create a folder to dump all of the raw jsons, if it doesn't exist already.
        Path(raw_jsons_folder).mkdir(parents=True, exist_ok=True)

        # Get the list of HTML files that have changed
        with open(os.path.join(PROJECT_PATH, "data", WEBSITE_NAME, "pickles", "requested.pkl"), "rb") as f_pkl:
            changed = pickle.load(f_pkl)

        # Loop through every downloaded HTML file. If it did not 404 and 
        # it changed, parse it to generate a raw JSON file.
        for html_file_name in os.listdir(htmls_folder):

            if not_404(os.path.join(htmls_folder, html_file_name)) and html_file_name in changed:
                json_file_name = html_file_name.split(".")[0] + ".json"
                parse_html_to_json(html_file_path=          os.path.join(htmls_folder, html_file_name),
                                   output_json_file_path=   os.path.join(raw_jsons_folder, json_file_name))

    # If we don't have any html files available, let us warn the developer.
    else:
        # log an error
        pass

if __name__ == "__main__":
    
    # Command-line arguments.
    PROJECT_PATH = sys.argv[1]
    WEBSITE_NAME = sys.argv[2]

    # Getting the path to important folders.
    htmls_folder = os.path.join(PROJECT_PATH, "data", WEBSITE_NAME, "htmls")
    raw_jsons_folder = os.path.join(PROJECT_PATH, "data", WEBSITE_NAME, "jsons", "raw")

    create_raw_jsons()