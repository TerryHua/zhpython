#!/usr/bin/python3
#coding=UTF-8
#从数据库中导出html制作成epub格式

import mysqlClass


class exportHtml:
    topicsTitle = ''
    topicTitle = ''

    def __init__(self, topicsId):
        self.topicsId = topicsId
        self.mysqlObj = mysqlClass.mysqlClass('localhost', 'root', '', 'zhihu')

    def getTopic(self):
        table = 'zhihu_topics'
        where = " WHERE parent_topic_id= %s" % (self.topicsId)
        rows = self.mysqlObj.getAll(table, where)
        for row in rows:
            print(row[1])
            self.getQuestionByTopic(row[1])
            break

    def getQuestionByTopic(self, topicId):
        table = 'zhihu_question'
        where = " WHERE topic_id='%s'" % (topicId)
        question = self.mysqlObj.getAll(table, where)
        if question:
            for quesrow in question:
                quesId = quesrow[1]  #知乎问题Id
                quesTitle = quesrow[2]  #问题标题




if __name__ == '__main__':
    exObj = exportHtml('388')
    exObj.getTopic()
