import scrapy
from ..items import ZoznamItem


class ZoznamSpider(scrapy.Spider):

    name = 'zoznam'  # jmeno spideru
    start_urls = ['https://www.zoznam.sk/katalog/Auto-moto-preprava-logistika/Auto-HiFi-autoelektro/']

    def parse(self, response):  # response je odpoved stranky (html kod), kde budu hledat html tagy a css tagy

        items = ZoznamItem()

        firmy = response.css('.catalog-list-content')
        # print("FIRMY:", firmy)

        for firma in firmy:
            # print("FIRMA:", firma)
            # print(type(firma))
            nazev_firmy = firma.css('a::text')[0].extract()
            adresa_firmy = firma.css('a::text')[1].extract()
            popis_firmy = firma.css('.desc::text').extract()
            url_firmy = firma.css('a::text')[2].extract()

            # nazev firmy v hranatych zavorkach musi byt s podtrzitkem, jinak to nefunguje,
            # protoze ten nazev odkazuje na promennou v items
            items['nazev_firmy'] = nazev_firmy
            items['adresa_firmy'] = adresa_firmy
            items['popis_firmy'] = popis_firmy
            items['url_firmy'] = url_firmy

            yield items

            # yield{
            #     'nazev_firmy': nazev_firmy,
            #     'adresa': adresa,
            #     'popis': popis,
            #     'url_firmy': url_firmy
            # }

        next_page = response.css('div.paginator a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)