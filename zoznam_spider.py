import scrapy
from ..items import ZoznamItem
from scrapy.linkextractors import LinkExtractor
from datetime import datetime


class ZoznamSpider(scrapy.Spider):

    def __init__(self):
        self.pocet_naparsovanych_url = 0  # Pocet pro porovnani s limitem url
        self.limit_pro_naparsovani_url = 100
        self.naparsovane_url = []
        self.prvni_cast_url = "https://www.zoznam.sk"
        self.items = ZoznamItem()

    name = 'zoznam'  # jmeno spideru

    start_urls = [
        'https://www.zoznam.sk/katalog/'
    ]

    link_extractor = LinkExtractor(allow='/katalog/', restrict_css='.folder')

    def start_requests(self):

        for url in self.start_urls:
            self.naparsovane_url.append(url)
            self.pocet_naparsovanych_url += 1
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):  # response je odpoved stranky (html kod), kde budu hledat html tagy a css tagy

        links = self.link_extractor.extract_links(response)

        # Stazeni udaju o firmach
        yield from self.stahni_firmy_a_zalozky(response)

        # Url k naparsovani
        for idx, link in enumerate(links):
            if idx < 2 and link.url not in self.naparsovane_url and \
                    self.pocet_naparsovanych_url < self.limit_pro_naparsovani_url:
                self.pocet_naparsovanych_url += 1
                self.naparsovane_url.append(link.url)
                yield scrapy.Request(link.url)

                # print(f"Pocet stazenych url: {self.pocet_naparsovanych_url}")
            else:
                break

        # print(f"Naparsovane url: {self.naparsovane_url}")

    def stahni_firmy(self, response):

        firmy = response.css('.catalog-list-content')
        # print("FIRMY:", firmy)

        for firma in firmy:
            # print("FIRMA:", firma)
            # print(type(firma))

            vytvoreno = str(datetime.now())
            nazev_firmy = firma.css('h2 a::text').extract()
            zoznam_url_firmy = firma.css('a::attr(href)').get()
            adresa_firmy = firma.css('address a::text').extract()
            popis_firmy = firma.css('p::text').extract()
            url_firmy = firma.css('a.catalog-list-link::text').extract()

            zoznam_url_firmy = self.prvni_cast_url + zoznam_url_firmy

            # nazev firmy v hranatych zavorkach musi byt s podtrzitkem, jinak to nefunguje,
            # protoze ten nazev odkazuje na promennou v items
            self.items['vytvoreno'] = vytvoreno
            self.items['nazev_firmy'] = nazev_firmy
            self.items['zoznam_url_firmy'] = zoznam_url_firmy
            self.items['adresa_firmy'] = adresa_firmy
            self.items['popis_firmy'] = popis_firmy
            self.items['url_firmy'] = url_firmy

            yield self.items

    def stahni_firmy_a_zalozky(self, response):

        yield from self.stahni_firmy(response)

        next_page = response.css('a.next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.stahni_firmy_a_zalozky)

















