import scrapy
from pathlib import Path
import logging
import os

class XMLSpider(scrapy.Spider):
    name = "xml_download"

    # Give me access to the contents of a sitemap.xml file, parse them with parse_sitemap_index
    def start_requests(self):
        sitemap_url = self.settings.get("SITEMAP_URL")
        logging.debug(f"Running XML download for {sitemap_url}")
        yield scrapy.Request(url=sitemap_url, callback=self.parse_sitemap_index)

    def parse_sitemap_index(self, response):

        # A sitemap.xml file has a bunch of <loc> tags
        # The text inside those <loc> tags is a URL to another xml file
        # Let's call those xml files <loc>.xml
        # <loc>.xml files contain URLs to every product page of the website, and we want those

        namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        # Get the URLs to every <loc>.xml file
        sitemap_links = response.xpath('//ns:loc/text()', namespaces=namespaces).getall()

        # For every <loc>.xml file, get it's contents, and save them using parse_sitemap_link
        for sitemap_link in sitemap_links:
            yield scrapy.Request(url=sitemap_link, callback=self.parse_sitemap_link)

    def parse_sitemap_link(self, response):
        # Create a folder to save the contents of the current <loc>.xml file
        project_path = self.settings.get("PROJECT_PATH")
        sitemap_url = self.settings.get("SITEMAP_URL")
        xmls_dir = os.path.join(project_path, "data", sitemap_url.split("/")[2].split(".")[1], "xmls")
        Path(xmls_dir).mkdir(parents=True, exist_ok=True)

        # Save the contents of the current <loc>.xml file
        xml_file_path = os.path.join(xmls_dir, response.url.split("/")[-1])
        Path(xml_file_path).write_bytes(response.body)