# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RepItem(scrapy.Item):
    name = scrapy.Field()
    email = scrapy.Field()
    phone = scrapy.Field()
    ssn = scrapy.Field()
    rep_id = scrapy.Field()
    upline_rep = scrapy.Field()
    downline_rep = scrapy.Field()
    pass
