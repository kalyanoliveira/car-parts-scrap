def parse_html_to_json_old(html_file_path, output_json_file_path):
    """
    Deprecated
    """
    from .utils.imports import json, bs 

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

# Does cool stuff
def parse_html_to_json(html_file_path, output_json_file_path):
    from .utils.imports import json, bs, re, eval_js, logging

    logging.debug(f"Parsing html file {html_file_path}")

    # Get the html content of the html file in html_file_path
    content = []
    with open(html_file_path, "r") as f_html:
        content = f_html.readlines()
    content = "".join(content)
    bs_content = bs(content, features="lxml")

    # Find all possible <script> tags in that content
    scripts = bs_content.find_all('script')

    # For each script tag, evaluate the following regex
    # Append true evaluations to the array "potentials"
    pattern = r'var skuJson_0 = ({.*});CATALOG_SDK.setProductWithVariationsCache\(skuJson_0.productId, skuJson_0\); var skuJson = skuJson_0;'
    potentials = []
    for script in scripts:
        if (match := re.match(pattern, script.text)):
            potentials.append(match.group(1))

    # If we get more than one true regex evaluation, something went wrong
    if len(potentials) != 1:
        print("Found more than one regex pattern, saving some random stuff into the json")
        random_data = {"hi":"how are you doing"}
        with open(output_json_file_path, "w") as f_json:
            json.dump(random_data, f_json, indent=4, ensure_ascii=False)
            logging.error(f"Error in parsing of {html_file_path}: found more than one regex pattern")
            return
    
    # If we get just one true regex evaluation, that means that we have the json contents we need
    # Let's save those here
    true_potential = potentials[0]

    # I have no idea what this exactly does, but
    # the input is the regex string
    # the output is the dictionary of the regex string
    # and I know how to convert a python dictionary to a JSON, so we good
    js_code = f'''
        var result={true_potential};
        JSON.stringify(result);
    '''
    variable_value = eval_js(js_code)
    data = json.loads(variable_value)

    with open(output_json_file_path, "w") as f_json:
        json.dump(data, f_json, indent=4, ensure_ascii=False)


def generate_jsons():
    from .utils.imports import os, PROJECT_PATH

    # def can_generate_jsons():
    #     # If there are any html files, return True
    #     for filename in os.listdir(os.path.join(PROJECT_PATH, "data", "htmls")):
    #         if filename.endswith(".html"):
    #             return True
    #     # Else, return False
    #     return False

    # if can_generate_jsons():
    #     # Go through each html file, and call the parse for it to create its json
    #     html_file_paths = os.listdir(os.path.join(PROJECT_PATH, "data", "htmls"))

    #     for html_file_path in html_file_paths:
    #         html_path = os.path.join(PROJECT_PATH, "data", "htmls", html_file_path)
    #         json_path = os.path.join(PROJECT_PATH, "data", "jsons", html_file_path.split(".")[0] + ".json")

    #         parse_html_to_json(html_path, json_path)
    # else:
    #     return 1

    for filename in os.listdir(os.path.join(PROJECT_PATH, "data", "htmls")):
        if filename.endswith(".html"):
            html_file_paths = os.listdir(os.path.join(PROJECT_PATH, "data", "htmls"))

            for html_file_path in html_file_paths:
                html_path = os.path.join(PROJECT_PATH, "data", "htmls", html_file_path)
                json_path = os.path.join(PROJECT_PATH, "data", "jsons", html_file_path.split(".")[0] + ".json")

                parse_html_to_json(html_path, json_path)
            return "Found html"
    return "Not found html"