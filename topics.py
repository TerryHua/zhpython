'''
知乎所有话题获取
'''
#coding=UTF-8
import urllib.request
import urllib.parse
import json
import re
import html


class ZhihuTopic:
    topUrl = "https://www.zhihu.com/topics"

    def __init__(self):
        self.userAgent = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.69 Safari/537.36'}
        self.requestUrl = 'http://www.baidu.com'
        self.requestMethod = 'POST'

    def getTopContent(self):
        req = urllib.request.Request(self.topUrl)
        response = urllib.request.urlopen(req)
        htmlText = response.read()
        return htmlText

    def getTopSign(self, htmlText):
        htmlText = htmlText.decode('UTF-8')
        searchObj = re.search(r'zg-icon-topic-square(.*)zm-topic-cat-sub', htmlText, re.M|re.I|re.S)
        if searchObj:
            hrefHtml = searchObj.group();
            urls = re.findall(r'<a.*?href="(.*?)">.*?<\/a>',hrefHtml,re.I)
            for i in urls:
                print(i)
            else:
                print ('this is over')
        else:
           print ("Nothing found!!")

    def getTopList(self, topicId):
        url = "https://www.zhihu.com/node/TopicsPlazzaListV2"
        values = {'method':'next','params': '{"topic_id":253,"offset":0,"hash_id":""}','_xsrf':'337756f889b88582050596b81da0d0a1'}

        data = urllib.parse.urlencode(values).encode('UTF-8')
        request = urllib.request.Request(url = url, data = data, headers = self.userAgent, method = self.requestMethod)

        textDestination = urllib.request.urlopen(request).read().decode('utf-8');
        print(textDestination)


    def getTopSignList(self, htmlText):
        #通过ajax获取话题内的标签
        htmlText = htmlText.decode('UTF-8')
        offSet = '0'
        xsrf = re.findall(r'name=\"_xsrf\" value=\"(.*)\"',htmlText,re.I)
        #获取请求参数
        param = re.findall(r'class=\"zh-general-list clearfix\" data-init=\"(.*)\">',htmlText,re.I)
        paramText =  html.unescape(param[0])

        paramDict = json.loads(paramText)

        #url组装
        url = "https://www.zhihu.com/node/"+paramDict['nodename']
        values = {'method':'next','params': '{"topic_id":'+ str(paramDict['params']['topic_id']) + ',"offset":'+offSet+',"hash_id":"'+str(paramDict['params']['hash_id'])+'"}','_xsrf':xsrf[0]}

        data = urllib.parse.urlencode(values).encode('UTF-8')
        request = urllib.request.Request(url = url, data = data, headers = self.userAgent, method = self.requestMethod)

        textDestination = urllib.request.urlopen(request).read().decode('utf-8');
        textDestinationDict = json.loads(textDestination)
        if textDestinationDict['msg']:
            for textRow in textDestinationDict['msg']:
                print (textRow)

    def getSignLink(self, htmlText):
        #获取单个话题的链接地址
        link = re.findall(r'<a target=\"_blank\" href=\"(.*)\">',htmlText,re.I)
        url = "https://www.zhihu.com/node/"+link[0]


s = ZhihuTopic()
htmlText = s.getTopContent()
print(s.getTopSignList(htmlText));




