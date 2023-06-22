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

process_json:
	echo For each website
	echo For each raw JSON of that website
	echo Process that raw JSON to create a refined JSON