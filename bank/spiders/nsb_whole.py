import json
import re

import scrapy
from scrapy.linkextractor import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
# from datablogger_scraper.items import DatabloggerScraperItem


class HNBSpider(CrawlSpider):
    # The name of the spider
    name = "nsb"
    bank_objects = {}
    page = 0

    # The domains that are allowed (links to other domains are skipped)
    allowed_domains = ["nsb.lk"]

    # The URLs to start with
    start_urls = ["http://www.nsb.lk/"]

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
        # if '/si/' not in response.url and '/ta/' not in response.url:
        if 'http://www.nsb.lk/product/' in response.url:
            # filename = './bank/data/nsb/html/' + str(self.page) + '.html'
            heading = response.selector.xpath(
                '/html/body/div[1]/section/div/div/div[1]/div/div/h2/text()').extract_first()
            text = response.selector.xpath('//html/body/div[1]/section/div/div/div[1]/div/div').extract_first()
            cleanr = re.compile('<.*?>')
            text = re.sub(cleanr, ' ', text)
            text = re.sub('\s+',' ', text)
            # text = " ".join(text.split())

            account_object = {
                'url': response.url,
                'bank': 'nsb',
                'name': heading,
                'details': text
            }

            filename_json = './bank/data/nsb/nsb_' + str(heading) + '.json'
            with open(filename_json, 'w') as f:
                json.dump(account_object, f)