# encoding: utf-8

"""
文件：database_to_file.py
作者：wq0426
时间：2024-01-10 23:42
描述：通过脚本传参（数据库和表）实现将数据表中的数据格式，按照指定的格式存入本地文件
"""
import sys
import pymysql
import os

FORLDER = 'database_file'
HOST = '127.0.0.1'
USER = '你的用户名'
PASSWORD = '你的密码'

def analyzeFile(file):
    # 目录是否存在
    if not (os.path.exists(FORLDER)) or not os.path.isdir(FORLDER):
        os.mkdir(FORLDER)
    # 文件是否已存在
    if (os.path.exists(file)):
        os.unlink(file)

class DataDict:
    def __init__(self, table_schema, table_name):
        self.table_schema = table_schema
        self.table_name = table_name

    def run(self):
        conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=self.table_schema)
        cursor = conn.cursor()
        sql = 'show databases like "' + self.table_schema + '"'
        print(sql)
        cursor.execute(sql)
        if (len(self.table_name) == 0):
            print("table is null")
            exit(0)
        file_path = FORLDER + "/" + self.table_schema + "_" + self.table_name + ".md"
        analyzeFile(file_path)
        header = "column_name" + "|" + "column_type" + "|" + "column_default" + "|" + "column_comment\n"
        with open(file_path, "a") as file:
            file.write(header)
            cursor.execute("select COLUMN_NAME, DATA_TYPE, COLUMN_DEFAULT, COLUMN_COMMENT from information_schema.COLUMNS where  TABLE_SCHEMA='blog' and TABLE_NAME='t_blog'")
            res = cursor.fetchall()
            for item in res:
                file.write(item[0] + "|" + item[1] + "|" + str(item[2]) + "|" + item[3] + "\n")
        cursor.close()
        conn.close()

if __name__=='__main__':
    args = sys.argv
    if (len(args) < 2):
        print("数据库不能为空")
        exit(0)
    table_schema = args[1]
    table_name = ''
    if (len(args) > 2):
        table_name = args[2]
    dict = DataDict(table_schema, table_name)
    print('数据库开始映射到文件...\n')
    dict.run()
    print('Done.\n')