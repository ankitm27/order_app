import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import csv
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    # f = open("url.txt")
    # start_urls = ["https://www.liveyoursport.com/squash/?search_query=&page="+ str(page_num) + "&limit=36&sort=featured&category=353&is_category_page=1" for page_num in xrange(1,18)]
    f = open("url.txt")
    start_urls = [url.strip() for url in f.readlines()]
    f.close()


    def parse(self, response):

        # product_links = []
        # f = open('url_file.txt', 'a')
        # for i in response.xpath('//div[contains(@class,"ProductImage QuickView")]/a/@href').extract():
            # product_links.append(i)
            # f.write(i + '\n')


        main_list = []
        product_list = []
        f = open('data.csv', 'ab')
        w = csv.writer(f,dialect='excel',delimiter=',', quoting=csv.QUOTE_NONNUMERIC)

        for pro_name in response.xpath('//h1/text()').extract():
            product_list.append(pro_name)
        for price in response.xpath('//em[contains(@class,"ProductPrice VariationProductPrice")]/text()').extract():

            product_list.append(price)
        product_list.append(response.request.url)
        for des in response.xpath('//div[contains(@class,"prod-short-desc")]/text()').extract():
            product_list.append(des)
        for des in response.xpath('//span[contains(@class,"prod-descr")]/p/text()').extract():
            product_list.append(des)
        if len(product_list) > 2:
            main_list.append(product_list)
            for item1 in main_list:
                try:
                    w.writerows([item1])
                except:
                    pass
        f.close()
