# -*- coding: utf-8 -*-
import scrapy
from items import ArtistdataItem


class BaseSpider(scrapy.Spider):
    #
    attribute_paths = {}
    allowed_data_link = ''
    start_urls = []
    base_url = ''
    bio = ''

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if self.allowed_data_link in response.url:
            result = ArtistdataItem()
            for key in self.attribute_paths:
                result_list = response.xpath(self.attribute_paths[key]).extract()
                if len(result_list) == 1:
                    result[key] = result_list[0].strip().encode('ascii', 'ignore').decode("utf-8")
                else:
                    result[key] = [x.strip() for x in result_list]

            link = response.xpath(self.bio).extract_first()
            request = scrapy.Request(url=response.urljoin(link), callback=self.parser_bio, priority=1)
            request.meta['item'] = result
            yield request
        for url in response.xpath('//body//*[@href]/@href').extract():
            yield scrapy.Request(response.urljoin(url), callback=self.parse)

    def parser_bio(self, response):
        item = response.meta['item']
        paragraph = response.xpath('//body//section[@class = "biography"]/div/text()').extract()
        biography = ''
        for line in paragraph:
            biography += line.strip().encode('ascii', 'ignore').decode("utf-8")
        item['biography'] = biography
        return item


class AllMusicSpiderSpider(BaseSpider):
    name = 'allmusic_spider'
    allowed_domains = ['allmusic.com']
    base_url = 'https://www.allmusic.com'
    start_urls = [
        'https://www.allmusic.com/'
    ]
    allowed_data_link = 'allmusic.com/artist'
    attribute_paths = {
        "name": '//body//*[@class = "artist-name"]/text()',
        "active": '//body//*[@class = "active-dates"]/div/text()',
        "genre": '//body//*[@class = "genre"]/div/a/text()',
        "styles": '//body//*[@class = "styles"]/div/a/text()'
    }
    bio = '//*[@class = "tab biography"]/a/@href'
