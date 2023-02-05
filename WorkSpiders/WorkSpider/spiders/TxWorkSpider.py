# -- coding: utf-8 --
import json
import scrapy
from WorkSpiders.WorkSpider.items import WorkspiderItem


class TxworkspiderSpider(scrapy.Spider):
    name = 'TxWorkSpider'
    allowed_domains = ['careers.tencent.com']
    one_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1675091286720&countryId=&cityId' \
              '=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword=&pageIndex={}&pageSize=10&language=zh' \
              '-cn&area=cn '
    start_urls = ['https://careers.tencent.com/search.html']

    def start_requests(self):
        for page in range(1, 136):
            url = self.one_url.format(page)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response, **kwargs):
        html = response.text
        dic = json.loads(html)
        list_items = dic.get('Data').get('Posts')
        for list_item in list_items:
            work_item = WorkspiderItem()
            work_item['RecruitPostName'] = list_item.get('RecruitPostName').replace('\t', '').replace('\n', '').replace(
                '\r', ''),
            work_item['LocationName'] = list_item.get('LocationName').replace('\t', '').replace('\n', '').replace(
                '\r', ''),
            work_item['Responsibility'] = list_item.get('Responsibility').replace('\t', '').replace('\n', '').replace(
                '\r', ''),
            work_item['LastUpdateTime'] = list_item.get('LastUpdateTime').replace('\t', '').replace('\n', '').replace(
                '\r', ''),
            work_item['CategoryName'] = list_item.get('CategoryName').replace('\t', '').replace('\n', '').replace(
                '\r', ''),
            work_item['PostURL'] = list_item.get('PostURL').replace('\t', '').replace('\n', '').replace(
                '\r', '')
            yield work_item
