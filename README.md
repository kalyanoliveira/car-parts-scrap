# Goal

The goal of this project is automate the scrapping of auto parts' information.<br>

# Methodology

1. Download all the .xml files linked in the sitemap.xml file of a website that sells car parts;
2. Process those .xml files to create a list of all URLs of all webpages of car parts in that website;
3. Use that list to download the HTML contents of every single webpage that contains information about car parts in that website;
4. Process those HTML files in raw JSONs, which contain general information that might be interesting to us;
5. Process those raw JSONs to gather more specifically the data that we want, generating refined JSONs;
6. Use those refined JSONs to generate .csv files that contain the information that we actually want, in the structure that we want it;
7. Success!

# Usage

`echo "" > log.txt && make pecahoje > log.txt`

Or, of course, you can run just run `$ make pecahoje`, but I prefer keeping all of the output in a log file.

You will need to setup a proxy, eventually. Then just add it the Makefile variable.
Or just remove the proxy from the request command in the html_download.py file.