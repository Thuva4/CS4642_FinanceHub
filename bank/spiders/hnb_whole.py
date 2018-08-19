import json
import re

import scrapy
from scrapy.linkextractor import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider


# from datablogger_scraper.items import DatabloggerScraperItem
import unidecode

class HNBSpider(CrawlSpider):
    # The name of the spider
    name = "hnb"
    bank_objects = {}
    page = 0

    # The domains that are allowed (links to other domains are skipped)
    allowed_domains = ["hnb.net"]

    # The URLs to start with
    start_urls = ["https://www.hnb.net/"]

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
        if 'https://www.hnb.net/personal/savings' in response.url:
            # filename = './bank/data/hnb/html/' + str(self.page) + '.html'
            heading = response.selector.xpath('//*[@id="TopInner"]/div/div[1]/div/div/h1/text()').extract_first()
            print(heading)
            account_deatils = response.selector.xpath('//*[@id="Start-saving"]').extract_first()
            account_offers = response.selector.xpath('//*[@id="offer-you"]').extract_first()
            text = account_deatils + account_offers
            text = unidecode.unidecode(str(text))
            cleanr = re.compile('<.*?>')
            text = re.sub(cleanr, ' ', text)
            text = re.sub('\s+', ' ', text)
            # text = " ".join(text.split())

            account_object = {
                'url': response.url,
                'bank': 'hnb',
                'name': heading,
                'details': text
            }
            self.bank_objects[self.page] = account_object

            filename_json = './bank/data/hnb/hnb_'+ str(heading) + '.json'
            with open(filename_json, 'w') as f:
                json.dump(account_object, f)