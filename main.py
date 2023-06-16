from python_src.utils.imports import os
PROJECT_PATH = os.getcwd()

def main():
    # Generating final.csv from xml files
    from python_src.utils.imports import logging
    from python_src.utils.imports import generate_csv
    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug("Generating final.csv")
    out_stat = generate_csv()
    if out_stat == "Not found xmls":
        logging.error("Could not find xml files required to generate final.csv")
        logging.error("Please create them by going to the data directory and running $ scrapy runspider xml_download.py")
        return
    elif out_stat == "Found csv":
        logging.warning("Found final.csv. If you wish to re-create it, please delete it")
    elif out_stat == "No errors":
        logging.debug("Generated final.csv")


    # Downloading html files using final.csv
    os.system("echo downloading htmls using bash")

    # Parsing the downloaded htmls files to generate jsons
    from python_src.utils.imports import generate_jsons
    logging.debug("Generating jsons")
    out_stat = generate_jsons()
    if out_stat == "Not found html":
        logging.error("Could not find any html files")
        return
    elif out_stat == "Found html":
        logging.debug("Generated jsons")
        return

    print("This should never happen")

if __name__ == "__main__":
    main()