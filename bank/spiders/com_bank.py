import scrapy
from bs4 import BeautifulSoup
from scrapy import Selector


class QuotesSpider(scrapy.Spider):
    name = "combank"
    allowed_domains = 'www.combank.net'
    product_url = []
    deposite_details = []

    def start_requests(self):
        start_url = 'https://www.combank.net/newweb/en/personal/deposits/fixed-deposits'
        yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response):
        sel = Selector(response)
        soup = BeautifulSoup(response.body, "lxml")
        table = soup.find("table")
        # print(table)
        rows = table.findAll('tr')
        data = [[td.findChildren(text=True) for td in tr.findAll("td")] for tr in rows]
        for i in data:
            if i.__len__()>=3:
                self.deposite_details.append({
                    'duration' : i[0][0],
                    'Interest Rate ( p.a.)': i[1][0],
                    'Annual Percentage Rate': i[2][0]
                })
        print(self.deposite_details)
