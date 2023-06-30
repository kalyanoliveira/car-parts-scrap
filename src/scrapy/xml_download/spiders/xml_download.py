"""
A sitemap.xml file contains URLs to other .xml files, the combination of which
collectively contain all URLs to every single webpage in a website.
This script, given a URL to a sitemap.xml file, downloads those other xml
files.

Usage from project root is:
$ cd /src/scrapy && scrapy crawl xml_download -s PROJECT_PATH="path/to/root/here" -s SITEMAP_URL="link/to/sitemap/xml/file"

You can also add --nolog to omit all of scrapy's whining.
"""

import scrapy
from pathlib import Path
import os

class XMLSpider(scrapy.Spider):
    name = "xml_download"

    def start_requests(self):
        """
        Create a scrapy Request to the sitemap.xml file, and give the response
        contents to the parse_sitemap_index function.

        Args: 
            scrapy Spider

        Returns: 
            void
        """

        sitemap_url = self.settings.get("SITEMAP_URL")
        yield scrapy.Request(url=sitemap_url, callback=self.parse_sitemap_index)

    def parse_sitemap_index(self, response):
        """
        Create a scrapy Request for every single URL of an .xml file that is 
        linked in the sitemap.xml, and give the responses to the
        parse_sitemap_link function.

        Args: 
            scrapy Spider, sitemap.xml response

        Returns: 
            void
        """
        
        # A sitemap.xml file has a bunch of <loc> tags.
        # The text inside those <loc> tags is a URL to another xml file.
        # Let's call those other xml files <loc>.xml.
        # <loc>.xml files contain URLs to every product page of the website, 
        # and we want those.

        namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        # Get the URLs to every <loc>.xml file.
        sitemap_links = response.xpath('//ns:loc/text()', namespaces=namespaces).getall()

        # Create a request to the every URL of a <loc>.xml file, and parse the 
        # response with the parse_sitemap_link function.
        for sitemap_link in sitemap_links:
            yield scrapy.Request(url=sitemap_link, callback=self.parse_sitemap_link)

    def parse_sitemap_link(self, response):
        """
        Saves the contents of the response of a request of a .xml file linked 
        in the sitemap into the appropriate folder.

        Args:
            scrapy Spider, response of the request to the URL of a .xml file
            linked in the sitemap
        
        Returns:
            void
        """

        # Create a folder to save the contents of the current <loc>.xml file.
        project_path = self.settings.get("PROJECT_PATH")
        sitemap_url = self.settings.get("SITEMAP_URL")
        xmls_dir = os.path.join(project_path, "data", sitemap_url.split("/")[2].split(".")[1], "xmls")
        Path(xmls_dir).mkdir(parents=True, exist_ok=True)

        # Save the contents of the current <loc>.xml file.
        xml_file_path = os.path.join(xmls_dir, response.url.split("/")[-1])
        Path(xml_file_path).write_bytes(response.body)