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
