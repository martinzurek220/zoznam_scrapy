import scrapy
from ..items import ZoznamItem
from scrapy.linkextractors import LinkExtractor
from datetime import datetime


class ZoznamSpider(scrapy.Spider):

    def __init__(self):
        self.urL_counter = 0  # Pocet pro porovnani s limitem url
        self.limit_urls = 100
        self.parsed_url = []
        self.firs_part_url = "https://www.zoznam.sk"
        self.items = ZoznamItem()

    name = 'zoznam'  # jmeno spideru

    start_urls = [
        'https://www.zoznam.sk/katalog/'
    ]

    link_extractor = LinkExtractor(allow='/katalog/', restrict_css='.folder')

    def start_requests(self):
        """

        Funkce ziska html kod ze vsech starts_url a tyto url adresy ulozi do slovniku

        :return: html kod urls start-requests
        """

        for url in self.start_urls:
            self.parsed_url.append(url)
            self.urL_counter += 1
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):  # response je odpoved stranky (html kod), kde budu hledat html tagy a css tagy
        """

        Funkce vezme jednotlive odpovedi ze serveru (html kod) a provede nasledujici:
         - Najde vsechny odkazy pro dalsi crawlovani
         - Stahne z dane url udaje o vsech firmach
         - Ziska html kod urls nasledujici urovne

        :param response: html kod urls aktualni urovne
        :return: html kod urls nasledujici urovne
        """

        # Ziskani url adres pro dalsi crawling
        links = self.link_extractor.extract_links(response)

        # Stazeni udaju o firmach
        yield from self.get_companies_and_bookmarks(response)

        # Url k naparsovani
        for idx, link in enumerate(links):
            if idx < 1 and link.url not in self.parsed_url and \
                    self.urL_counter < self.limit_urls:
                self.urL_counter += 1
                self.parsed_url.append(link.url)
                yield scrapy.Request(link.url)

                # print(f"Pocet stazenych url: {self.pocet_naparsovanych_url}")
            else:
                break

        # print(f"Naparsovane url: {self.naparsovane_url}")

    def get_companies(self, response):
        """

        Funkce z url stahne informace o firme a posle je do items.py k dalsimu zpracovani.

        Priklad vystupu:
        {"created": "2023-01-29 17:40:32.292815",
         "name": ["Aster, spol. s r.o., Bratislava"],
         "zoznam_url": "https://www.zoznam.sk/firma/22654/Aster-spol-s-r-o-Bratislava",
         "address": ["Mramorov\u00e1 4, 82106 Bratislava"],
         "label": ["Predaj autohifi a autodoplnkov ..."],
         "company_url": ["http://www.aster.sk"]}

        :param response: html kod urls aktualni urovne
        :return: ulozeni informaci o firmach do itemu
        """

        companies = response.css('.catalog-list-content')

        for company in companies:

            created = str(datetime.now())
            name = company.css('h2 a::text').extract()
            zoznam_url = company.css('a::attr(href)').get()
            address = company.css('address a::text').extract()
            label = company.css('p::text').extract()
            company_url = company.css('a.catalog-list-link::text').extract()

            zoznam_url = self.firs_part_url + zoznam_url

            # nazev firmy v hranatych zavorkach musi byt s podtrzitkem, jinak to nefunguje,
            # protoze ten nazev odkazuje na promennou v items
            self.items['created'] = created
            self.items['name'] = name
            self.items['zoznam_url'] = zoznam_url
            self.items['address'] = address
            self.items['label'] = label
            self.items['company_url'] = company_url

            yield self.items

    def get_companies_and_bookmarks(self, response):
        """

        Funkce stahne informace o firme ze vsech zalozek (1, 2, 3, ...)

        :param response: html kod urls aktualni urovne
        :return: html kod jednotlivych zalozek
        """

        yield from self.get_companies(response)

        next_page = response.css('a.next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.get_companies_and_bookmarks)

















