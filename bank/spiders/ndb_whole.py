import json
import re

import scrapy
from scrapy.linkextractor import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
# from datablogger_scraper.items import DatabloggerScraperItem


class HNBSpider(CrawlSpider):
    # The name of the spider
    name = "ndb"
    bank_objects = {}
    page = 0

    # The domains that are allowed (links to other domains are skipped)
    allowed_domains = ["ndbbank.com"]

    # The URLs to start with
    start_urls = ["http://www.ndbbank.com/"]

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
        # filename = './bank/data/' + str(self.page) + '.json'
        if 'http://www.ndbbank.com/pages/english/individuals/' in response.url:
            self.page += 1
            # filename = './bank/data/ndb/html/' + str(self.page) + '.html'

            text = response.selector.xpath('//*[@id="main_container"]/div[4]/div[2]/div[2]').extract_first()
            # cleanr = re.compile('<.*?>')
            # text = re.sub(cleanr, ' ', text)
            # text = re.sub('\s+',' ', text)
            # text = " ".join(text.split())

            account_object = {
                'url': response.url,
                'details': text
            }
            self.bank_objects[self.page] = account_object

            filename_json = './bank/data/ndb/url_map.json'
            with open(filename_json, 'w') as f:
                json.dump(self.bank_objects, f)