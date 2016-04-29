'''
知乎所有话题获取
'''
#coding=UTF-8
import urllib.request
import urllib.parse
import json
import re

class ZhihuTopic:
    topUrl = "https://www.zhihu.com/topics"

    def __init__(self):
        self.userAgent = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.69 Safari/537.36'}
        self.requestUrl = 'http://translate.google.com.hk/translate_a/t'
        self.requestMethod = 'POST'

    def getTopContent(self):
        '''
        request = urllib.Request(self.topUrl)
        response = urllib.urlopen(request)
        html = response.read()
        response.close()
        '''
        req = urllib.request.Request(self.topUrl)
        response = urllib.request.urlopen(req)
        html = response.read()
        return html

    def getTopSign(self, html):
        html = html.decode('UTF-8')
        searchObj = re.search(r'zg-icon-topic-square(.*)zm-topic-cat-sub', html, re.M|re.I|re.S)
        if searchObj:
            hrefHtml = searchObj.group();
            urls = re.findall(r'<a.*?href="(.*?)">.*?<\/a>',hrefHtml,re.I)
            for i in urls:
                print(i)
            else:
                print ('this is over')
        else:
           print ("Nothing found!!")

    def test11(self):
        print('hello world')


    def getTopList(self, topicId):
        url = "https://www.zhihu.com/node/TopicsPlazzaListV2"
        values = {'method':'next','params': '{"topic_id":253,"offset":0,"hash_id":""}','_xsrf':'337756f889b88582050596b81da0d0a1'}

        data = urllib.parse.urlencode(values).encode('UTF-8')
        request = urllib.request.Request(url = url, data = data, headers = self.userAgent, method = self.requestMethod)

        textDestination = urllib.request.urlopen(request).read().decode('utf-8');
        print(textDestination)



s = ZhihuTopic()
html = s.getTopList(253)
#print(s.getTopSign(html));
print(html)



