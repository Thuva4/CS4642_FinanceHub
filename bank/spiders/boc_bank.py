import scrapy
from bs4 import BeautifulSoup
from scrapy import Selector


class QuotesSpider(scrapy.Spider):
    name = "boc"
    allowed_domains = 'web.boc.lk'
    product_url = []

    def start_requests(self):
        start_url = 'http://web.boc.lk/boc/index.php?route=rates/rates'
        yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response):
        sel = Selector(response)
        # print(type(response.body))
        soup = BeautifulSoup(response.body, "lxml")
        # print(soup.title)
        # print(soup.a)
        # i = 0
        # for link in soup.find_all('a'):
        #     if 'product' in link.get('href') and 'http' in link.get('href'):
        #         i+=1
        #         # print(link.get('href'))
        #         self.product_url.append(link.get('href'))
        # for url in self.product_url:
        #     yield scrapy.Request(url=url, callback=self.parse_product, dont_filter=True)

        table = soup.find("table", {'class':'TB1'})
        rows = table.findAll('tr')
        data = [[td.findChildren(text=True) for td in tr.findAll("td")] for tr in rows]
        for i in data:
            print(i)

    def parse_product(self, response):
        sel = Selector(response)
        print(type(response.body))
        soup = BeautifulSoup(response.body, "lxml")
        print(soup.h3)