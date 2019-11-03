from common import newsapi_data_collection
from common import newsapi_data_handeling
import json
import os
import csv

class keywords:
    def __init__(self, word, count):
        self.keyword = word
        self.hits = count
    def to_dict(self):
      return {"keyword": self.keyword, "hits": self.hits}

def experimenting(text):
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, '../../data/configuration/positive_keywords.csv')

    keyword_list = []
    totalWords = 0
    with open(filename, 'r') as csvFile:
        reader = csv.reader(csvFile, delimiter=',')
        for row in reader:
            for col in row:
                counter = text.lower().count(col)
                if counter > 0:
                    totalWords += counter
                    keyword_list.append(keywords (col,totalWords))
    csvFile.close()
    for keyWord in keyword_list:
        print(keyWord.keyword)

    results = [obj.to_dict() for obj in keyword_list]
    jsdata = json.dumps({"results": results})
    print(jsdata)


def main():
    datasource = newsapi_data_collection.init()
    newsapi_data_handeling.init(datasource)

if __name__ == '__main__':
    main()
