import requests
import json
from information import Information


class Notion(Information):

    def __init__(self,title='Study List'):

        self.DatabaseTitle = title

        super().__init__()
        super().notionInfo()

        self.DATABASE = None
        self.error = None
        self.pageId = None
        self.page = None

    def readDatabase(self): # info.json에서 특정 데이터베이스 정보 가져오기

        self.DatabaseId = self.DatabaseDict[self.DatabaseTitle]["id"]

        headers = {
                "Authorization": "Bearer " + self.TOKEN,
                "Content-Type": "application/json",
                "Notion-Version": "2021-05-13"
                }

        url = self.URL + "databases/" + self.DatabaseId + "/query"
        res = requests.request("POST", url, headers=headers)

        self.DATABASE = res.json()["results"]


    def Update(self): #info.json에 게시글 정보 업데이트(글 제목,id)

        if self.DATABASE == None : self.readDatabase()
        self.DatabasePage = self.DatabaseDict[self.DatabaseTitle]["page"]

        for i in range(len(self.DATABASE)):

            pageTitle = self.DATABASE[i]['properties']['TITLE']['title'][0]['plain_text']
            pageId = self.DATABASE[i]['id']

            try:
                self.DatabasePage[pageTitle]
            except:
                self.DatabasePage.update({pageTitle:pageId})

        with open('info.json', 'w', encoding='utf-8') as file:
            json.dump(self.info, file, ensure_ascii=False, indent="\t")

    def getPage(self): #info.json에서 데이터베이스 페이지(게시글) 정보 가져오기

        if self.DATABASE == None : self.readDatabase()
        self.DatabasePage = self.DatabaseDict[self.DatabaseTitle]["page"]

        return self


    def getPageId(self): #info.json에서 page ID 불러오기

        self.pageTitle = input('페이지 제목을 입력하시오 : ')
        self.getPage()

        print(f'페이지의 ID를 검색하는 중입니다')

        try:
            self.pageId = self.DatabasePage[self.pageTitle]
            print(f'"{self.pageTitle}" 페이지의 Id는 "{self.pageId}" 입니다')
        except:
            print('페이지를 찾을 수 없어 업데이트 하는 중입니다')
            self.Update() 
            try:
                self.getPage()
                self.pageId = self.DatabasePage[self.pageTitle]
                print(f'{self.pageTitle}의 Id는 {self.pageId}입니다')
            except:
                self.error = f'{self.pageTitle} 페이지를 찾을 수 없습니다'
                print(self.error)


    def getPageProperty(self):

        if self.pageId == None : self.getPageId()
        if self.error != None : return

        url = f"https://api.notion.com/v1/pages/{self.pageId}"
        headers = {
                    "Authorization": "Bearer " + self.TOKEN,
                    "Notion-Version": "2021-08-16"
                  }
        res = requests.request('get', url, headers=headers)
        page = res.json()

        type_ = page['properties']['카테고리']['type']
        self.category = page['properties']['카테고리'][type_]['name'][1:-1]

        tag = [i['name'] for i in page['properties']['태그']['multi_select']]
        self.tag = ','.join(tag)

        return self

    def getPageContent(self):

        if self.pageId == None : self.getPageId()
        if self.error != None : return

        url = f"https://api.notion.com/v1/blocks/{self.pageId}/children"

        headers = {
                    "Authorization": "Bearer " + self.TOKEN,
                    "Notion-Version": "2021-08-16"
                  }
        res = requests.request('get', url, headers=headers)
        content = res.json()['results']

        return content