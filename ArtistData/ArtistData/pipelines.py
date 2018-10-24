# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import sys

from scrapy import crawler
from scrapy.exceptions import CloseSpider


class ArtistdataPipeline(object):
    count = 0
    def open_spider(self, spider):
        self.file = open('artists.json', 'wb')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        self.count += 1
        if self.count > 10:
            self.file.close()
            raise CloseSpider("Enough, I need to eat")
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line.encode('utf-8'))
        return item
