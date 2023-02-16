import scrapy
from scrapy import Selector, Request

from spidertest.items import DiseaseItem


class YoulaiSpider(scrapy.Spider):
    name = "youlai"
    allowed_domains = ["www.youlai.cn"]
    # start_urls = ["http://www.youlai.cn/"]

    def start_requests(self):
        for index in range(1, 2332):  # 我们这里最多是1 - 2331
            yield Request(url=f"https://www.youlai.cn/dise/{index}.html")

    def parse(self, response):
        selector = Selector(response)
        disease_item = DiseaseItem()
        a = selector.xpath("/html/body/div[2]/div/p/text()").get()
        b = selector.xpath("/html/body/div[3]/div[1]/dl/dt/p[2]/span/text()").get()
        c = selector.xpath("/html/body/div[3]/div[1]/dl/dt/p[4]/span/text()").get()
        d = selector.xpath("/html/body/div[3]/div[1]/dl/dd[1]/p[5]/span/text()").get()
        e = selector.xpath("/html/body/div[3]/div[1]/dl/dd[1]/p[1]/span/text()").get()
        disease_item['disName'] = a
        disease_item['disLoc'] = b
        disease_item['disTreat'] = c
        disease_item['disDrug'] = d
        disease_item['disSymptom'] = e
        yield disease_item
