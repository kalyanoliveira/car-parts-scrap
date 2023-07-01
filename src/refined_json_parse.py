"""
CSV generation! Besides the downloading of photos, this is the final step in our
pipeline. Utilizes the data from the refined JSONs, and does some last bits of 
processing in them.

Usage:
$ python3 refined_json_parse.py path/to/project/here website_name
"""

from pathlib import Path
import json
import sys
import csv
import os

def remove_n_a_from_row(row):
    """
    Little helper function for a previous design choice, takes any list/row that
    we want to add to a csv file and substitues any "n/a" occurences by a space.

    Args:
        List/row that is to be added to a csv file

    Returns:
        Same list/row, but with "" instead of "n/a"
    """

    for index, element in enumerate(row):
        row[index] = element.replace("n/a", "")
    return row

def parse_refined_json(refined_json_path): 
    """
    Given the path to a refined JSON in our drive, adds the data in that JSON
    to each one of our CSVs: compatibilidade.csv, fotos.csv, and info.csv.
    
    Args:
        Path to the refined JSON file

    Returns:
        void
    """

    logger.info(f"Parsing refined json file {refined_json_path.split('/')[-1]}")

    # Get a dict with the data of the supplied refined json.
    with open(refined_json_path, "r") as f_refined_json:
        refined_json_data = json.load(f_refined_json)

    # I mean, I guess this is pretty self explanatory.
    add_json_info_csv(refined_json_data)
    add_json_fotos_csv(refined_json_data)
    add_json_compatibilidade_csv(refined_json_data)

    logger.info(f"Done parsing refined JSON file {refined_json_path.split('/')[-1]}")

def add_json_info_csv(json_data): 

    logger.debug("Adding to info.csv")

    row = [json_data['mpn'], json_data['fabricante'], json_data['nome'], 
           json_data['altura'], json_data['largura'], json_data['profundidade'], 
           json_data['peso'], json_data['descricao'], json_data['partnumber'], 
           json_data['categoria'], json_data['garantia'], json_data['anotacoes'], 
           json_data['produtoId']]

    # Cleaning those annoying "n/a".
    row = remove_n_a_from_row(row)

    info_csv_file_path = os.path.join(csvs_dir, "info.csv")
    with open(info_csv_file_path, "a") as f_info_csv:
        info_csv_writer = csv.writer(f_info_csv)

        info_csv_writer.writerow(row)

    logger.debug("Done adding to info.csv")

def add_json_fotos_csv(json_data):

    logger.debug("Adding to fotos.csv")

    fotos_csv_file_path = os.path.join(csvs_dir, "fotos.csv")
    with open(fotos_csv_file_path, "a") as f_fotos_csv:
        fotos_csv_writer = csv.writer(f_fotos_csv)

        for index, image in enumerate(json_data['imagens']):

            remote_path = image[:image.index("?")]

            image_name = json_data["mpn"] + f"_{index}" + ".jpg"

            Path(local_images_dir).mkdir(parents=True, exist_ok=True)
            local_path = os.path.join(local_images_dir, image_name)

            row = f"{remote_path},{local_path}"
            row = [remote_path, local_path]
            # Cleaning those annoying "n/a".
            row = remove_n_a_from_row(row)

            fotos_csv_writer.writerow(row)

    logger.debug("Done adding to fotos.csv")

def add_json_compatibilidade_csv(json_data):

    logger.debug("Adding to compatibilidade.csv")

    compatibilidade_csv_file_path = os.path.join(csvs_dir, "compatibilidade.csv")
    with open(compatibilidade_csv_file_path, "a") as f_compatibilidade_csv:
        compatibilidade_csv_writer = csv.writer(f_compatibilidade_csv)

        # We check this because certain parts do not have any listed 
        # compatibilidades, and in that we saved an empty string to the
        # refined json data instead of a dict/list.
        if not isinstance(json_data['compatibilidades'], str):

            for compatibilidade in json_data['compatibilidades']:

                row = [json_data['partnumber'], compatibilidade['fabricante'], 
                       compatibilidade['automaker'], compatibilidade['ano_inicial'], 
                       compatibilidade['ano_final'], compatibilidade['name']]
                # Cleaning those annoying "n/a".
                row = remove_n_a_from_row(row)

                compatibilidade_csv_writer.writerow(row)

    logger.debug("Done adding to compatibilidade.csv")


def refined_jsons_exist():
    """
    Returns True if refined JSON files exist, else False.

    Args:
        void

    Returns:
        void
    """

    for file_name in os.listdir(refined_jsons_dir):
        if file_name.endswith(".json"):
            return True
    return False

def create_csv_headers():
    """
    Creates the CSV files where the data from the refined JSONs will be added,
    and their headers too.

    Args:
        void

    Returns:
        void
    """

    logger.debug("Creating csv files and headers")

    # info.csv.
    info_csv_header = ['mpn', 'fabricante', 'nome', 'altura', 'largura', 'profundidade', 'peso', 'descricao', 'partnumber', 'categoria', 'garantia', 'anotacoes', 'id']
    info_csv_file_path = os.path.join(csvs_dir, "info.csv")
    with open(info_csv_file_path, "w") as f_info_csv:
        info_csv_writer = csv.writer(f_info_csv)
        info_csv_writer.writerow(info_csv_header)

    logger.debug("Created info.csv and corresponding header")

    # fotos.csv.
    fotos_csv_header = ['remote', 'local']
    fotos_csv_file_path = os.path.join(csvs_dir, "fotos.csv")
    with open(fotos_csv_file_path, "w") as f_fotos_csv:
        fotos_csv_writer = csv.writer(f_fotos_csv)
        fotos_csv_writer.writerow(fotos_csv_header)
        
    logger.debug("Created fotos.csv and corresponding header")

    # compatibilidade.csv.
    compatibilidade_csv_header = ['partnumber', 'fabricante', 'automaker', 'ano_inicial', 'modelo', 'familia']
    compatibilidade_csv_file_path = os.path.join(csvs_dir, "compatibilidade.csv")
    with open(compatibilidade_csv_file_path, "w") as f_compatibilidade_csv:
        compatibilidade_csv_writer = csv.writer(f_compatibilidade_csv)
        compatibilidade_csv_writer.writerow(compatibilidade_csv_header)

    logger.debug("Created compatibilidade.csv and corresponding header")

    logger.debug("Done creating csv files and headers")

def create_csvs():
    """
    Loops through each refined JSON file, and adds its data to the CSVs.

    Args:
        void

    Returns:
        void
    """

    logger.info(f"Starting refined JSON parse of {WEBSITE_NAME}")

    if refined_jsons_exist():

        # Open the csv file and create their headers.
        create_csv_headers()

        # This is the looping of each refined JSON and the corresponding parsing.
        for refined_json_file_name in os.listdir(refined_jsons_dir):
            refined_json_file_path = os.path.join(refined_jsons_dir, refined_json_file_name)
            parse_refined_json(refined_json_path= refined_json_file_path)
    else:
        logger.error(f"Could not find any refined JSON files")
        return

    logger.info(f"Done parsing refined JSONs of {WEBSITE_NAME}")

if __name__ == "__main__":

    import logging
    import logging.config
    logging.config.fileConfig("./src/logging.conf")
    logger = logging.getLogger("refined_json_parse")
    
    # Command-line arguments.
    PROJECT_PATH = sys.argv[1]
    WEBSITE_NAME = sys.argv[2]

    # Getting the path of some important folders.
    refined_jsons_dir = os.path.join(PROJECT_PATH, "data", WEBSITE_NAME, "jsons", "refined")
    csvs_dir = os.path.join(PROJECT_PATH, "data", WEBSITE_NAME, "csvs")
    local_images_dir = os.path.join("data", WEBSITE_NAME, "fotos")

    create_csvs()