#!/usr/bin/python3

import pymysql

def test():
    # 打开数据库连接
    db = pymysql.connect("localhost","root","","test" )

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # 使用 execute()  方法执行 SQL 查询
    cursor.execute("SELECT VERSION()")

    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchone()

    print ("Database version : %s " % data)

    # 关闭数据库连接
    db.close()

def createTable():
    # 打开数据库连接
    db = pymysql.connect("localhost","root","","test" )
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute() 方法执行 SQL，如果表存在则删除
    cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
    # 使用预处理语句创建表
    sql = """CREATE TABLE EMPLOYEE (
             FIRST_NAME  CHAR(20) NOT NULL,
             LAST_NAME  CHAR(20),
             AGE INT,
             SEX CHAR(1),
             INCOME FLOAT )"""
    cursor.execute(sql)
    # 关闭数据库连接
    db.close()

def insertRow():
    #插入单条数据库记录
    # 打开数据库连接
    db = pymysql.connect("localhost","root","","test" )
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 插入语句
    sql = """INSERT INTO EMPLOYEE(FIRST_NAME,
             LAST_NAME, AGE, SEX, INCOME)
             VALUES ('Mac', 'Mohan', 20, 'M', 2000)"""
    try:
       # 执行sql语句
       cursor.execute(sql)
       # 提交到数据库执行
       db.commit()
    except:
       # 如果发生错误则回滚
       db.rollback()
    # 关闭数据库连接
    db.close()

def getRow():
    # 打开数据库连接
    db = pymysql.connect("localhost","root","","test" )
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 查询语句
    sql = "SELECT * FROM EMPLOYEE \
           WHERE INCOME > '%d'" % (1000)
    print (sql);
    try:
       # 执行SQL语句
       cursor.execute(sql)
       # 获取所有记录列表
       results = cursor.fetchall()
       for row in results:
          fname = row[0]
          lname = row[1]
          age = row[2]
          sex = row[3]
          income = row[4]
           # 打印结果
          print ("fname=%s,lname=%s,age=%d,sex=%s,income=%d" % \
                 (fname, lname, age, sex, income ))
    except:
       print ("Error: unable to fecth data")
    # 关闭数据库连接
    db.close()

#更新数据库记录
def updateRow(where):
    # 打开数据库连接
    db = pymysql.connect("localhost","root","","test" )
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 更新语句
    sql = "UPDATE EMPLOYEE SET AGE = AGE + 1 \
                              WHERE SEX = '%c'" % (where)
    try:
       # 执行SQL语句
       cursor.execute(sql)
       # 提交到数据库执行
       db.commit()
    except:
       # 发生错误时回滚
       db.rollback()

    # 关闭数据库连接
    db.close()

def deleteRow():
    # 打开数据库连接
    db = pymysql.connect("localhost","test","","test" )
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 删除语句
    sql = "DELETE FROM EMPLOYEE WHERE AGE > '%d'" % (20)
    try:
       # 执行SQL语句
       cursor.execute(sql)
       # 提交修改
       db.commit()
    except:
       # 发生错误时回滚
       db.rollback()
    # 关闭连接
    db.close()


if __name__ == '__main__':
    insertRow()

