# Usage: $ scrapy runspider xml_download.py

import scrapy
from pathlib import Path
import logging

# Making sure scrapy is not polluting the terminal if not necessary
logging.getLogger('scrapy').setLevel(logging.WARNING)

# Sucks that I can't relative import, but whatever
# from ..python_src.utils.imports import PROJECT_PATH, os
output_dir = "xmls/"


class SitemapSpider(scrapy.Spider):
    name = 'sitemap_spider'

    def start_requests(self):
        yield scrapy.Request('http://www.pecahoje.com.br/sitemap.xml', self.parse_sitemap_index)

    def parse_sitemap_index(self, response):
        # Parse the sitemap index XML and extract the individual sitemap URLs
        namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        sitemap_urls = response.xpath('//ns:loc/text()', namespaces=namespaces).getall()

        # Follow each sitemap URL and parse the sitemaps
        for sitemap_url in sitemap_urls:
            yield scrapy.Request(sitemap_url, self.parse_sitemap)

    def parse_sitemap(self, response):
        filename = output_dir + response.url.split("/")[-1]
        Path(filename).write_bytes(response.body)