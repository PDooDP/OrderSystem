# pymysql.connect(host="127.0.0.1", user="username", passwd="password", database="your_database_name")
class dbConn():
    def __init__(self, db):
        self.db = db
        self.c = self.db.cursor()        

    def connEnd(self):
        self.c.close()
        self.db.close()

    # 找出所有的資料
    def sql_selectFetchAll(self, sql):
        self.c.execute(sql)
        self.db.commit()
        data = self.c.fetchall()
        return data

    # 取回來的資料是tuple串列型態，故需設定index位置 (pos)
    def sql_selectFetchOne(self, sql, pos=-1):
        self.c.execute(sql)
        self.db.commit()
        if pos >= 0:
            data = self.c.fetchone()[pos]
            return data
        else:
            data = self.c.fetchone()
            return data

    # update, insert, delete
    def sql_execute(self, sql):
        self.c.execute(sql)
        self.db.commit()
        
