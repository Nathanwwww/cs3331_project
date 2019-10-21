import sqlite3

mydb = sqlite3.connect('forex.db')
cursor = mydb.cursor()
cursor.execute('select name from sqlite_master where type="table";')
tables = cursor.fetchall()
print(tables)
cursor.execute('select * from user')
user = cursor.fetchall()
print(user)