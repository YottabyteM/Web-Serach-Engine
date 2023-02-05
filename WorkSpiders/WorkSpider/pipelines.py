# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json, codecs, os
# useful for handling different item types with a single interface
import WorkSpiders.WorkSpider.items as form_item


class WorkspiderPipeline:
    def __init__(self):
        # 文件的位置
        store_file1 = os.path.dirname(__file__) + 'Work.json'
        # 打开文件，设置编码为utf-8
        self.file1 = codecs.open(filename=store_file1, mode='wb', encoding='utf-8')

    def process_item(self, item, spider):
        if isinstance(item, form_item.WorkspiderItem):
            text = json.dumps(dict(item), ensure_ascii=False) + ",\n"
            self.file1.write(text)
            return item

    def close_spider(self, spider):
        self.file1.close()
