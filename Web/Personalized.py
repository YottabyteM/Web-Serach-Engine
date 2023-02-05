from Cluster import predict

HISTORY_PATH = "./logs.txt"


class Personalized_Search:

    def __init__(self):
        fp = open(HISTORY_PATH, 'r', encoding='UTF-8')
        self.History = ""
        for line in fp.readlines():
            self.History += line.strip()
            self.History += " "
        fp.close()

    def get_cluster(self):
        return predict(self.History)

    def new_res(self, origin, k):
        search_contents = origin['hits']['hits']
        cluster = self.get_cluster()
        res = []
        i = 0
        for s_c in search_contents:
            if i < k:
                if s_c['_source']['Cluster'] == str(cluster):
                    res.append(s_c)
                    search_contents.remove(s_c)
            else:
                break
            i += 1
        for s_c in search_contents:
            res.append(s_c)
        return res


class Personalized_Recommend:

    def __init__(self):
        fp = open(HISTORY_PATH, 'r', encoding='UTF-8')
        self.History = ""
        for line in fp.readlines():
            self.History += line.strip()
            self.History += " "
        fp.close()

    def get_cluster(self):
        return predict(self.History)
