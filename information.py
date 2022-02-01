import requests
import json

class Information:

    def __init__(self):
        with open('info.json', 'r') as f:
            self.info = json.load(f)

    def tistoryInfo(self):

        self.url = self.info["tistory"]["URL"]
        self.UpolodUrl  = self.url + "post/write"
        self.CategoryUrl = self.url + "category/list?"

        self.ACCESS_TOKEN = self.info["tistory"]["ACCESS_TOKEN"]
        self.BLOG_NAME = self.info["tistory"]["BLOG_NAME"]

        return self

    def tistoryCategory(self):

        self.tistoryInfo()

        category = dict()
        params = {
                'access_token' : self.ACCESS_TOKEN,
                'output': 'json',
                'blogName' : self.BLOG_NAME
                 }   

        res = requests.get(self.CategoryUrl,params=params)
        res = res.json()
        catInfo = res['tistory']['item']['categories']

        for i in range(len(catInfo)):
            category[catInfo[i]['label']] = catInfo[i]['id']

        return category

    def tistoryCategorySearch(self,category_name):

        id_ = self.tistoryCategory()[category_name]
        return id_

    def notionInfo(self):

        self.URL = self.info["notion"]["URL"]
        self.TOKEN = self.info["notion"]["TOKEN"]
        self.DatabaseDict = self.info["notion"]["DATABASE"]

        return self
