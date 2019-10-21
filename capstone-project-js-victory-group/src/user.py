import os
import random
import sqlite3
from sqlite3 import Error
import json 
import datetime,re

#create the database
def create_db(db_file):
    try:
        conn = sqlite3.connect(db_file)
        create_table_user = """CREATE TABLE IF NOT EXISTS USER(
                                        username text primary key,
                                        password text NOT NULL,
                                        -- userID integer UNIQUE AUTOINCREMENT,
                                        email text NOT NULL UNIQUE,
                                        creation_time time                                    
                                    ); """

        create_table_account = """CREATE TABLE IF NOT EXISTS ACCOUNT(
                                        currencyid text,
                                        remain text NOT NULL UNIQUE,
                                        username references USER(username)                                   
                            ); """
        cur = conn.cursor()
        cur.execute(create_table_user)
        print("DONE!")
        cur.execute(create_table_account)
        conn.commit()
        conn.close()
    except Error as e:
        print("Error on Sql", e)

class User:
    # implement the register/sign up function (create the new user)
    @staticmethod
    def createUser(username, password, email):
        try:
            conn = sqlite3.connect('forex.db')
        except Error as e:
            print(e)

        cur = conn.cursor()
        creation_time = datetime.datetime.now()
        cur.execute("INSERT INTO USER(username,password,email,creation_time) VALUES (?,?,?,?)", (username, password,email,creation_time))
        conn.commit()
        print("Create Successfully!")
        # cur.execute("SELECT userid FROM USER WHERE username = ?",(username,))
        # conn.commit()
        # userid = cur.fetchone()
        # print("This is the userid:  ", userid)
        conn.close()
        return True

    # implement the login function
    @staticmethod
    def login(username, password):
        try:
            conn = sqlite3.connect('forex.db')
        except Error as e:
            print(e)
       
        cur = conn.cursor()
        print("username: ",username)
        print("\n password: ",password)
        cur.execute("SELECT * FROM USER WHERE password = ? AND username = ? ", (password,username))
        conn.commit()
        result = cur.fetchone()
        conn.close()

        #return the result
        if result:
            return True
        else:
            print("No this user")
            return False 
            

    # Using for change the password
    @staticmethod
    def reset(newpsw,username):
        try:
            #connect the database
            conn = sqlite3.connect('forex.db')
        except Error as e:
            print(e)
        
        cur = conn.cursor()
        print("new password: ", newpsw)
        print("username: ", username)

        #update the password
        cur.execute("UPDATE USER SET password = ? WHERE username = ? ", (newpsw, username))
        conn.commit()

        #check if the password is changed.
        cur.execute("SELECT password FROM USER WHERE username = ?",(username,))
        conn.commit()
        new = cur.fetchone()
        # print("after change: ", new[0], len(new[0]), type(new[0]))
        # print("input password: ", newpsw, len(newpsw), type(newpsw))
        conn.close()

        # Return the result
        if newpsw == new[0]:
            print("Reset success")
            return True 
        else:
            print("not success!")
            return False



if __name__ == '__main__':
    create_db('forex.db')
    a = User()
    # a.createUser('shangjie','123456','shangjie@gmail.com')
