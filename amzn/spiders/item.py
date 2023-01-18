import MySQLdb
import scrapy
from amzn.app import App
from urllib.parse import urlencode
from datetime import datetime
from amzn.items import AmznItem


def get_url(url):
    payload = {'api_key': App.config("scraper_api_key"), 'url': url}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url

class ItemSpider(scrapy.Spider):
    name = 'item_spider'

    def __init__(self, query='', asin='', **kwargs):
        self.conn = MySQLdb.connect(
            host=App.config("mysql_url"),
            port=App.config("MYSQL_PORT"),
            user=App.config("username"),
            password=App.config("password"),
            database=App.config("MYSQL_DATABASE")
        )
        self.query = query
        self.cur = self.conn.cursor()
        self.asin = asin
        self.cur.execute("SELECT id FROM queries WHERE query=%s", (self.query,))
        self.queryId = self.cur.fetchone()

    def start_requests(self):
        url = f'https://www.amazon.pl/dp/{self.asin}'
        request = scrapy.Request(
            url=get_url(url),
            callback=self.parse_product_page,
            meta={'asin': self.asin, 'queryId': self.queryId}
        )
        yield request


    def parse_product_page(self, response):
        item = AmznItem()
        title = response.xpath('//*[@id="productTitle"]/text()').extract_first().strip().replace(u'\xa0', u'')
        asin = response.meta['asin']
        price = str(response.xpath('//*[@id="corePrice_feature_div"]/div/span/span[1]/text()').extract_first()).replace(u'\xa0', u'').replace('zł', '').replace(',', '.')
        if price == 'None':
            price = '0.00'
        item['asin'] = asin
        item['title'] = title
        item['timestamp'] = datetime.now().strftime("%d-%m-%Y")
        item['price'] = float(price)
        item['queryID'] = response.meta['queryId']

        yield item
