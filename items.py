# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZoznamItem(scrapy.Item):
    # define the fields for your item here like:
    nazev_firmy = scrapy.Field()
    adresa_firmy = scrapy.Field()
    popis_firmy = scrapy.Field()
    url_firmy = scrapy.Field()
