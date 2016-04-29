'''
知乎日报内容获取
'''
#coding=UTF-8
import urllib.request
import urllib.parse
import json
import re
import time
import os, sys


class zhihuDailyReport:
    dailyUrl = "http://news.at.zhihu.com/api/1.2/news/latest"

    def __init__(self):
        self.userAgent = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.69 Safari/537.36'}
        self.requestUrl = 'http://translate.google.com.hk/translate_a/t'
        self.requestMethod = 'GET'

    def getDailyList(self):
        '''获取知乎日报接口列表记录'''
        values = {}
        data = urllib.parse.urlencode(values).encode('UTF-8')
        req = urllib.request.Request(self.dailyUrl, data=data, headers=self.userAgent, method=self.requestMethod)
        response = urllib.request.urlopen(req)
        html = response.read().decode("UTF-8")

        list = json.loads(html)
        print(list['date'])
        # 创建的目录
        path = "./"+time.strftime("%Y%m%d", time.localtime())
        if (os.path.exists(path) == False): #判断文件夹是否存在
            os.mkdir( path, 0o755 );


        for row in list['news']:
            print(row['url'])
            content = self.getDailyDetail(row['url'])
            jsonContent = json.loads(content)

            f = open(path + '/'+row['title']+'.txt', "w", encoding='utf-8')
            f.write(jsonContent['body'])
            f.close();

        return html



    def getDailyDetail(self, detailUrl):
        values = {}
        data = urllib.parse.urlencode(values).encode('UTF-8')
        request = urllib.request.Request(url = detailUrl, data = data, headers = self.userAgent, method = self.requestMethod)
        textDestination = urllib.request.urlopen(request).read().decode('UTF-8');

        return textDestination



if __name__ == '__main__':
    s = zhihuDailyReport()
    html = s.getDailyList()



