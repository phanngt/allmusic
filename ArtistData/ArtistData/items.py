# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArtistdataItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    active = scrapy.Field()
    genre = scrapy.Field()
    styles = scrapy.Field()
    biography = scrapy.Field()
    pass
