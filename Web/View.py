import os.path
import time

import streamlit as st
from search import My_Search as Search
from PIL import Image
import streamlit.components.v1 as components
from Personalized import Personalized_Search as ps, Personalized_Recommend as pr


class Web_View:
    def __init__(self, index_name):
        self.search = Search(index_name)
        self.header = "Q-Search"
        self.state = 1
        self.res = None

    def process_search(self, words=None, Url=None, time1=None, time2=None, model=None, cluster=None):
        if self.state == 1:
            self.res = self.search.search_in_web(words, Url)
        elif self.state == 2:
            self.res = self.search.search_by_time(words, time1, time2)
        elif self.state == 3:
            self.res = self.search.search_by_words(words)
        elif self.state == 4:
            self.res = self.search.search_by_match(model)
        elif self.state == 5:
            my_ps = ps()
            self.res = my_ps.new_res(self.search.search_by_words(words), 7)
        elif self.state == 6:
            self.res = self.search.search_by_cluster(cluster)
        else:
            print("Wrong Type")

    def show_html(self, href, Name):
        components.html(
            """
            <body>
                <p><a href={}><cite>{}</cite></a></p>
            </body>
            """.format(href, Name),
            height=50,
        )

    def show_res(self):
        if self.res is not None:
            if self.state != 5:
                search_contents = self.res['hits']['hits']
            else:
                search_contents = self.res
            for search_content in search_contents:
                source = search_content['_source']
                image_path = self.search.get_photo(source['RecruitPostName'])
                self.show_html(source['PostURL'], source['RecruitPostName'])
                if os.path.exists(image_path):
                    image = Image.open(image_path)
                    st.image(image, caption=source['RecruitPostName'] + " SnapShot", width=50)

    def run(self):
        st.header(self.header, anchor=None)
        st.info('1为域名搜索，2为时间范围搜索，3为短语搜索，4为通配搜索，5为个性化查询，6为个性化推荐', icon="ℹ️")
        self.state = st.number_input("number_input", min_value=-10, max_value=10, value=2, step=2, help="testing")
        text = None
        if self.state != 6:
            text = st.text_input("搜索输入框", value="", max_chars=None, key=None, type="default",
                                 help=None, autocomplete=None, on_change=None, args=None,
                                 kwargs=None, placeholder="请输入想要搜索的内容", disabled=False, label_visibility="visible")
        if self.state == 1:
            url = st.text_input("输入框", value="", max_chars=None, key=None, type="default",
                                help=None, autocomplete=None, on_change=None, args=None,
                                kwargs=None, placeholder="请输入限制的域名", disabled=False, label_visibility="visible")
            if text != "" and url != "":
                self.process_search(words=text, Url=url)
        elif self.state == 2:
            time1 = st.text_input("输入框", value="", max_chars=None, key=None, type="default",
                                  help=None, autocomplete=None, on_change=None, args=None,
                                  kwargs=None, placeholder="请输入开始时间，输入形式应为%YY-%MM-%DD", disabled=False, label_visibility="visible")
            time2 = st.text_input("输入框", value="", max_chars=None, key=None, type="default",
                                  help=None, autocomplete=None, on_change=None, args=None,
                                  kwargs=None, placeholder="请输入截止时间，输入形式应为%YY-%MM-%DD", disabled=False, label_visibility="visible")
            if time1 != "" and time2 != "":
                self.process_search(words=text, time1=time1, time2=time2)
        elif self.state == 3:
            if text != "":
                self.process_search(words=text)
        elif self.state == 4:
            if text != "":
                self.process_search(model=text)
        elif self.state == 5:
            if text != "":
                self.process_search(words=text)
        elif self.state == 6:
            my_pr = pr()
            self.process_search(cluster=my_pr.get_cluster())
        else:
            print("Wrong Type")
        self.show_res()


if __name__ == '__main__':
    my_Web = Web_View("tecent_recruit")
    my_Web.run()
