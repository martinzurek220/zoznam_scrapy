import scrapy
from ..items import ZoznamItem
from scrapy.linkextractors import LinkExtractor


class ZoznamSpider(scrapy.Spider):

    def __init__(self):
        self.pocet_naparsovanych_url = 0
        self.limit_pro_naparsovani_url = 100
        self.naparsovane_url = []

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
        # print(f"Link: {links}")
        print(f"Počet odkazů: {len(links)}")

        # Stazeni udaju o firmach
        yield from self.stahni_udaje_o_firmach(response)

        # Url k naparsovani
        for idx, link in enumerate(links):
            if idx < 1 and link.url not in self.naparsovane_url and \
                    self.pocet_naparsovanych_url < self.limit_pro_naparsovani_url:
                self.pocet_naparsovanych_url += 1
                self.naparsovane_url.append(link.url)
                yield scrapy.Request(link.url)

                print(f"Pocet stazenych url: {self.pocet_naparsovanych_url}")
            else:
                break

        print(f"Naparsovane url: {self.naparsovane_url}")

    def stahni_udaje_o_firmach(self, response):

        firmy = response.css('.catalog-list-content')
        # print("FIRMY:", firmy)

        for firma in firmy:
            # print("FIRMA:", firma)
            # print(type(firma))

            nazev_firmy = firma.css('h2 a::text').extract()
            adresa_firmy = firma.css('address a::text').extract()
            # popis_firmy = firma.css('.desc::text').extract()
            popis_firmy = firma.css('p::text').extract()
            url_firmy = firma.css('a.catalog-list-link::text').extract()

            yield {
                'nazev_firmy': nazev_firmy,
                'adresa': adresa_firmy,
                'popis': popis_firmy,
                'url_firmy': url_firmy,
            }

    def najdi_zalozky(self, response):

        zalozky = response.css('.row paginator')

        for zalozka in zalozky:

            zalozka_url = zalozka.css('a::attr(href)').get()

            # Dokoncit zalozky


















