def add_xml_to_csv(xml_filepath, output_csv_filepath):
    from .utils.imports import bs, logging 

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

def generate_csv():
    from .utils.imports import os, PROJECT_PATH, logging

    # def can_generate_csv():
    #     # If there already exists a csv file, return 1
    #     if os.path.exists(os.path.join(PROJECT_PATH, "data", "csvs", "final.csv")):
    #         return 1
    #     # If there are xmls, return False (signifying no errors) 
    #     for filename in os.listdir(os.path.join(PROJECT_PATH, "data", "xmls")):
    #         if filename.endswith(".xml"):
    #             return 0
    #     # If there are no xmls, return error 2
    #     return 2

    # condition = can_generate_csv()
    # # If there are xml files and no csv file
    # if condition == 0:
    #     xml_file_names = os.listdir(os.path.join(PROJECT_PATH, "data", "xmls"))
    #     for xml_file_name in xml_file_names:
    #         add_xml_to_csv(os.path.join(PROJECT_PATH, "data", "xmls", xml_file_name), os.path.join(PROJECT_PATH, "data", "csvs", "final.csv"))
    #     return condition
    # # If there are no xml files and no csv file
    # elif condition == 2:
    #     return condition
    # # If there is already a csv file
    # elif condition == 1:
    #     return condition

    if os.path.exists(os.path.join(PROJECT_PATH, "data", "csvs", "final.csv")):
        return "Found csv"
    for filename in os.listdir(os.path.join(PROJECT_PATH, "data", "xmls")):
        if filename.endswith(".xml"):
            xml_file_names = os.listdir(os.path.join(PROJECT_PATH, "data", "xmls"))
            for xml_file_name in xml_file_names:
                add_xml_to_csv(os.path.join(PROJECT_PATH, "data", "xmls", xml_file_name), os.path.join(PROJECT_PATH, "data", "csvs", "final.csv"))
            return "No errors"
    return "Not found xmls"