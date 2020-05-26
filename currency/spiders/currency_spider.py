# python -m scrapy runspider currency.py
import scrapy
from datetime import datetime
import time
import csv
import os.path

class CurrencySpider(scrapy.Spider):
    name = 'currency'
    start_urls = ['http://www.livecharts.co.uk/currency-strength.php']

    def getCurrencyData(self, response):
        now = datetime.now()
        list = []
        to_check = ['USD', 'EURO', 'CAD', 'JPY']
        for currency in response.css('#rate-outercontainer'):
            currency_name = currency.css('#map-innercontainer-symbol::text').get()
            if not currency_name in to_check :
                continue
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

            list.append({'date': now.strftime("%d/%m/%Y %H:%M:%S"), 'currency': currency_name, 'strength': currenct_str})
        return list

    def parse(self, response):
        data = self.getCurrencyData(response)
        now = datetime.now()
        # f = open(now.strftime("%d-%m-%Y")+"_currency.csv", "a")
        # f.write(str(data))
        # f.close()
        filename = now.strftime("%d-%m-%Y")+"_currency.csv"
        self.write_csv(data, filename)

        return data

    def write_csv(self, data, filename):
        if(not os.path.exists(filename)):
            with open(filename, 'w+', newline='') as outf:
                writer = csv.DictWriter(outf, data[0].keys())
                writer.writeheader()
                for row in data:
                    writer.writerow(row)
        else:
            with open(filename, 'a+', newline='') as outf:
                writer = csv.DictWriter(outf, data[0].keys())
                for row in data:
                    writer.writerow(row)