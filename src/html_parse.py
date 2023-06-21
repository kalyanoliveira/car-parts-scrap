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

# Does cool stuff
def parse_html_to_json(html_file_path, output_json_file_path):

    logging.debug(f"Parsing html file {html_file_path}")

    # # Get the html content of the html file in html_file_path
    # content = []
    # with open(html_file_path, "r") as f_html:
    #     content = f_html.readlines()
    # content = "".join(content)
    # bs_content = bs(content, features="lxml")

    # # Find all possible <script> tags in that content
    # scripts = bs_content.find_all('script')

    # # For each script tag, evaluate the following regex
    # # Append true evaluations to the array "potentials"
    # pattern = r'var skuJson_0 = ({.*});CATALOG_SDK.setProductWithVariationsCache\(skuJson_0.productId, skuJson_0\); var skuJson = skuJson_0;'
    # potentials = []
    # for script in scripts:
    #     if (match := re.match(pattern, script.text)):
    #         potentials.append(match.group(1))

    # # If we get more than one true regex evaluation, something went wrong
    # if len(potentials) != 1:
    #     print("Found more than one regex pattern, saving some random stuff into the json")
    #     random_data = {"hi":"how are you doing"}
    #     with open(output_json_file_path, "w") as f_json:
    #         json.dump(random_data, f_json, indent=4, ensure_ascii=False)
    #         logging.error(f"Error in parsing of {html_file_path}: found more than one regex pattern")
    #         return
    
    # # If we get just one true regex evaluation, that means that we have the json contents we need
    # # Let's save those here
    # true_potential = potentials[0]

    # # I have no idea what this exactly does, but
    # # the input is the regex string
    # # the output is the dictionary of the regex string
    # # and I know how to convert a python dictionary to a JSON, so we good
    # js_code = f'''
    #     var result={true_potential};
    #     JSON.stringify(result);
    # '''
    # variable_value = eval_js(js_code)
    # data = json.loads(variable_value)
    
    # type_of_product = bs_content.find('td', {"class": "TIPO-DE-PRODUTO"})
    # if type_of_product: 
    #     type_of_product = type_of_product.text
    #     data["item_type"] = type_of_product

    # color = bs_content.find('td', {"class": "COR"})
    # if color: 
    #     color = color.text
    #     data["color"] = color

    # quantity_per_package = bs_content.find('td', {"class": "QUANTIDADE-POR-EMBALAGEM"})
    # if quantity_per_package: quantity_per_package = quantity_per_package.text

    # mass = bs_content.find('td', {"class": "PESO-APROXIMADO"})
    # if mass: 
    #     mass = mass.text
    #     data["mass"] = mass

    # product_dimensions = bs_content.find('td', {"class": "DIMENSOES-DO-PRODUTO"})
    # if product_dimensions: 
    #     product_dimensions = product_dimensions.text
    #     data["product_dimensions"] = product_dimensions

    # package_dimensions = bs_content.find('td', {"class": "DIMENSOES-DA-EMBALAGEM"})
    # if package_dimensions: 
    #     package_dimensions = package_dimensions.text
    #     data["package_dimensions"] = package_dimensions

    # compatibility = bs_content.find('td', {"class": "Modelo"})
    # if compatibility: 
    #     compatibility = compatibility.text
    #     data["compatibility"] = compatibility

    # mpn = bs_content.find("div", {"class": "skuReference"})
    # if mpn:
    #     data["mpn"] = mpn.text

    # with open(output_json_file_path, "w") as f_json:
    #     json.dump(data, f_json, indent=4, ensure_ascii=False)

def htmls_exist():
    for file_name in os.listdir(htmls_folder):
        if file_name.endswith(".html"):
            return True
    return False

def create_raw_jsons():

    if htmls_exist():
        # Create a folder to dump all of the raw jsons, if it doens't exist already
        Path(raw_jsons_folder).mkdir(parents=True, exist_ok=True)

        for html_file_name in os.listdir(htmls_folder):
            json_file_name = html_file_name.split(".")[0] + ".json"
            parse_html_to_json(html_file_path=          os.path.join(htmls_folder, html_file_name),
                               output_json_file_path=   os.path.join(raw_jsons_folder, json_file_name))

    # If we don't have any html files available, let us warn the developer
    else:
        logging.error(f"HTML files for {WEBSITE_NAME} do not exist, could not parse them")

if __name__ == "__main__":
    create_raw_jsons()