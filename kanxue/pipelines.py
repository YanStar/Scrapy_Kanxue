# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3

class KanxuePipeline(object):

    DATABASE = 'kanxue.db'
    TABLE_NAME = "table"
    CREATE_TABLE_SQL = "CREATE TABLE IF NOT EXISTS '{0}' (id INTEGER PRIMARY KEY AUTOINCREMENT, title VARCHAR(150), url VARCHAR(100))"
    INSERT_DATA_SQL = "INSERT INTO '{0}' (title,url) VALUES ('{1}','{2}')"

    def CheckExit(self,table, title):   #查重
        sql = 'select * from {0} where title = \'{1}\' '.format(table, title)
        num = ""
        try:
            try:
                conn = sqlite3.connect(self.DATABASE)
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                num = cur.fetchall()
                conn.close()
                try:
                    n = len(num)
                except:
                    n = 0
            finally:
                if hasattr(conn, 'close'):
                    conn.close()
                if n == 0:
                    return False
                else:
                    return True
        except:
            return False

    def process_item(self, item, spider):
        title = item['title']
        url = item['url']
        conn = sqlite3.connect(self.DATABASE)
        conn.isolation_level = None
        conn.execute(self.CREATE_TABLE_SQL.format(self.TABLE_NAME))
        if self.CheckExit(self.TABLE_NAME,title) == False:
            conn.execute(self.INSERT_DATA_SQL.format(self.TABLE_NAME,title,url))
        else:
            print("Have Exist!")
        conn.close()
        return item

