import json
import unidecode
import scrapy
import re
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
    start_urls = ["http://web.boc.lk/boc/index.php?route=product/category&path=87"]

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
            if 'route=product/category&path=87'in response.url:
                heading = response.selector.xpath('/html/body/div[1]/div/div[3]/div[2]/div/div[2]/div/div[1]/h1/text()').extract_first()
                print(heading)
                account_deatils = response.selector.xpath('//*[@id="corporate-page"]/div[1]').extract_first()
                text = account_deatils
                text = unidecode.unidecode(str(text))
                cleanr = re.compile('<.*?>')
                text = re.sub(cleanr, ' ', text)
                text = re.sub('\s+', ' ', text)
                # text = " ".join(text.split())

                account_object = {
                    'url': response.url,
                    'bank': 'boc',
                    'name': heading,
                    'details': text
                }

                filename_json = './bank/data/boc/boc_' + str(heading) + '.json'
                with open(filename_json, 'w') as f:
                    json.dump(account_object, f)