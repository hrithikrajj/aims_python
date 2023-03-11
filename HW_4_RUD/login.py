import sqlite3
import getpass
import os
import time


def logout(user):
    con = sqlite3.connect("aims.db")
    cur = con.cursor()
    query = f"""DELETE FROM sessiontable where usertype ='{user}'"""
    cur.execute(query)
    con.commit()
    con.close()
    os.system("clear")



def login(user):
    user_name = input("Enter user name : ")
    passwd = getpass.getpass("Enter password : ")
    con = sqlite3.connect("aims.db")
    cur = con.cursor()
    user_name = user_name.upper()
    query = f"SELECT username , password FROM {user}_credentials WHERE username = '{user_name}'"
    res = cur.execute(query)
    res = res.fetchone()
    if res == None:
        if user == "student":
            type = "registration"
        if user == "faculty":
            type = "faculty"
        if user == "acad":
            print("login failed")
            return 0
        query = f"""SELECT username FROM {type} where username='{user_name}'"""
        res = cur.execute(query)
        res = res.fetchone()
        if res != None:
            print("User first time login Please enter new password ")
            passwd = getpass.getpass("Enter password : ")
            query = f"""INSERT INTO {user}_credentials values(?,?)"""
            val = (user_name, passwd)
            cur.execute(query, val)
            query_2 = f"""DELETE FROM sessiontable where usertype ='{user}'"""
            cur.execute(query_2)
            ct = str( int(time.time() * 1000000))
            query_3 = f"INSERT INTO sessiontable values (?,?,?)"
            val = (ct, user_name, user)
            cur.execute(query_3, val)
            con.commit()
            print("login sucessfull ")
            con.commit()
            con.close()
            return 1
        else:
            print(f"No user with {user_name} exist of type : {user}")
            return 0
    if user_name == res[0] and passwd != res[1]:
        print("login failed")
        time.sleep(2)
        return 0
    if user_name == res[0] and passwd == res[1]:
        query = f"""DELETE FROM sessiontable where usertype ='{user}'"""
        cur.execute(query)
        ct = str( int(time.time() * 1000000))
        query_3 = f"INSERT INTO sessiontable values (?,?,?)"
        val = (ct, user_name, user)
        cur.execute(query_3, val)
        con.commit()
        print("Login in sucessfull")
        time.sleep(2)
        return 1
    con.close()
