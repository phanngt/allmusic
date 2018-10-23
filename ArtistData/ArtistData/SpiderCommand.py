from scrapy import cmdline

#cmdline.execute('scrapy genspider allmusic_spider allmusic.com'.split())
cmdline.execute('scrapy crawl allmusic_spider'.split())
#cmdline.execute('scrapy crawl example.com'.split())