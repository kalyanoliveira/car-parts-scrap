# Goal

The goal of this project is automate the scrapping of auto parts' information.

# Methodology

For each website that sells auto parts
1. Obtain the home/main URL of that website
2. Use that URL to obtain that website's sitemap.xml
3. Use that sitemap.xml to obtain all of the URLs of webpages containing auto parts information in that website
4. Use those URLs to download the HTML contents of each webpage containing auto parts information in that website
5. Process those downloaded HTML contents to generate raw JSON files containing a broad range of information about each auto part in that website
6. Implement the ETL of those raw JSON files to obtain refined ones, containing only the information that is relevant about each auto part in that website
7. Do whatever you want with that info

# Usage

Currently implementing a Makefile to do the job