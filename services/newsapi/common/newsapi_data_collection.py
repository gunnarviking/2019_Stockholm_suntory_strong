import requests
import json
import os

def make_request():
    #connect(cfg.mysql['host'], cfg.mysql['user'], cfg.mysql['password'])
    print("collecting  data")

    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, 'config/config.json')
    endpoint = ""
    apiKey = ""
    with open(filename) as json_file:
        data = json.load(json_file)
        print(data)
        endpoint = data["url_endpoint"]
        print("endpoint " + endpoint)
        apiKey = data["api_key"]
        print("apiikey: " + apiKey)
    # response = requests.get('https://newsapi.org/v2/top-headlines?country=se&apiKey=49bdf4bfba684bea8bac0eeacb3c15ea')
    data = {"country": "se", "apiKey": apiKey}
    response = requests.get(endpoint,params=data)
    if response.status_code == 200:
        print('Success!')
        return response.content
    elif response.status_code == 404:
        print('Not Found.')
        print(response)



def init():
    print("collect data")
    content = make_request()
    return content
