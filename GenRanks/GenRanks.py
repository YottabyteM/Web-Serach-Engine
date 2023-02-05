import codecs
import json
import os

import networkx as nx

store_file = os.path.dirname(__file__) + '/WithRank.json'


class GenRanks:

    def __init__(self, input_file, input_file2):
        self.data = []
        self.data2 = []
        self.input_file = input_file
        self.input_file2 = input_file2
        self.matrix = None
        self.vertexes = set()
        self.edges = dict()
        self.file = codecs.open(filename=store_file, mode='wb', encoding='utf-8')
        self.PR = None

    def Load_data(self):
        f = open(self.input_file, 'r', encoding='UTF-8')
        for line in f.readlines():
            self.data.append(line.strip().strip(','))
        f.close()
        f = open(self.input_file2, 'r', encoding='UTF-8')
        for line in f.readlines():
            self.data2.append(line.strip().strip(','))
        f.close()

    def GenMatrix(self):
        for d in self.data2:
            d = eval(d)
            self.vertexes.add(d["PostURL"])
        for d in self.data:
            d = eval(d)
            to_ver = d["page_link"]
            self.edges[d["current_url"]] = to_ver
            if len(to_ver) > 0:
                for v in to_ver:
                    if v not in self.vertexes:
                        self.vertexes.add(v)

    def GenRank(self):
        Graph = nx.DiGraph()
        for v in self.vertexes:
            Graph.add_node(v)
        for ver in self.vertexes:
            if ver in self.edges:
                for edge_to in self.edges[ver]:
                    Graph.add_edge(ver, edge_to)
        # nx.draw(Graph, with_labels=True)
        # plt.savefig("./graph.jpg")
        self.PR = nx.pagerank(Graph, max_iter=20000, alpha=0.85)
        return self.PR

    def store(self):
        origin_file = self.input_file2
        f = open(origin_file, 'r', encoding='UTF-8')
        for line in f.readlines():
            cur_j = eval(line.strip().strip(','))
            cur_j["Page_rank"] = self.PR[cur_j["PostURL"]]
            text = json.dumps(cur_j, ensure_ascii=False) + "\n"
            self.file.write(text)
        f.close()


if __name__ == '__main__':
    my_rank = GenRanks("./PageRank.json", "./Info.json")
    my_rank.Load_data()
    my_rank.GenMatrix()
    my_rank.GenRank()
    my_rank.store()
