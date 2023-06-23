import json
from bs4 import BeautifulSoup as bs
import re
from js2py import eval_js
import logging
import sys
import os
from pathlib import Path

logging.getLogger().setLevel(logging.DEBUG)

PROJECT_PATH = sys.argv[1]
WEBSITE_NAME = sys.argv[2]

htmls_folder = os.path.join(PROJECT_PATH, "data", WEBSITE_NAME, "htmls")

raw_jsons_folder = os.path.join(PROJECT_PATH, "data", WEBSITE_NAME, "jsons", "raw")

def get_images(bs_content):
    # Get all of the images
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
    
    # We could technically stop here, and already do a json.loads(search_result)
    # The only reason we do all this below is to return a sorted dict, and also a dict inside a list
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

    logging.debug(f"Parsing html file {html_file_path}")

    with open(html_file_path, "r") as f_html:
        html_contents = f_html.read()

    bs_content = bs(html_contents, features="lxml")

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
    for file_name in os.listdir(htmls_folder):
        if file_name.endswith(".html"):
            return True
    return False

def not_404(html_file_path) -> bool:
    if os.stat(html_file_path).st_size > 157861:
        return True
    return False

def create_raw_jsons():

    if htmls_exist():
        # Create a folder to dump all of the raw jsons, if it doens't exist already
        Path(raw_jsons_folder).mkdir(parents=True, exist_ok=True)

        for html_file_name in os.listdir(htmls_folder):
            json_file_name = html_file_name.split(".")[0] + ".json"
            if not_404(os.path.join(htmls_folder, html_file_name)):
                parse_html_to_json(html_file_path=          os.path.join(htmls_folder, html_file_name),
                                   output_json_file_path=   os.path.join(raw_jsons_folder, json_file_name))

    # If we don't have any html files available, let us warn the developer
    else:
        logging.error(f"HTML files for {WEBSITE_NAME} do not exist, could not parse them")

if __name__ == "__main__":
    create_raw_jsons()