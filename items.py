# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZoznamItem(scrapy.Item):
    # define the fields for your item here like:
    created = scrapy.Field()
    name = scrapy.Field()
    zoznam_url = scrapy.Field()
    address = scrapy.Field()
    label = scrapy.Field()
    company_url = scrapy.Field()
