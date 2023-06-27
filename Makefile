PROJECT_PATH = $(shell pwd)

download_xmls:
	cd ./src/scrapy && scrapy crawl xml_download -s PROJECT_PATH=$(PROJECT_PATH) -s SITEMAP_URL=$(sitemap_url)

parse_xmls:
	cd ./src && python3 xml_parse.py $(PROJECT_PATH) $(website_name)

download_htmls:
	cd ./src && python3 html_download.py $(proxy_credential) $(PROJECT_PATH) $(website_name)

parse_htmls:
	cd ./src && python3 html_parse.py $(PROJECT_PATH) $(website_name)

parse_raw_jsons:
	cd ./src && python3 raw_json_parse.py $(PROJECT_PATH) $(website_name)

parse_refined_jsons:
	cd ./src && python3 refined_json_parse.py $(PROJECT_PATH) $(website_name)

download_photos:
	cd ./src && python3 photo_download.py $(proxy_credential) $(PROJECT_PATH) $(website_name)

.PHONY: pecahoje_xmls pecahoje_urls pecahoje_htmls pecahoje_raw_jsons pecahoje_refined_jsons pecahoje_csvs



a := ./data/pecahoje/xmls/product-
PECAHOJE_XML_FILES := $a1.xml $a2.xml $a3.xml $a4.xml $a5.xml $a6.xml $a7.xml

pecahoje_xmls: $(PECAHOJE_XML_FILES)

$(PECAHOJE_XML_FILES) &:
	@cd ./src/scrapy && scrapy crawl xml_download -s PROJECT_PATH=$(PROJECT_PATH) -s SITEMAP_URL="http://www.pecahoje.com.br/sitemap.xml" --nolog
	@rm ./data/pecahoje/xmls/brand-1.xml
	@rm ./data/pecahoje/xmls/category-1.xml



pecahoje_urls: ./data/pecahoje/csvs/product_urls.csv

./data/pecahoje/csvs/product_urls.csv: pecahoje_xmls
	cd ./src && python3 xml_parse.py $(PROJECT_PATH) pecahoje



pecahoje_htmls: pecahoje_urls
	# If there are no html files, download them
	@if [ -z "$$(ls -A ./data/pecahoje/htmls/*.html 2>/dev/null)" ]; then \
		NUM_OF_HTMLS_FILES="$$(cat ./data/pecahoje/csvs/product_urls.csv | wc -l)"; \
		python3 ./src/html_download.py socks5h://localhost:9050 $(PROJECT_PATH) pecahoje 15 $${NUM_OF_HTMLS_FILES}; \
	else \
		:; \
	fi



pecahoje_raw_jsons: pecahoje_htmls
	# If no raw jsons already exist, create them
	@if [ -z "$$(ls -A ./data/pecahoje/jsons/raw/*.json 2>/dev/null)" ]; then \
		python3 .src/html_parse.py $(PROJECT_PATH) pecahoje; \
	else \
		:; \
	fi




pecahoje_refined_jsons: pecahoje_raw_jsons
	# If no refined jsons already exist, create them
	@if [ -z "$$(ls -A ./data/pecahoje/jsons/refined/*.json 2>/dev/null)" ]; then \
		python3 ./src/raw_json_parse.py $(PROJECT_PATH) pecahoje; \
	else \
		:; \
	fi




pecahoje_csvs: pecahoje_refined_jsons
	# If no csvs exist, create them
	@if [ -z "$$(ls -A ./data/pecahoje/csvs/*.csv 2>/dev/null)" ]; then \
		python3 ./src/refined_json_parse.py $(PROJECT_PATH) pecahoje; \
	else \
		:; \
	fi