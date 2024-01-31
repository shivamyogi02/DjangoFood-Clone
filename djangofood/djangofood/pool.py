import pymysql as SQL
def OpenConnection():
    DB=SQL.connect(host="localhost", port=3306, user="root", password="1234", database="djfood", cursorclass=SQL.cursors.DictCursor) 
    SMT=DB.cursor()
    return DB,SMT