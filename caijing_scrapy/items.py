# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    only_id = scrapy.Field()
    title = scrapy.Field()
    body = scrapy.Field()
    put_time = scrapy.Field()

class TopicItem(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    only_id = scrapy.Field()
    title = scrapy.Field()
    body = scrapy.Field()
    put_time = scrapy.Field()    
