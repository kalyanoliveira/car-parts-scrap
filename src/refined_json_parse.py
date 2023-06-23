from pathlib import Path
import json
import sys
import csv
import logging
import os

PROJECT_PATH = sys.argv[1]
WEBSITE_NAME = sys.argv[2]

refined_jsons_dir = os.path.join(PROJECT_PATH, "data", WEBSITE_NAME, "jsons", "refined")
csvs_dir = os.path.join(PROJECT_PATH, "data", WEBSITE_NAME, "csvs")
local_images_dir = os.path.join("data", WEBSITE_NAME, "fotos")

logging.getLogger().setLevel(logging.DEBUG)


def remove_n_a_from_row(row):
    for index, element in enumerate(row):
        row[index] = element.replace("n/a", "")
    return row

def parse_refined_json(refined_json_path): 
    logging.debug(f"Parsing refined json {refined_json_path}")
    with open(refined_json_path, "r") as f_refined_json:
        refined_json_data = json.load(f_refined_json)

    add_json_info_csv(refined_json_data)
    add_json_fotos_csv(refined_json_data)
    add_json_compatibilidade_csv(refined_json_data)

def add_json_info_csv(json_data): 
    row = [json_data['mpn'], json_data['fabricante'], json_data['nome'], json_data['altura'], json_data['largura'], json_data['profundidade'], json_data['peso'], json_data['descricao'], json_data['partnumber'], json_data['categoria'], json_data['garantia'], json_data['anotacoes'], json_data['produtoId']]

    row = remove_n_a_from_row(row)

    info_csv_file_path = os.path.join(csvs_dir, "info.csv")
    with open(info_csv_file_path, "a") as f_info_csv:
        info_csv_writer = csv.writer(f_info_csv)
        info_csv_writer.writerow(row)

def add_json_fotos_csv(json_data):
    fotos_csv_file_path = os.path.join(csvs_dir, "fotos.csv")
    with open(fotos_csv_file_path, "a") as f_fotos_csv:
        fotos_csv_writer = csv.writer(f_fotos_csv)

        for index, image in enumerate(json_data['imagens']):
            remote_path = image[:image.index("?")]

            image_name = json_data["mpn"] + f"_{index}"

            Path(local_images_dir).mkdir(parents=True, exist_ok=True)
            local_path = os.path.join(local_images_dir, image_name)

            row = f"{remote_path},{local_path}"
            row = [remote_path, local_path]
            row = remove_n_a_from_row(row)
            fotos_csv_writer.writerow(row)

def add_json_compatibilidade_csv(json_data):

    compatibilidade_csv_file_path = os.path.join(csvs_dir, "compatibilidade.csv")

    with open(compatibilidade_csv_file_path, "a") as f_compatibilidade_csv:
        compatibilidade_csv_writer = csv.writer(f_compatibilidade_csv)
        if not isinstance(json_data['compatibilidades'], str):
            for compatibilidade in json_data['compatibilidades']:

                row = [json_data['partnumber'], compatibilidade['fabricante'], compatibilidade['automaker'], compatibilidade['ano_inicial'], compatibilidade['ano_final'], compatibilidade['name']]
                row = remove_n_a_from_row(row)
                compatibilidade_csv_writer.writerow(row)


def refined_jsons_exist():
    for file_name in os.listdir(refined_jsons_dir):
        if file_name.endswith(".json"):
            return True
    return False

def create_csv_headers():
    info_csv_header = ['mpn', 'fabricante', 'nome', 'altura', 'largura', 'profundidade', 'peso', 'descricao', 'partnumber', 'categoria', 'garantia', 'anotacoes', 'id']
    info_csv_file_path = os.path.join(csvs_dir, "info.csv")
    with open(info_csv_file_path, "w") as f_info_csv:
        info_csv_writer = csv.writer(f_info_csv)
        info_csv_writer.writerow(info_csv_header)

    fotos_csv_header = ['remote', 'local']

    fotos_csv_file_path = os.path.join(csvs_dir, "fotos.csv")
    with open(fotos_csv_file_path, "w") as f_fotos_csv:
        fotos_csv_writer = csv.writer(f_fotos_csv)
        fotos_csv_writer.writerow(fotos_csv_header)

    compatibilidade_csv_header = ['partnumber', 'fabricante', 'automaker', 'ano_inicial', 'modelo', 'familia']
    compatibilidade_csv_file_path = os.path.join(csvs_dir, "compatibilidade.csv")
    with open(compatibilidade_csv_file_path, "w") as f_compatibilidade_csv:
        compatibilidade_csv_writer = csv.writer(f_compatibilidade_csv)
        compatibilidade_csv_writer.writerow(compatibilidade_csv_header)

def create_csvs():
    if refined_jsons_exist():
        create_csv_headers()

        for refined_json_file_name in os.listdir(refined_jsons_dir):
            refined_json_file_path = os.path.join(refined_jsons_dir, refined_json_file_name)
            parse_refined_json(refined_json_path= refined_json_file_path)
    else:
        logging.debug(f"Could not create csvs for {WEBSITE_NAME}, refined jsons do not exist")

if __name__ == "__main__":
    create_csvs()