import json
import re
import os
import csv
import datetime
from flashtext import KeywordProcessor

def loadfiles():
    print("loadfiles")

    dir = os.path.dirname(__file__)
    filedir = os.path.join(dir, '../../../data/')
    filelist = []
    for file in os.listdir(filedir):
        if file.endswith(".txt"):
            print(os.path.join(filedir, file))
            filelist.append(os.path.join(filedir, file))
        if file.endswith(".json"):
            print(os.path.join(filedir, file))
            filelist.append(os.path.join(filedir, file))


    print("filelist len:",len(filelist) )
    if(len(filelist) > 0):
        return filelist
    return None

def init():
    print("init")
    filelist = loadfiles()
    if(filelist is not None):
        return filelist
    print("No files found")
