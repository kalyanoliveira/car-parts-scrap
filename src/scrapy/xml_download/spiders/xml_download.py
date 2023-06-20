import scrapy
from pathlib import Path

class XMLSpider(scrapy.Spider):
    name = "xml_download"

    # Give me access to the contents of a sitemap.xml file, parse them with parse_sitemap_index
    def start_requests(self):
        yield scrapy.Request(url=self.settings.get("SITEMAP_URL"), callback=self.parse_sitemap_index)

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
        output_dir = "data/pecahoje/xmls"
        file_folder = project_path + "/" + output_dir
        Path(file_folder).mkdir(parents=True, exist_ok=True)

        # Save the contents of the current <loc>.xml file
        file_name = file_folder + "/" + response.url.split("/")[-1]
        Path(file_name).write_bytes(response.body)