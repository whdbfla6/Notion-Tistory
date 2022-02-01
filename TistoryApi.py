from NotionApi import Notion
import requests

def tag(word,tag_name,css_dict=None):

    css = ''
    if css_dict:
        for key in css_dict.keys():
            css += f' {key}="{css_dict[key]}"' 

    word = f'<{tag_name} {css}> {word} </{tag_name}>'
    return word

def equation_inline(text):
    
    text = '$' + text + '$'
    return text

def equation_outline(text):

    text = '$$' + text + '$$'
    return text

def font_type(text,type_):

    font_dict = {'bold':'b','italic':'i'}
    if type_ in ['underline','code']:
        return tag(text,'span',{'style':'background-color: #f6e199; color: #000000;'})
    elif type_ in ['bold','italic']:  
        text = tag(text,font_dict[type_])
    else:
        return tag(text,'span',{'style':f'color: {type_}'})

    return text

def Heading(text,num):

    font_size = {'1':'"size26"','2':'"size23"','3':'"size20"','p':'"size16"'}

    tag_name = 'h' + str(num)
    css = font_size[num]
    sentence = tag(text,tag_name,{'data-ke-size':css})

    return sentence

def convertHtml(text,type_,class_=None):

    if type_ == 'equation':
        return equation_inline(text)

    elif type_ == 'bulleted_list_item':
        return tag(text,'li')
    
    elif type_ == 'callout':
        return tag(text,'blockquote',{'data-ke-style':'style3'})

    elif type_ == 'text':
        return text

    elif type_ == 'code':
        text = tag(text,'code')
        return tag(text,'pre',{'class':class_})

    else:
        return tag(text,'p',{'data-ke-style':'size16'})

class Tistory(Notion):

    def __init__(self):

        super().__init__()
        super().tistoryInfo()

        super().getPageId() #self.pageId

    def getHtml(self,block):

        type_ = block['type']

        if type_ == 'divider' :
            sentence = '<hr contenteditable="false" data-ke-type="horizontalRule" data-ke-style="style6" />'

        elif type_ == 'equation' :
            eq = block[type_]['expression']
            sentence = equation_outline(eq)
            sentence = tag(sentence,'p',{'size':'size16'})

        elif type_ in ['heading_1','heading_2','heading_3']:

            block = block[type_]['text']
            hNum = type_[-1:]; sentence = ''

            for i in range(len(block)):
                word = block[i]['plain_text']
                word_type = block[i]['type']
                word = convertHtml(word,word_type)
                annot = block[i]['annotations']
                annotKey = [key for key in annot.keys() if annot[key]==True]
                if annotKey:
                    for a in annotKey:
                        word = font_type(word,a)
                sentence += convertHtml(word,word_type)

            sentence = Heading(sentence,hNum)

        elif type_ == 'code':
            lang = block[type_]['language']
            word = block[type_]['text'][0]['plain_text']
            wordList = word.split('\n'); word = ''
            for w in wordList:
                word += tag(w,'div')
            sentence = convertHtml(word,type_,class_=lang)

        elif type_ == 'image':
            url = block[type_]['file']['url']
            sentence = tag(" ","img",{"src":url,"width":"60%","height":"60%"})
            sentence = tag(sentence,"center")

        else:
            block = block[type_]['text']; status = False
            if type_ == "bulleted_list_item":
                status = True
            if block == []:
                sentence = convertHtml('&nbsp;',type_)
            else:
                sentence = ''
                for i in range(len(block)):
                    word = block[i]['plain_text']
                    word_type = block[i]['type']
                    annot = block[i]['annotations']
                    annotKey = [key for key in annot.keys() if annot[key]==True]
                    if annotKey:
                        for a in annotKey:
                            word = font_type(word,a)
                    if annot['color'] != 'default':
                        word = font_type(word,annot['color'])
                    sentence += convertHtml(word,word_type)
                sentence = convertHtml(sentence,type_)
        
        return sentence

    def notionToHtml(self):

        html = ''
        content = self.getPageContent()
        num = len(content)
        half = len(content)//2

        for i in range(num):
            block = content[i]
            html += self.getHtml(block)
            if i == half:
                print('변환 50% 완료')

        return html

    
    def upload(self):
    
        self.getPageProperty()

        print(f'카테고리: {self.category}')
        print(f'태그: {self.tag}')

        data = {
            'access_token': self.ACCESS_TOKEN,
            'blogName': self.BLOG_NAME,
            'output': 'json',
            'title': self.pageTitle,
            'content': self.notionToHtml(),
            'category' : self.tistoryCategorySearch(self.category),
            'visibility': '0',
            'tag': self.tag
            }

        resp = requests.post(self.UpolodUrl, data=data)
        res = resp.status_code

        if res == 200:
            print('성공적으로 업로드 되었습니다')
        else:
            print('업로드에 실패했습니다')
            print(res)

if __name__ == "__main__":
    tistory = Tistory()
    tistory.upload()
