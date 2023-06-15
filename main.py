from python_src.utils.imports import os
PROJECT_PATH = os.getcwd()

def main():
    print(PROJECT_PATH)

    from python_src.utils.imports import generate_csv
    generate_csv()

    from python_src.utils.imports import generate_jsons
    generate_jsons()

if __name__ == "__main__":
    main()