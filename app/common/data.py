import json
import datetime
from os import listdir
from os.path import isfile, join

def add_path_to_image(data):
    img_police = "static/police.png"
    img_news = "static/news.png"

    category = data[0]["category"]["category"]
    if category == "Polishändelse":
        img_path = img_police
        classCss = "police"
    else:
        img_path = img_news
        classCss = "news"

    for entry in data:
        entry["path_image"] = img_path
        entry["classCss"] = classCss
    

def get_entries():
    path_json_files_directory = "../data/processed"
    path_json_files = [f for f in listdir(path_json_files_directory) if isfile(join(path_json_files_directory, f))]
    path_json_files = [ join(path_json_files_directory, path) for path in path_json_files]
    combinedData = []
    for path_json_file in path_json_files:
        with open(path_json_file) as json_file:
            data = json.load(json_file)
            add_pretty_date(data)
            add_path_to_image(data)
            combinedData += data
    
    sortedData = sort_dates_descending(combinedData)

    return sortedData

def sort_dates_descending(data):
    sorted_data = sorted(data, key=lambda entry: datetime.datetime.strptime(entry['datetime_pretty'],  '%b %d %H:%M'), reverse=True) 
    return sorted_data

def add_pretty_date(data):
     for entry in data:
        date_time_str = entry["datetime"]
        if isinstance(date_time_str, str) == False:
            date_time_str = entry["datetime"]["datetime"]

        print(date_time_str)
        if "+" in date_time_str and "T" in date_time_str:
            date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S%z')
        elif "+" in date_time_str:
            date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S %z')
        else:
            date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%SZ')
        date_time_obj_pretty = date_time_obj.strftime('%b %d %H:%M')
        entry["datetime_pretty"] = date_time_obj_pretty