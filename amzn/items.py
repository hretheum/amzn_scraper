# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmznItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    asin = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    timestamp = scrapy.Field()
    queryID = scrapy.Field()

    pass
