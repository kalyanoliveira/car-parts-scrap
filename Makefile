PROJECT_PATH = $(shell pwd)

download_photos:
	cd ./src && python3 photo_download.py $(proxy_credential) $(PROJECT_PATH) $(website_name)

.PHONY: pecahoje_xmls pecahoje_urls pecahoje_htmls pecahoje_raw_jsons pecahoje_refined_jsons pecahoje_csvs pecahoje

a := ./data/pecahoje/xmls/product-
PECAHOJE_XML_FILES := $a1.xml $a2.xml $a3.xml $a4.xml $a5.xml $a6.xml $a7.xml

$(PECAHOJE_XML_FILES) &:
	@echo 0
	@# If xml files do not already exist, create them
	@if [ -z "$$(ls -A ./data/$(WEBSITE_NAME)/xmls/*.xml 2>/dev/null)" ]; then \
		echo "Downloading xml files from supplied sitemap url"; \
		cd ./src/scrapy && scrapy crawl xml_download -s PROJECT_PATH=$(PROJECT_PATH) -s SITEMAP_URL="http://www.pecahoje.com.br/sitemap.xml" --nolog; \
		rm -f ../../data/$(WEBSITE_NAME)/xmls/brand-1.xml; \
		rm -f ../../data/$(WEBSITE_NAME)/xmls/category-1.xml; \
	else \
		:; \
	fi
	
pecahoje_xmls: $(PECAHOJE_XML_FILES)
	@echo 1

pecahoje_urls: pecahoje_xmls
	@echo 2
	@# If the url csv file does not already exist, create it
	@if [ -z "$$(ls -A ./data/$(WEBSITE_NAME)/csvs/urls/product_urls.csv 2>/dev/null)" ]; then \
		echo "Creating urls csv from xml files"; \
		python3 ./src/xml_parse.py $(PROJECT_PATH) $(WEBSITE_NAME); \
	else \
		:; \
	fi

pecahoje_htmls: pecahoje_urls
	@echo 3
	@# If no html files already exist, download them
	@if [ -z "$$(ls -A ./data/$(WEBSITE_NAME)/htmls/*.html 2>/dev/null)" ]; then \
		echo "Downloading html files from urls csv"; \
		NUM_OF_HTMLS_FILES="$$(cat ./data/$(WEBSITE_NAME)/csvs/product_urls.csv | wc -l)"; \
		python3 ./src/html_download.py $(PROXY) $(PROJECT_PATH) $(WEBSITE_NAME) 15 5; \
		$(MAKE) clean_pecahoje_raw_jsons ; \
	else \
		:; \
	fi

pecahoje_raw_jsons: pecahoje_htmls
	@echo 4
	@# If no raw jsons already exist, create them
	@if [ -z "$$(ls -A ./data/$(WEBSITE_NAME)/jsons/raw/*.json 2>/dev/null)" ]; then \
		echo "Creating raw jsons from html files"; \
		python3 ./src/html_parse.py $(PROJECT_PATH) $(WEBSITE_NAME); \
		$(MAKE) clean_pecahoje_refined_jsons ; \
	else \
		:; \
	fi

pecahoje_refined_jsons: pecahoje_raw_jsons
	@echo 5
	@# If no refined jsons already exist, create them
	@if [ -z "$$(ls -A ./data/$(WEBSITE_NAME)/jsons/refined/*.json 2>/dev/null)" ]; then \
		echo "Creating refined jsons from raw jsons"; \
		python3 ./src/raw_json_parse.py $(PROJECT_PATH) $(WEBSITE_NAME); \
		$(MAKE) clean_pecahoje_csvs ; \
	else \
		:; \
	fi

pecahoje_csvs: pecahoje_refined_jsons
	@echo 6
	@# If no csvs already exist, create them
	@if [ -z "$$(ls -A ./data/$(WEBSITE_NAME)/csvs/*.csv 2>/dev/null)" ]; then \
		echo "Creating csvs from refined json files"; \
		python3 ./src/refined_json_parse.py $(PROJECT_PATH) $(WEBSITE_NAME); \
	else \
		:; \
	fi

pecahoje: WEBSITE_NAME = pecahoje
pecahoje: PROXY = socks5h://localhost:9050
pecahoje: pecahoje_csvs
	@echo 7

clean_pecahoje_csvs:
	@echo "Cleaning csvs"
	@rm -f ./data/pecahoje/csvs/compatibilidade.csv
	@rm -f ./data/pecahoje/csvs/fotos.csv
	@rm -f ./data/pecahoje/csvs/info.csv

clean_pecahoje_refined_jsons: clean_pecahoje_csvs
	@echo "Cleaning refined jsons"
	@rm -f ./data/pecahoje/jsons/refined/*.json

clean_pecahoje_raw_jsons: clean_pecahoje_refined_jsons
	@echo "Cleaning raw jsons"
	@rm -f data/pecahoje/jsons/raw/*.json