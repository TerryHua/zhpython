#!/usr/bin/python3
#coding=UTF-8
#从数据库中导出html制作成epub格式

import mysqlClass
import html
import os, sys

class exportHtml:
    htmlTitle = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>Untitled Document</title>
<style>img { width:100% }</style>
</head>
"""
    htmlBottom = """<body></body></html>"""
    htmlText = ''
    topicsTitle = ''
    topicTitle = ''

    def __init__(self, topicsId):
        self.topicsId = topicsId
        self.mysqlObj = mysqlClass.mysqlClass('localhost', 'root', 'root', 'zhihu')

    def getTopic(self):
        table = 'zhihu_topics'
        where = " WHERE parent_topic_id= %s" % (self.topicsId)
        rows = self.mysqlObj.getAll(table, where)
        if rows:
            self.htmlText = self.htmlTitle
            # 创建的目录 根据大的topics
            self.htmlPath = "./html"
            if (os.path.exists(self.htmlPath) == False):  # 判断文件夹是否存在
                os.mkdir(self.htmlPath, 0o755);

            for row in rows:
                print(row[1])
                hasQuestion = self.getQuestionByTopic(row[1])
                if hasQuestion == True:
                    self.htmlText = self.htmlText + '<h1>' + row[3] + ' ' + row[4] + '</h1>'


            self.htmlText = self.htmlText + self.htmlBottom
            f = open(self.htmlPath + '/' + self.topicsId + '.html', "w", encoding='utf-8')
            f.write(self.htmlText)
            f.close();

    def getQuestionByTopic(self, topicId):
        table = 'zhihu_question'
        where = " WHERE topic_id='%s'" % (topicId)
        question = self.mysqlObj.getAll(table, where)
        hasQuestion = False
        if question:
            for quesrow in question:
                quesId = quesrow[1]  #知乎问题Id
                quesTitle = quesrow[2]  #问题标题
                answerCount = quesrow[3] #回答问题数量
                hasQuestion = True
                self.htmlText = self.htmlText + '<h2>' + quesTitle + ' 回答数(' + str(answerCount)+ ')</h2>'


                table = 'zhihu_answer'
                where = " WHERE question_id='%s'" % (quesId)
                answerList = self.mysqlObj.getAll(table, where)
                if answerList:
                    for answer in answerList:
                        voteCount = answer[3]
                        commentNum = answer[4]
                        content = answer[5]
                        self.htmlText = self.htmlText + '答案点赞数(' + str(voteCount) + ') 评论数(' + str(commentNum) + ')<br />'
                        self.htmlText = self.htmlText + html.unescape(content) + '<br /><br />'
        return hasQuestion










if __name__ == '__main__':
    exObj = exportHtml('253')
    exObj.getTopic()
