import json
import re
import os
import csv
import datetime
from flashtext import KeywordProcessor


# import pandas as pd

class information(object):
    def __init__(self, title,text,imgUrl,orignalSource,location):
        self.title = title
        self.text = text
        self.imgUrl = imgUrl
        self.orignalSource = orignalSource
        self.location = location
    def to_dict(self):
      return {"title": self.title, "text": self.text, "imgUrl": self.imgUrl, "orignalSource": self.orignalSource, "location":self.location}
class keywords(object):
    def __init__(self,keyWord,hits):
        self.keyWord = keyWord
        self.hits = hits
    def to_dict(self):
      return {"keyWord": self.keyWord, "hits": self.hits}
class category(object):
    def __init__(self, category ,tag):
        self.tag = tag
        self.category = category
    def to_dict(self):
      return {"tag": self.tag, "category": self.category}

class datetimeClass(object):
    """docstring for datetime."""
    def __init__(self, datestamp):
        self.datestamp = datestamp
    def to_dict(self):
      return {"datetime": self.datestamp}

def save_data(data):
    time = datetime.datetime.now()
    print("time")
    print(time)
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, '../../../data/'+ time.strftime("%Y-%m-%d %-H%-M-%-S %z") + '_newsapi.txt')
    with open(filename, 'w') as outfile:
        json.dump(data, outfile,ensure_ascii=False)

def format_data(article, keyword_list):
    jsondata = {}

    information_holder = information(article['title'],article['content'],article['urlToImage'],article['url'],"not set")
    category_holder = category(article['source']['name'],"Nyheter")

    information_obj = information_holder.to_dict()
    keywords_obj = [obj.to_dict() for obj in keyword_list]
    category_obj = category_holder.to_dict()

    jsondata['information'] = information_obj
    jsondata['keyWords'] = keywords_obj
    jsondata['category'] = category_obj
    jsondata['datetime'] = article['publishedAt']

    return jsondata

def find_unrelated(title,content):
    if content is None:
        return "Success"
    negative_keywords = []
    keyword_processor = KeywordProcessor()
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, '../../../data/configuration/negative_keywords.csv')
    with open(filename, 'r') as csvFile:
        reader = csv.reader(csvFile, delimiter=',')
        for row in reader:
            keyword_processor.add_keywords_from_list(row)
            key_proc_title = keyword_processor.extract_keywords(title.lower())
            len_title = len(key_proc_title)
            if len_title > 0:
                return None

            key_proc_content = keyword_processor.extract_keywords(content.replace("[","").replace("]","").replace("chars", "").lower())
            len_content = len(key_proc_content)
            if len_content > 0:
                return None
            break

    return "Succcess"

def find_keywords(title,content):
    locations = find_unrelated(title,content)
    if locations is None:
        print("Not Related")
        return None

    keyword_list = []

    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, '../../../data/configuration/positive_keywords.csv')
    keyword_processor = KeywordProcessor()
    keyword_list = []
    totalWords = 0
    with open(filename, 'r') as csvFile:
        reader = csv.reader(csvFile, delimiter=',')
        for row in reader:
            keyword_processor.add_keywords_from_list(row)
            key_proc_title = keyword_processor.extract_keywords(title.lower())
            len_title = len(key_proc_title)
            if len_title > 0:
                keyword_list.append(keywords (key_proc_title,len_title +1))
            key_proc_content = keyword_processor.extract_keywords(content.replace("[","").replace("]","").replace("chars", "").lower())
            len_content = len(key_proc_content)
            if len_content > 0:
                keyword_list.append(keywords (key_proc_title,len_content +1))
            break

    csvFile.close()

    if len(keyword_list) > 0:
        return keyword_list
    elif len(keyword_list) == 0:
        return None


def iterate_articles(article):
    title = ""
    content = ""
    if article["title"] is not None:
        title = article["title"]
    if article["content"] is not None:
        content = article["content"]

    keywords = find_keywords(title,content)
    if keywords is not None:
        content = format_data(article,keywords)
        return content
    return None


def find_articles(datasource):
    test = json.loads(datasource)
    results = test["articles"]
    return results

def init(datasource):
    formated_list = []
    articles = find_articles(datasource)
    for article in articles:
        formated_content = iterate_articles(article)
        if formated_content is not None:
            formated_list.append(formated_content)

    if(len(formated_list) > 0):
        save_data(formated_list)
    elif len(formated_list) == 0:
        print("no articles found")
