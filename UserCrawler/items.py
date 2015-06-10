# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UserItem(scrapy.Item):
    uid = scrapy.Field()
    pid = scrapy.Field()
    name = scrapy.Field()
    follow_num = scrapy.Field()
    fan_num = scrapy.Field()
    post_num = scrapy.Field()
    verify = scrapy.Field()
