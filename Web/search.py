import codecs
import time
from datetime import datetime

from elasticsearch import Elasticsearch as ES

USERNAME = "elastic"
PASSWORD = "g_PqbE3r*3Dqx+DzOYBr"
ELASTICSEARCH_ENDPOINT = "localhost:9200"
ELASTICSEARCH_CERT_PATH = "D:\\matlab\\elasticsearch\\elasticsearch\\config\\certs\\http_ca.crt"
url = f'https://{USERNAME}:{PASSWORD}@{ELASTICSEARCH_ENDPOINT}'
LOG_PATH = "./logs.txt"
TIME_PATH = "./time.txt"
LOG_HEAD = "[SEARCH_LOG]"


class My_Search:
    def __init__(self, index_name):
        self.index_name = index_name
        self.es = ES(url, ca_certs=ELASTICSEARCH_CERT_PATH, verify_certs=True)

    def search_in_web(self, word, Url):
        """
        主要是在对应的网址下进行搜索，比如在我们的腾讯里面除了careers.tencent.com这一国内域名，
        还有tencent.wd1.myworkdayjobs.com这些外网域名，我们可以在对应域名下进行短语搜索
        :param word:查询的短语或者内容
        :param Url:想要查询的网址域名
        :return:返回查询的结果
        """
        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "wildcard": {"PostURL": "*" + Url + "*"}
                        },
                        {
                            "multi_match":
                                {
                                    "query": word,
                                    "fields": ["RecruitPostName", "Responsibility"]
                                }
                        }
                    ]
                }
            },
            "size": 7  # 一页大小
        }
        self.log(word)
        return self.es.search(index=self.index_name, body=body)

    def search_by_time(self, word, time1, time2=None):
        """
        主要是在对应的网址下进行搜索，比如在我们的腾讯里面除了careers.tencent.com这一国内域名，
        还有tencent.wd1.myworkdayjobs.com这些外网域名，我们可以在对应域名下进行短语搜索
        :param time2: 终止时间
        :param time1: 起始时间
        :param word:查询的短语或者内容
        :return:返回查询的结果
        """
        date1 = datetime.strptime(time1, '%Y-%m-%d').date()
        if time2 is not None:
            date2 = datetime.strptime(time2, '%Y-%m-%d').date()
        else:
            date2 = datetime.now().date()
        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "range": {"LastUpdateTime": {"gt": date1}},
                        },
                        {
                            "range": {"LastUpdateTime": {"lte": date2}},
                        },
                        {
                            "multi_match":
                                {
                                    "query": word,
                                    "fields": ["RecruitPostName", "Responsibility"]
                                }
                        }
                    ]
                }
            },
            "size": 7  # 一页大小
        }
        self.log(word)
        return self.es.search(index=self.index_name, body=body)

    def search_by_words(self, words):
        """
        主要用于短语查询
        :param words: 要输入的短语
        :return: 返回json形式的结果
        """
        body = {
            "query": {
                "multi_match": {
                    "query": words,
                    "fields": ["RecruitPostName", "Responsibility"]
                }
            },
            "size": 7  # 一页大小
        }
        self.log(words)
        return self.es.search(index=self.index_name, body=body)

    def search_by_cluster(self, cluster):
        body = {
            "query": {
                "term": {
                    "Cluster": str(cluster)
                }
            },
            "size": 7  # 一页大小
        }
        return self.es.search(index=self.index_name, body=body)

    def search_by_match(self, model):
        """
        主要是为了实现通配符查找，即输入正则表达式输出结果
        :param model: 要查找的通配符模式，以字符串形式给出
        :return: 返回查找结果
        """
        body = {
            "query": {
                "wildcard": {
                    "RecruitPostName": model
                }
            }
        }
        self.log(model.replace('*', ''))
        return self.es.search(index=self.index_name, body=body)

    def get_photo(self, words):
        """
        主要是查找网页快照
        :param words: 要查找
        :return: 返回文件路径
        """
        return "E:\\WorkSpace\\pycharmProject\\IRFinal\\SnapShot\\data\\['" + words + "'].png"

    def log(self, info_log):
        """
        主要是打印日志
        :param info_log: 要打印的日志信息，应该为json模式，要讲明白到底找到没，方便后续继续推荐
        :return: None
        """
        f = codecs.open(filename=LOG_PATH, mode='a', encoding='utf-8')
        f1 = codecs.open(filename=TIME_PATH, mode='a',encoding='utf-8')
        Time = time.time()
        f.write(info_log + ' ' + '\n')
        f1.write(str(Time) + '\n')
        f.close()
        f1.close()

    # def synthesize_search(self,
    #                       should_have_complete,
    #                       just_have_any,
    #                       should_not_have,
    #                       time_from,
    #                       time_to,
    #                       Url,
    #                       position=None
    #                       ):
    #     """
    #     综合搜索，最终应该调用的模块应该是这一模块
    #     :param should_have_all: 应该包含全部的关键词
    #     :param should_have_complete:应该包含完整的关键词
    #     :param just_have_any:包含任意的关键词即可
    #     :param should_not_have:不应该包含的关键词
    #     :param time_from:时间开始于
    #     :param time_to:时间结束于
    #     :param position:应该出现在的字段
    #     :param Url:应该处在的域名
    #     :return:返回所有的搜索结果，并且分页呈现
    #     """
    #     date1 = datetime.strptime(time_from, '%Y-%m-%d').date()
    #     if time_to is not None:
    #         date2 = datetime.strptime(time_to, '%Y-%m-%d').date()
    #     else:
    #         date2 = datetime.now().date()
    #     if position is None:
    #         body = {
    #             "query": {
    #                 "bool": {
    #                     "must": {
    #                         "match_phrase": {
    #                             "RecruitPostName": just_have_any,
    #                             "Responsibility": just_have_any,
    #                             "LocationName": just_have_any
    #                         },
    #                         "wildcard": {"PostURL": "*" + Url + "*"},
    #                         "range": {
    #                             "LastUpdateTime": {
    #                                 "gt": date1,
    #                                 "lte": date2
    #                             }
    #                         }
    #                     },
    #                     "must_not": {
    #                         "multi_match": {
    #                             "query": should_not_have,
    #                             "fields": ["RecruitPostName", "Responsibility", ]
    #                         }
    #                     }
    #                 }
    #             }
    #         }
    #     else:
    #         body = {
    #             "query": {
    #                 "bool": {
    #                     "must": {
    #                         "match_phrase": {
    #                             position: just_have_any,
    #                         },
    #                         "wildcard": {"PostURL": "*" + Url + "*"},
    #                         "range": {
    #                             "LastUpdateTime": {
    #                                 "gt": date1,
    #                                 "lte": date2
    #                             }
    #                         }
    #                     },
    #                     "must_not": {
    #                         "multi_match": {
    #                             "query": should_not_have,
    #                             "fields": [position]
    #                         }
    #                     }
    #                 }
    #             }
    #         }
    #     return self.es.search(index=self.index_name, body=body)


if __name__ == '__main__':
    search = My_Search("tecent_recruit")
    Words = "*Market*"
    # should_have_complete = "运维保障系统"
    # just_have_any = "商务助理"
    # should_not_have = "工程师"
    # time_from = "2023-1-1"
    # time_to = "2023-2-3"
    # Url = "careers.tencent.com"
    position = None
    # res = search.search_in_web(Words, "careers.tencent.com")
    res = search.search_by_match(Words)
    # res = search.search_by_time(Words, "2023-1-1")
    # res = search.synthesize_search(should_have_complete, just_have_any, should_not_have, time_from,
    #                                time_to, Url, position)
    print(res)
