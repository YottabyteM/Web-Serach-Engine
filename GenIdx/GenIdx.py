# 主要是为了实现将json文件导入ElasticSearch
import json
import time
from datetime import datetime

from elasticsearch import Elasticsearch as ES
from elasticsearch.helpers import bulk
USERNAME = "elastic"
PASSWORD = "g_PqbE3r*3Dqx+DzOYBr"
ELATICSEARCH_ENDPOINT = "localhost:9200"
ELASTCSEARCH_CERT_PATH = "D:\\matlab\\elasticsearch\\elasticsearch\\config\\certs\\http_ca.crt"
url = f'https://{USERNAME}:{PASSWORD}@{ELATICSEARCH_ENDPOINT}'


class My_Elastic:
    def __init__(self, index_name):
        """
        主要是借用ElasticSearch搭建自己的搜索框架
        :param index_name: 索引的名称
        """
        self.index_name = index_name
        self.es = ES(url, ca_certs=ELASTCSEARCH_CERT_PATH, verify_certs=True)

    def create_index(self):
        """
        这里主要是初始化索引
        """

        settings = {
            "index": {"number_of_replicas": 2},
            "analysis": {
                "filter": {
                    "ngram_filter": {
                        "type": "edge_ngram",
                        "min_gram": 2,
                        "max_gram": 15,
                    }
                },
                "analyzer": {
                    "ngram_analyzer": {
                        "type": "custom",
                        "tokenizer": "ik_smart",
                        "filter": ["lowercase", "ngram_filter"],
                    }
                }
            }
        }
        mappings = {
            "properties": {
                "RecruitPostName": {
                    'type': 'keyword'
                },
                "LocationName": {
                    'type': 'text'
                },
                "Responsibility": {
                    'type': 'text'
                },
                "LastUpdateTime": {
                    'type': 'date'
                },
                "CategoryName": {
                    'type': 'text'
                },
                "PostURL": {
                    'type': 'text'
                },
                "Page_rank": {
                    'type': 'keyword'
                },
                "Cluster": {
                    'type': 'keyword'
                }
            }
        }
        if self.es.indices.exists(index=self.index_name):
            print("The index has already existed, going to remove it")
            self.es.options(ignore_status=404).indices.delete(index=self.index_name)
        self.es.indices.create(index=self.index_name, settings=settings, mappings=mappings)

    def debug_info(self):
        print(self.es.info())

    def insert_data(self, input_file):
        f = open(input_file, 'r', encoding='UTF-8')
        data = []
        for line in f.readlines():
            data.append(line.strip())
        f.close()
        ACTIONS = []
        bulk_num = 100
        for list_line in data:
            list_line = eval(list_line)
            date = str(list_line["LastUpdateTime"]).replace(']', '').replace('[', '').replace('\'', '')
            date = date.replace('年', '/').replace('月', '/').replace('日', '')
            date = datetime.strptime(date, '%Y/%m/%d').date()
            action = {
                "_index": self.index_name,
                "_source": {
                    "RecruitPostName": list_line["RecruitPostName"][0],
                    "LocationName": list_line["LocationName"][0],
                    "Responsibility": list_line["Responsibility"][0],
                    "LastUpdateTime": date,
                    "CategoryName": list_line["CategoryName"][0],
                    "PostURL": list_line["PostURL"],
                    "Page_rank": list_line["Page_rank"],
                    "Cluster": list_line["Cluster"]
                }
            }
            ACTIONS.append(action)
            if len(ACTIONS) == bulk_num:
                print('插入一批数据')
                success, _ = bulk(self.es, ACTIONS, index=self.index_name, raise_on_error=True)
                del ACTIONS[0:len(ACTIONS)]

        if len(ACTIONS) > 0:
            success, _ = bulk(self.es, ACTIONS, index=self.index_name, raise_on_error=True)
            del ACTIONS[0:len(ACTIONS)]
            print('last_bulk finished!')


if __name__ == '__main__':
    My_ES = My_Elastic("tecent_recruit")
    My_ES.create_index()
    My_ES.insert_data("./WithCluster.json")
