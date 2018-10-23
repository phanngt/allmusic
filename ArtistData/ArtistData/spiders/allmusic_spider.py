# -*- coding: utf-8 -*-
import scrapy
from items import ArtistdataItem

class BaseSpider(scrapy.Spider):
    #
    attribute_paths = {}
    allowed_data_link = ''
    start_urls = []

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_info)

    def parse_info(self, response):
        result = ArtistdataItem()
        if self.allowed_data_link in response._url:
            for key in self.attribute_paths:
                result[key] = response.xpath(self.attribute_paths[key]).extract_first()
            yield result
        else:
            for url in response.xpath('//a/@href').extract():
                yield scrapy.Request(url, callback=self.parse_info)


class AllMusicSpiderSpider(BaseSpider):
    name = 'allmusic_spider'
    allowed_domains = ['allmusic.com']
    start_urls = [
        'https://www.allmusic.com/artist/adele-mn0000503460',
        'https://www.allmusic.com/artist/justin-timberlake-mn0000312890'
    ]
    allowed_data_link = 'allmusic.com/artist'
    attribute_paths = {
        "name": '//*[@class = "aliases"]/div/div/text()',
        "birthdate": '//*[contains(@href, "date")]/text()'
    }


class MySpider(scrapy.Spider):
    name = 'example.com'
    allowed_domains = ['lipsum.com']

    def start_requests(self):
        yield scrapy.Request('https://www.lipsum.com/', self.parse)
        yield scrapy.Request('https://www.lipsum.com/banners/', self.parse)

    def parse(self, response):
        for h1 in response.xpath('//h1').extract():
            yield ArtistdataItem(name=h1)

        for url in response.xpath('//a/@href').extract():
            yield scrapy.Request(url, callback=self.parse)

