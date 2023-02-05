import scrapy
import json
import time

from selenium.webdriver.common.by import By

from PageRanks.PageRank.items import PagerankItem

from selenium import webdriver
from scrapy import signals
from pydispatch import dispatcher
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")


class PagerankspiderSpider(scrapy.Spider):
    name = 'PageRankSpider'
    allowed_domains = ['careers.tencent.com']
    one_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1675266036366&countryId=&cityId' \
              '=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword=&pageIndex={}&pageSize=10&language=zh' \
              '-cn&area=cn '
    start_urls = ['http://careers.tencent.com/']

    def start_requests(self):
        for page in range(1, 136):
            url = self.one_url.format(page)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response, **kwargs):
        html = response.text
        dic = json.loads(html)
        list_items = dic.get('Data').get('Posts')
        for list_item in list_items:
            page_item = PagerankItem()
            page_item['current_url'] = list_item.get('PostURL').replace('\t', '').replace('\n', '').replace('\r', '')
            yield scrapy.Request(url=page_item['current_url'], callback=self.get_link, cb_kwargs={'item': page_item})

    def get_link(self, response, **kwargs):
        page_item = kwargs['item']
        page_item['page_link'] = []
        driver = webdriver.Chrome(chrome_options=chrome_options)
        main_url = page_item['current_url']
        driver.get(main_url)
        main_handle = driver.window_handles
        links = driver.find_elements(By.CLASS_NAME, "recruit-list-link")
        for link in links:
            link.click()
            driver.implicitly_wait(1)
        all_handles = driver.window_handles
        for handle in all_handles:
            driver.switch_to.window(handle)
            if main_handle[0] != handle:
                page_item['page_link'].append(driver.current_url)
        print("one has been stored")
        driver.quit()
        time.sleep(1)
        yield page_item
