import os
import json
from pathlib import Path
import logging
import sys
import re
from collections import defaultdict

PROJECT_PATH = sys.argv[1]
WEBSITE_NAME = sys.argv[2]

raw_jsons_dir = os.path.join(PROJECT_PATH, "data", WEBSITE_NAME, "jsons", "raw")
refined_jsons_dir = os.path.join(PROJECT_PATH, "data", WEBSITE_NAME, "jsons", "refined")

def parse_raw_json_refined(raw_json_path, output_refined_json_path):
    with open(raw_json_path, "r") as f_raw_json:
        raw_data = json.load(f_raw_json)

    data = {
        "mpn":                      raw_data["vtex.events.addData"][0]["productReferenceId"],
        "partnumber":               raw_data["vtex.events.addData"][0]["productReferenceId"],
        "altura":                   get_measures(raw_data)[0],
        "largura":                  get_measures(raw_data)[1],
        "profundidade":             get_measures(raw_data)[2],
        "peso":                     get_peso(raw_data),
        "nome":                     get_descricao(raw_data).split(" ")[0].strip(),
        "descricao":                get_descricao(raw_data),
        "garantia":                 get_garantia(raw_data),
        "categoria":                raw_data["vtxctx"][0]["categoryName"],
        "categoriaId":              raw_data["vtxctx"][0]["categoryId"],
        "departamento":             raw_data["vtxctx"][0]["departmentName"].title(),
        "departamentoId":           raw_data["vtxctx"][0]["departmentyId"],
        "produtoId":                str(raw_data["skuJson_0"][0]["productId"]),
        "imagens":                  raw_data["images"],
        "familias":                 get_familias(raw_data),
        "ano_inicial":              get_ano_inicial(raw_data),
        "ano_final":                get_ano_final(raw_data),
        "modelo":                   get_modelo(),
        "fabricante":               get_fabricante(raw_data),
        "automaker":                get_fabricante(raw_data),
        "anotacoes":                get_anotacoes(raw_data),
    }

    with open(output_refined_json_path, "w") as f_refined_json:
        json.dump(data, f_refined_json, indent=4, ensure_ascii=False)

def get_peso(raw_data):
    peso_string = raw_data["CARACTERISTICAS"][0]["PESO-APROXIMADO"]
    try:
        peso_kg = peso_string[:peso_string.index("kg")].strip().replace(",", ".")
    except ValueError:
        peso_kg = "n/a"
    return peso_kg

def get_descricao(raw_data):
    nome_string = raw_data["skuJson_0"][0]["name"]
    try:
        nome = nome_string[:nome_string.index("|")].strip()
    except ValueError:
        nome = "n/a"
    return nome
    
def get_garantia(raw_data):
    garantia_string = raw_data["CARACTERISTICAS"][0]["GARANTIA"]
    try:
        # Now this is just evil
        garantia_dias = garantia_string[:garantia_string.index("–")].split(" ")[0].strip()
    except ValueError:
        garantia_dias = "n/a"
    return garantia_dias

def get_compatibilidades(raw_data):
    description_string = raw_data["itemprop"]
    pattern = r'APLICAÇÃO: (.+) \| TIPO DE PRODUTO:'
    if (found := re.search(pattern, description_string)):
        familias_string = found.group(1)
        familias = [i.strip() for i in familias_string.split(",")]
        compatibilidades = defaultdict(lambda: [])
        for familia in familias:
            marca = familia.split(" ")[0]
            compatibilidades[marca].append(familia)
        compatibilidades = [compatibilidades]
    else:
        compatibilidades = "n/a"
    return compatibilidades

def get_fabricante(raw_data):
    description_string = raw_data["itemprop"]
    pattern = r'APLICAÇÃO: (.+) \| TIPO DE PRODUTO:'
    if (found := re.search(pattern, description_string)):
        familias_string = found.group(1)
        familias = [i.strip() for i in familias_string.split(",")]
        fabricante = familias[0].split(" ")[0]
    else:
        fabricante = "n/a"
    return fabricante

def get_familias(raw_data):
    description_string = raw_data["itemprop"]
    pattern = r'APLICAÇÃO: (.+) \| TIPO DE PRODUTO:'
    if (found := re.search(pattern, description_string)):
        familias_string = found.group(1)
        familias = [i.strip() for i in familias_string.split(",")]
        for index, familia in enumerate(familias):
            try:
                if re.search("\d\d\d\d", familia):
                    familias[index] = familia[:familia.rindex("-")].strip()
            except ValueError:
                continue
    else:
        familias = "n/a"
    return familias 

def get_ano_inicial(raw_data):
    description_string = raw_data["itemprop"]
    pattern = r'APLICAÇÃO: (.+) \| TIPO DE PRODUTO:'
    if (found := re.search(pattern, description_string)):
        familias_string = found.group(1)
        familias = [i.strip() for i in familias_string.split(",")]
    anos = ["n/a" for _ in familias]
    for index, familia in enumerate(familias):
        if (found := re.search(r'(\d\d\d\d) Em Diante', familia)):
            anos[index] = found.group(1)
    return anos

def get_ano_final(raw_data):
    description_string = raw_data["itemprop"]
    pattern = r'APLICAÇÃO: (.+) \| TIPO DE PRODUTO:'
    if (found := re.search(pattern, description_string)):
        familias_string = found.group(1)
        familias = [i.strip() for i in familias_string.split(",")]
    anos = ["n/a" for _ in familias]
    for index, familia in enumerate(familias):
        if (found := re.search(r'Até (\d\d\d\d)', familia)):
            anos[index] = found.group(1)
    return anos

def get_modelo():
    return "n/a"

def get_anotacoes(raw_data):
    anotacoes = ""
    description_string = raw_data["itemprop"]
    pattern = r"(\| TIPO DE PRODUTO: .* \| QUANTIDADE: .* \| COR: .* \| LADO: .* \|)"
    if (found := re.search(pattern, description_string)):
        anotacoes = anotacoes + f"{found.group(1)}"

    tech_specs_string = raw_data["ESPECIFICACOES"][0]["ESPECIFICACOES-TECNICAS"]
    pattern = r'(.*)Em caso de dúvidas sobre aplicação, entre em contato através de nossa Central de Atendimento ou, ainda,  envie-nos um email. Todos nossos canais de atendimento, incluindo telefone e chat, podem te ajudar a solucionar dúvidas sobre aplicação dos produtos.Nossa equipe também é qualificada para oferecer auxílio nos aspectos técnicos dos produtos que vendemos! Basta entrar em contato!'
    if (found := re.search(pattern, tech_specs_string)):
        anotacoes = anotacoes + f" {found.group(1)}"
    
    indications_string = raw_data["ESPECIFICACOES"][0]["INDICACOES"]
    pattern = r'(.*)O pecahoje.com.br aconselha e recomenda a todos os clientes a escolha de um profissional qualificado para uma instalação adequada do produto como fator decisivo do sucesso no reparo do veículo.'
    if (found := re.search(pattern, indications_string)):
        anotacoes = anotacoes + f" {found.group(1)}"
    return anotacoes

def get_measures(raw_data) -> tuple[str, str, str]:
    if raw_data["CARACTERISTICAS"][0]["DIMENSOES-DA-EMBALAGEM"] != "Consulte-nos!":
        altura = str(raw_data["skuJson_0"][0]["skus"][0]["measures"]["height"])
        largura = str(raw_data["skuJson_0"][0]["skus"][0]["measures"]["width"])
        profundidade = str(raw_data["skuJson_0"][0]["skus"][0]["measures"]["length"])
        return (altura, largura, profundidade)
    return ("n/a", "n/a", "n/a")

def raw_jsons_exist():
    for file_name in os.listdir(raw_jsons_dir):
        if file_name.endswith(".json"):
            return True
    return False

def create_refined_jsons():
    if raw_jsons_exist():
        Path(refined_jsons_dir).mkdir(parents=True, exist_ok=True)
        for raw_json_name in os.listdir(raw_jsons_dir):
            parse_raw_json_refined(raw_json_path=               os.path.join(raw_jsons_dir, raw_json_name),
                                   output_refined_json_path=    os.path.join(refined_jsons_dir, raw_json_name))
    else:
        logging.error(f"Could not create refined jsons for {WEBSITE_NAME}, raw jsons do not exist")

if __name__ == "__main__":
    create_refined_jsons()