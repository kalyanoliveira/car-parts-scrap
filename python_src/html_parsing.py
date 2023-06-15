def parse_html_to_json(html_file_path, output_json_file_path):
    from .utils.imports import json, bs, PROJECT_PATH

    content = []
    with open(html_file_path, "r") as f_html:
        content = f_html.readlines()
    content = "".join(content)
    bs_content = bs(content, features="lxml")

    type_of_product = bs_content.find('td', {"class": "TIPO-DE-PRODUTO"})
    if type_of_product: type_of_product = type_of_product.text

    quantity_per_package = bs_content.find('td', {"class": "QUANTIDADE-POR-EMBALAGEM"})
    if quantity_per_package: quantity_per_package = quantity_per_package.text

    color = bs_content.find('td', {"class": "COR"})
    if color: color = color.text

    mass = bs_content.find('td', {"class": "PESO-APROXIMADO"})
    if mass: mass = mass.text

    product_dimensions = bs_content.find('td', {"class": "DIMENSOES-DO-PRODUTO"})
    if product_dimensions: product_dimensions = product_dimensions.text

    package_dimensions = bs_content.find('td', {"class": "DIMENSOES-DA-EMBALAGEM"})
    if package_dimensions: package_dimensions = package_dimensions.text

    compatibility = bs_content.find('td', {"class": "Modelo"})
    if compatibility: compatibility = compatibility.text

    # print(type_of_product, quantity_per_package, color, mass, product_dimensions, package_dimensions, compatibility)

    data = {
        "Tipo": type_of_product,
        "Quantia": quantity_per_package,
        "Cor": color,
        "Peso": mass,
        "Dimensões do Produto": product_dimensions,
        "Dimensões da Embalagem": package_dimensions,
        "Compatibilidade": compatibility
    }

    with open(output_json_file_path, "w") as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)

def generate_jsons():
    from .utils.imports import os, PROJECT_PATH

    def can_generate_jsons():
        # If there are any html files, return True
        for filename in os.listdir(os.path.join(PROJECT_PATH, "data", "htmls")):
            if filename.endswith(".html"):
                return True
        # Else, return False
        return False

    if can_generate_jsons():
        # Go through each html file, and call the parse for it to create its json
        html_file_paths = os.listdir(os.path.join(PROJECT_PATH, "data", "htmls"))

        for html_file_path in html_file_paths:
            html_path = os.path.join(PROJECT_PATH, "data", "htmls", html_file_path)
            json_path = os.path.join(PROJECT_PATH, "data", "jsons", html_file_path.split(".")[0] + ".json")

            parse_html_to_json(html_path, json_path)
    else:
        print("There are no html files")