# python -m scrapy runspider currency.py
import scrapy
from datetime import datetime
class CurrencySpider(scrapy.Spider):
    name = 'currency'
    start_urls = ['http://www.livecharts.co.uk/currency-strength.php']

    def parse(self, response):
        now = datetime.now()
        for currency in response.css('#rate-outercontainer'):
            currency_name = currency.css('#map-innercontainer-symbol::text').get()
            currenct_str = 1
            weak3 = True if currency.css('#map-innercontainer-weak3') else False
            weak2 = True if currency.css('#map-innercontainer-weak2') else False
            weak1 = True if currency.css('#map-innercontainer-weak1') else False
            strong1 = True if currency.css('#map-innercontainer-strong1') else False
            strong2 = True if currency.css('#map-innercontainer-strong2') else False
            strong3 = True if currency.css('#map-innercontainer-strong3') else False

            if strong3:
                currenct_str = 6
            elif  strong2:
                currenct_str = 5
            elif (strong1):
                currenct_str = 4
            elif (weak1):
                currenct_str = 3
            elif (weak2):
                currenct_str = 2
            else:
                currenct_str = 1

            yield {'date': now.strftime("%d/%m/%Y %H:%M:%S"), 'currency': currency_name, 'strength': currenct_str}