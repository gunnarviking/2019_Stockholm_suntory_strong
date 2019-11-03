import json
import re
import os
import csv
import datetime
from flashtext import KeywordProcessor
from common import filter_service_class


def check_positive(data):
    keyword_list = []

    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, '../../../data/configuration/positive_keywords.csv')
    keyword_processor = KeywordProcessor()
    totalWords = 0
    data_copy = str(data)
    with open(filename, 'r') as csvFile:
        reader = csv.reader(csvFile, delimiter=',')
        for row in reader:
            keyword_processor.add_keywords_from_list(row)
            key_proc_title = keyword_processor.extract_keywords(data_copy.lower())
            len_title = len(key_proc_title)
            if len_title > 0:
                totalWords += len_title
            break

    if totalWords > 0:
        return totalWords
    return None

def check_negative(data):
    negative_keywords = []
    keyword_processor = KeywordProcessor()
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, '../../../data/configuration/negative_keywords.csv')
    data_copy = str(data)
    with open(filename, 'r') as csvFile:
        reader = csv.reader(csvFile, delimiter=',')
        for row in reader:
            keyword_processor.add_keywords_from_list(row)
            key_proc_title = keyword_processor.extract_keywords(data_copy.lower())
            len_title = len(key_proc_title)
            if len_title > 0:
                return None
            break

    return "Succcess"

def analyze_json(data):
    filtered_items = []
    for item in data:
        print("item", item["information"]["title"])
        negative = check_negative(item)
        if negative is None:
            print("negative words found")
            continue
        postive = check_positive(item)
        if postive is not None:
            print("positiv words found")
            filtered_items.append(item)
    if len(filtered_items) > 0:
        return filtered_items
    return None

def loadfile(file):
    data = None
    with open(file) as json_file:
        data = json.load(json_file)

    return data

def init(file):
    print("init")
    data = loadfile(file)
    filtered = analyze_json(data)
    if filtered is not None:
        return filtered
    return None
