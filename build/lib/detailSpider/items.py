# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class detailItem(scrapy.Item):
    website = scrapy.Field()
    review_date = scrapy.Field()
    id = scrapy.Field()
    # hometype = scrapy.Field()
    # isPlus =  scrapy.Field()
    # address = scrapy.Field()
    city = scrapy.Field()
    # state = scrapy.Field()
    # country = scrapy.Field()
    # guest = scrapy.Field()
    # bedroom = scrapy.Field()
    # bathroom = scrapy.Field()
    # bed = scrapy.Field()
    # hostname = scrapy.Field()
    # jointime = scrapy.Field()
    # hostcity = scrapy.Field()
    # hoststate = scrapy.Field()
    # hostcountry = scrapy.Field()
    # review = scrapy.Field()
    
    price = scrapy.Field()
    data = scrapy.Field()


