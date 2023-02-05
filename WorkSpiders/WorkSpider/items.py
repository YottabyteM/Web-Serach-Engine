# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WorkspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    RecruitPostName = scrapy.Field()  # 职位名
    LocationName = scrapy.Field()  # 地址
    Responsibility = scrapy.Field()  # 工作要求
    LastUpdateTime = scrapy.Field()  # 更新时间
    CategoryName = scrapy.Field()  # 工作种类
    PostURL = scrapy.Field()  # 对应的网址

