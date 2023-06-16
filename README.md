# Goal

The goal of this project is scrap relevant information from the auto parts in [pecahoje.com.br](https://www.pecahoje.com.br/)

# Method

I started by using python's Scrapy to use the [sitemap](https://www.pecahoje.com.br/robots.txt) to create a csv file ("data/csvs/final.csv"), which contains every single url of the website.

I then gave bash access to this csv via a script that went through each url and saved the html contents of the page.

With the html contents of every single page, it was only a matter of parsing it using tools like regex and bs4. I saved all of the relevant data of each html page into a json.

# Usage

In order to use the bash script to download the html contents of each auto part page, you will to setup some form of proxy. Then, simply pass it to the bash script so that `curl` can later on use it.

`$ python3 main.py`
