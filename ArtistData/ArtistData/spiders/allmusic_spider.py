# -*- coding: utf-8 -*-
import scrapy
from items import ArtistdataItem

class BaseSpider(scrapy.Spider):
    #
    attribute_paths = {}
    allowed_data_link = ''
    start_urls = []
    base_url = ''

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_info)

    def parse_info(self, response):
        result = ArtistdataItem()
        if self.allowed_data_link in response.url:
            for key in self.attribute_paths:
                result_list = response.xpath(self.attribute_paths[key]).extract()
                if len(result_list) == 1:
                    result[key] = result_list[0].strip().encode('ascii', 'ignore').decode("utf-8")
                else:
                    result[key] = [x.strip() for x in result_list]
            yield result
        for url in response.xpath('//body//*[@href]/@href').extract():
            yield scrapy.Request(response.urljoin(url), callback=self.parse_info)


class AllMusicSpiderSpider(BaseSpider):
    name = 'allmusic_spider'
    allowed_domains = ['allmusic.com']
    base_url = 'https://www.allmusic.com'
    start_urls = [
        'https://www.allmusic.com'
    ]
    allowed_data_link = 'allmusic.com/artist'
    attribute_paths = {
        "name": '//body//*[@class = "artist-name"]/text()',
        "active": '//body//*[@class = "active-dates"]/div/text()',
        "genre": '//body//*[@class = "genre"]/div/a/text()',
        "styles": '//body//*[@class = "styles"]/div/a/text()'
    }
