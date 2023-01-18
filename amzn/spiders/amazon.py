import scrapy
from ..items import AmznItem
from datetime import datetime
import MySQLdb
from urllib.parse import urlencode
from amzn.app import App

def get_url(url):
    payload = {'api_key': App.config("scraper_api_key"), 'url': url}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url

class AmazonSpider(scrapy.Spider):
    name = 'amazon'

    def __init__(self):
        self.conn = MySQLdb.connect(
            host=App.config("mysql_url"),
            port=App.config("MYSQL_PORT"),
            user=App.config("username"),
            password=App.config("password"),
            database=App.config("MYSQL_DATABASE")

        )

        self.cur = self.conn.cursor()
        self.cur.execute("""
            SELECT id, query FROM queries
        """)

        self.queries = self.cur.fetchall()

    def start_requests(self):
        for query in self.queries:
            url = 'https://www.amazon.pl/s?' + urlencode({'k': query[1]})
            request = scrapy.Request(
                url=get_url(url),
                callback=self.parse_keyword_response,
                meta={'query': query[0]}
            )
            yield request


    def parse_keyword_response(self, response):
        products = response.xpath('//div[@data-asin][@data-component-type="s-search-result"]')
        next = response.xpath('//*[@class="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]/@href').extract_first()

        for product in products:
            asin = product.xpath('@data-asin').extract_first()
            product_url = f"https://www.amazon.pl/dp/{asin}"

            yield scrapy.Request(
                url=get_url(product_url),
                callback=self.parse_product_page,
                meta={'asin': asin, 'query': response.meta.get('query')}

            )

        print(f"-------------------------------- wartość next: {next} --------------------------------")
        if next is not None:
            print(f":::::::::::::::::::::: next page clicked ::::::::::::::::::::::")
            yield response.follow(
                f"https://www.amazon.pl{next}",
                callback=self.parse_keyword_response,
                meta={'query': response.meta.get('query')}
            )
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
        item['queryID'] = response.meta['query']

        yield item


