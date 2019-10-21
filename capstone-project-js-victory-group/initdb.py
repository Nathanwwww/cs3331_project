import sqlite3
import random
import datetime,re
from sqlite3 import Error
from src.user import create_db, User
conn = sqlite3.connect('forex.db')
cur = conn.cursor()

create_db('forex.db')

user_list = []
User.createUser('shangjie','123456','shangjie@gmail.com')
User.createUser('zhounan','123456','zhounan@gmail.com')
User.createUser('libo','123456','libo@gmail.com')
User.createUser('zoudiming','123456','zoudiming@gmail.com')
# def create_user():
#     user_list = [['shangjie','123456','shangjie@gmail.com'],['zhounan','123456','zhounan@gmail.com'],['libo','123456','libo@gmail.com'],['zoudiming','123456','zoudiming@gmail.com']]
 
#     for i in user_list:
#         user = []
#         for j in range(len(i)):
#             user.append(i[j])
#         creation_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         user.append(creation_time)
#         print("user : ", user)
#         cur.execute("INSERT INTO USER VALUES (?,?,?,?)", user)
#     conn.commit()
#     print("Created Successfully!")

# create_user()