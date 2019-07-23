# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Music163Item(scrapy.Item):

    table_name = 'music_comment'

    id = scrapy.Field()
    artist = scrapy.Field()
    music = scrapy.Field()
    comments = scrapy.Field()
