# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# class SpidertestItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass

class DiseaseItem(scrapy.Item):
    disName = scrapy.Field()  # 疾病名称
    disLoc = scrapy.Field()  # 发病部位
    disTreat = scrapy.Field()  # 治疗方式
    disDrug = scrapy.Field()  # 治疗药物
    disSymptom = scrapy.Field()  # 相关症状


