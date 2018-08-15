import json

import scrapy
from scrapy.linkextractor import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
# from datablogger_scraper.items import DatabloggerScraperItem


class DatabloggerSpider(CrawlSpider):
    # The name of the spider
    name = "bocwhole"
    object_url = {}
    page = 0

    # The domains that are allowed (links to other domains are skipped)
    allowed_domains = ["web.boc.lk"]

    # The URLs to start with
    start_urls = ["http://web.boc.lk/boc/index.php"]

    # This spider has one rule: extract all (unique and canonicalized) links, follow them and parse them using the parse_items method
    rules = [
        Rule(
            LinkExtractor(
                canonicalize=True,
                unique=True
            ),
            follow=True,
            callback="parse_item"
        )
    ]

    # Method which starts the requests by visiting all URLs specified in start_urls
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)


    # Method for parsing items
    def parse_item(self, response):

        if 'sinhala' not in response.url and 'tamil' not in response.url:
            if 'product' in response.url and 'desc=1'in response.url:
                self.page += 1
                filename = './bank/data/boc/html/' + str(self.page) + '.html'
                with open(filename, 'wb') as f:
                    # object = {
                    #     'url': response.url
                    # }
                    # json.dump(object, f)
                    self.object_url[self.page] = response.url

                    f.write(response.body)
                filename_json = './bank/data/boc/url_map.json'
                with open(filename_json, 'w') as f:
                    json.dump(self.object_url, f)
