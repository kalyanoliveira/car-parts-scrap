PROJECT_PATH = $(shell pwd)

download_xmls:
	cd ./src/scrapy && scrapy crawl xml_download -s PROJECT_PATH=$(PROJECT_PATH) -s SITEMAP_URL=$(sitemap_url)

parse_xmls:
	cd ./src && python3 xml_parse.py $(PROJECT_PATH) $(website_name)

explore_site:
	echo For each line in sitemap.csv
	echo Get the URL of the sitemap.xml
	echo Use the sitemap.xml to find all URLs of webpages containing car parts in that website
	echo Create a csv where each line has a URL of a car part\'s webpage, and a file-name to save the HTML contents of that webpage to
	echo "Call that csv <name_of_website>.csv"

download_html:
	echo "For each <name_of_website>.csv file"
	echo "For each line in that <name_of_website>.csv file"
	echo "Use the URL of the car part's webpage to download the HTML contents of that webpage into the specified file-name"

process_html:
	echo For each website
	echo For each downloaded HTML file of that website
	echo Extract all of the revelant info of that HTML and put it in a raw JSON file

process_json:
	echo For each website
	echo For each raw JSON of that website
	echo Process that raw JSON to create a refined JSON