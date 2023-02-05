FILE_PATH = "../WorkSpiders/WorkSpiderWork.json"
f = open(FILE_PATH, 'r', encoding='UTF-8')
data = []
for d in f.readlines():
    data.append(d.strip('\n').strip(','))
for each_info in data:
    print(each_info)