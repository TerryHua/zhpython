#!/usr/bin/python3
#coding=utf-8

import pymysql

class mysqlClass:
    dbconnect = '';

    def __init__(self, host, user, pwd, dbname, port=3306):
        self.dbconnect = pymysql.connect(host, user, pwd, dbname, port, '','utf8')


    def query(self, sql):
        cursor = self.dbconnect.cursor()
        # 使用 execute() 方法执行 SQL，如果表存在则删除
        cursor.execute(sql)
        # 使用预处理语句创建表


    def getAll(self,table, where):
        # 使用cursor()方法获取操作游标
        cursor = self.dbconnect.cursor()
        # SQL 查询语句
        sql = "SELECT * FROM " + table + where
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            return results
        except:
            print ("Error: unable to fecth data")

    def getRow(self, table, where):
        # 使用cursor()方法获取操作游标
        cursor = self.dbconnect.cursor()
        # SQL 查询语句
        sql = "SELECT * FROM " + table + where
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchone()
            self.dbconnect.commit()
            return results
        except:
            print ("Error: unable to fecth data")

    def deleteRow(self, table, where):
        # 使用cursor()方法获取操作游标
        cursor = self.dbconnect.cursor()

        # SQL 删除语句
        sql = "DELETE FROM "+ table + where

        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 提交修改
            self.dbconnect.commit()
        except:
            # 发生错误时回滚
            self.dbconnect.rollback()

    # 更新数据库记录
    def updateRow(self, table, where, data):
        # 使用cursor()方法获取操作游标
        cursor = self.dbconnect.cursor()
        # SQL 更新语句
        sql = "UPDATE " + table + data + where
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 提交到数据库执行
            self.dbconnect.commit()
        except:
            # 发生错误时回滚
            self.dbconnect.rollback()

    def insertRow(self, table, value):
        # 插入单条数据库记录
        # 使用cursor()方法获取操作游标
        cursor = self.dbconnect.cursor()

        # SQL 插入语句
        sql = "INSERT INTO " + table + value;

        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            self.dbconnect.commit()
        except:
            # 如果发生错误则回滚
            self.dbconnect.rollback()

    def __del__(self):
        self.dbconnect.close()


