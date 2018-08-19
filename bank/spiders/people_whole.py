import json
import re

import scrapy
from scrapy.linkextractor import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
# from datablogger_scraper.items import DatabloggerScraperItem


class DatabloggerSpider(CrawlSpider):
    # The name of the spider
    name = "people"
    object_url = {}
    page = 0

    # The domains that are allowed (links to other domains are skipped)
    allowed_domains = ["www.peoplesbank.lk"]

    # The URLs to start with
    start_urls = ["https://www.peoplesbank.lk/"]

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
        if '/si/' not in response.url and '/ta/' not in response.url:
            heading = str(response.selector.xpath(
                '//*[@id="set_view_url"]/text()').extract_first()).strip()
            accounts = ['Savings Account', 'Current Account', 'Foreign Currency Deposit Accounts', 'Term Deposits']
            if heading in accounts:
                heading = str(response.selector.xpath(
                    '//*[@id="block-system-main"]/div/div/div[2]/div[1]/div/div[2]/h1/text()').extract_first()).strip()
                account_name = str(response.selector.xpath(
                    '//*[@id="block-system-main"]/div/div/div[2]/div[1]/div/div[2]/h1/text()').extract_first())
                details = str(
                    response.selector.xpath(
                        '//*[@id="block-system-main"]/div/div/div[2]/div[2]/div/div[1]/div/span[2]/div/div/div'
                    ).extract_first())

                details_benifits = str(
                    response.selector.xpath(
                        '//*[@id="block-system-main"]/div/div/div[3]/div/div/div/div/div[2]/div'
                    ).extract_first())
                text = details + details_benifits
                cleanr = re.compile('<.*?>')
                text = re.sub(cleanr, ' ', text)
                text = re.sub('\s+', ' ', text)
                # text = " ".join(text.split())

                account_object = {
                    'url': response.url,
                    'bank': 'people',
                    'name': heading,
                    'details': text
                }

                filename_json = './bank/data/people/people_' + str(heading) + '.json'
                with open(filename_json, 'w') as f:
                    json.dump(account_object, f)
