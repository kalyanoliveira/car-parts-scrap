# Goal/Objetivo

The goal of this project is automate the scrapping of auto parts' information.<br>
O objetivo deste projeto é automatizar o *"scrapping"* de informações de peças de carro.

# Methodology/Metodologia

For each website that sells auto parts
1. Obtain the home/main URL of that website
2. Use that URL to obtain that website's sitemap.xml
3. Use that sitemap.xml to obtain all of the URLs of webpages containing auto parts information in that website
4. Use those URLs to download the HTML contents of each webpage containing auto parts information in that website
5. Process those downloaded HTML contents to generate raw JSON files containing a broad range of information about each auto part in that website
6. Implement the ETL of those raw JSON files to obtain refined ones, containing only the information that is relevant about each auto part in that website
7. Do whatever you want with that info

Para cada website the vende peças de carro
1. Obter o URL principal (home) daquele website
2. Usar esse URL principal para obter o sitemap.xml daquele website
3. Usar esse sitemap.xml para obter todos os URLs de páginas daquele website que contém informações sobre peças de carro
4. Usar esses URLs para fazer download, em HTML, de todas as páginas com informações de peças de carro
5. Processar esses HTMLs para gerar arquivos JSON não-processados, que contém informações "brutas" sobre cada peça de carro
6. Implementar o processo de ETL para processar esses arquivos JSON não-processados para obter arquivos JSON processados, que contém apenas informações sobre cada peça de carro de utilidade para nós
7. Fazer o que quiser com esses arquivos JSON processados

# Usage/Uso

Currently implementing a Makefile to do the job <br>
Implentando uma Makefile para fazer o trabalho


`make download_xmls url="http://www.pecahoje.com.br/sitemap.xml"`

`make parse_xmls website_name=pecahoje`