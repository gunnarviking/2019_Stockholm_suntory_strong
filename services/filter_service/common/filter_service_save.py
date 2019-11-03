import os
import datetime
import json

def save(json_object, counter):
    print("save")
    time = datetime.datetime.now()
    dir = os.path.dirname(__file__)
    # filename = os.path.join(dir, '../../../data/processed/'+ time.strftime("%Y-%m-%d%-H%-M-%-S") + '_source.txt')
    filename = os.path.join(dir, '../../../data/processed/'+ str(counter) + '_source.txt')
    print("filename:", filename)
    with open(filename, 'w') as outfile:
        json.dump(json_object, outfile,ensure_ascii=False)

def init(json_object, counter):
    save(json_object, counter)
