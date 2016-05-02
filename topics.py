#coding=utf-8

'''
知乎所有话题获取
'''
#coding=UTF-8
import urllib.request
import urllib.parse
import json
import re
import html
import mysqlClass
import time
import pymysql


class zhihuTopic:

    def __init__(self, topUrl):
        self.userAgent = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.69 Safari/537.36'}
        self.requestUrl = 'http://www.baidu.com'
        self.requestMethod = 'POST'

        self.mysqlObj = mysqlClass.mysqlClass('localhost', 'root', 'root', 'zhihu')
        self.topUrl = topUrl

    def getTopContent(self):
        #获取知乎话题广场的html
        req = urllib.request.Request(self.topUrl)
        response = urllib.request.urlopen(req)
        htmlText = response.read()
        return htmlText

    def getTopSign(self, htmlText):
        #获取所有的话题广场的所有话题(科技,运动,创业等)
        htmlText = htmlText.decode('UTF-8')
        searchObj = re.search(r'zg-icon-topic-square(.*)zm-topic-cat-sub', htmlText, re.M|re.I|re.S)
        if searchObj:
            hrefHtml = searchObj.group();
            urls = re.findall(r'<a.*?href="(.*?)">.*?<\/a>',hrefHtml,re.I)
            topicId = re.findall(r'<li class=\"zm-topic-cat-item\" data-id=\"(.*?)\">', hrefHtml, re.I)
            for id in topicId:
                print (id);

            """for i in urls:
                print(i)
            else:
                print ('this is over')
            """
        else:
           print ("Nothing found!!")

    def getTopList(self, topicId):
        url = "https://www.zhihu.com/node/TopicsPlazzaListV2"
        values = {'method':'next','params': '{"topic_id":'+ topicId+ ',"offset":0,"hash_id":""}','_xsrf':'337756f889b88582050596b81da0d0a1'}

        data = urllib.parse.urlencode(values).encode('UTF-8')
        request = urllib.request.Request(url = url, data = data, headers = self.userAgent, method = self.requestMethod)

        textDestination = urllib.request.urlopen(request).read().decode('utf-8');
        print(textDestination)


    def getTopSignList(self, htmlText, topicTitle):
        #通过ajax获取话题内的标签
        htmlText = htmlText.decode('UTF-8')
        xsrf = re.findall(r'name=\"_xsrf\" value=\"(.*)\"',htmlText,re.I)
        #获取请求参数
        param = re.findall(r'class=\"zh-general-list clearfix\" data-init=\"(.*)\">',htmlText,re.I)
        paramText =  html.unescape(param[0])

        paramDict = json.loads(paramText)

        #获取当前页面的topicId
        topicInfo = re.findall(r'<li class="zm-topic-cat-item" data-id="(.*?)"><a href="#'+topicTitle+'">'+topicTitle+'</a></li>', htmlText, re.I)

        topicId = topicInfo[0]


        for i in range(0, 10000, 20):

            #url组装
            url = "https://www.zhihu.com/node/"+paramDict['nodename']
            values = {'method':'next','params': '{"topic_id":'+ str(topicId) + ',"offset":'+str(i)+',"hash_id":"'+str(paramDict['params']['hash_id'])+'"}','_xsrf':xsrf[0]}

            data = urllib.parse.urlencode(values).encode('UTF-8')
            request = urllib.request.Request(url = url, data = data, headers = self.userAgent, method = self.requestMethod)

            textDestination = urllib.request.urlopen(request).read().decode('utf-8');
            textDestinationDict = json.loads(textDestination)
            if textDestinationDict['msg']:
                for textRow in textDestinationDict['msg']:
                    urlLink = self.getSignLink (textRow)
                    for page in range(1, 50):
                        self.getTopicTopAnswers(urlLink, topicTitle, topicId, page)





    def getSignLink(self, htmlText):
        #获取单个话题的链接地址
        link = re.findall(r'<a target=\"_blank\" href=\"(.*)\">',htmlText,re.I)

        urlLink = "https://www.zhihu.com"+link[0]+'/top-answers'

        return urlLink


    def getTopicTopAnswers(self, urlLink, topicTitle='', topicId='1', page='1'):
        #获取话题的精华题目和答案
        print (urlLink)
        urlLink = urlLink+'?page='+str(page)
        req = urllib.request.Request(urlLink)
        response = urllib.request.urlopen(req)
        htmlText2 = response.read().decode('UTF-8')
        contentText = re.findall(r'<div class=\"feed-item feed-item-hook folding(.*?)<button class=\"meta-item item-collapse js-collapse\">', htmlText2, re.I|re.M|re.S)
        topicFollwer = re.findall(r'<strong>(.*?)<\/strong>(.*?)人关注了该话题', htmlText2, re.I);
        topicName = re.findall(r'<h1 class=\"zm-editable-content\"(.*?)>(.*?)<\/h1>', htmlText2, re.I)



        #将话题插入到话题数据库
        mysqlObj1 = mysqlClass.mysqlClass('localhost', 'root', 'root', 'zhihu')
        table = 'zhihu_topics'
        addTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        valueStr = " (`topic_id`, `topic`, `topic_tag`, `follwer_user`,  `add_time` ) VALUES " \
                   " ('" + topicId + "','" + topicTitle + "','" + topicName[0][1] + "','" + topicFollwer[0][0] + "', '" + addTime + "')"
        mysqlObj1.insertRow(table, valueStr)

        if contentText:
            for signText in contentText:
                self.getAnswerContent(signText, topicId)
                break;




    def getAnswerContent(self, htmlText, topicId='0'):

        #获取回答内容里面的问题相关信息
        answerContent = re.findall(r'<textarea hidden class=\"content\">(.*)<\/textarea>', htmlText, re.M|re.S)  #回答内容

        #赞同数量
        voteCount = re.findall(r'data-votecount=\"(.*?)\">', htmlText, re.I);

        #评论数
        comment = re.findall(r'<i class=\"z-icon-comment\"><\/i>(.*)<\/a>', htmlText, re.I);
        commentCount = comment[0].replace('条评论', '').replace(' ','')

        #问题的回答总数
        answerCount = re.findall(r'<meta itemprop=\"answerCount\" content=\"(.*?)\" \/>', htmlText, re.I)

        #问题的标题
        questionText = re.findall(r'<a class=\"question_link\" target=\"_blank\" href=\"(.*)\">(.*)<\/a>', htmlText, re.I|re.M)
        questionTitle = questionText[0][1];

        #问题的ID
        questionId = questionText[0][0].replace('/question/', '')

        #知乎的问题写入到mysql
        table = 'zhihu_question'
        addTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        valueStr = " (`question_id`, `question_title`, `answer_count`, `add_time`, `topic_id` ) VALUES " \
                   " ('" + questionId + "','" + questionTitle + "','" + answerCount[0] + "','" + addTime + "','" + topicId + "')"
        self.mysqlObj.insertRow(table, valueStr)


        #回答的ID
        answerText = re.findall(r'<meta itemprop=\"answer-url-token\" content=\"(.*)\">', htmlText, re.I)
        answerId = answerText[0]



        #插入答案到数据库
        table = 'zhihu_answer'
        addTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        valueStr = " (`answer_id`, `question_id`, `vote_count`, `comment_num`, `content`, `add_time` ) VALUES " \
                   " ('"+ answerId + "','" + questionId + "','" + voteCount[0] + "','"
        valueStr = valueStr + commentCount + "','" + pymysql.escape_string(answerContent[0]) + "','" + addTime + "')"
        self.mysqlObj.insertRow(table, valueStr )

        #插入问题到数据库




s = zhihuTopic('https://www.zhihu.com/topics#创业')
htmlText = s.getTopContent()
print(s.getTopSignList(htmlText, '创业'));




