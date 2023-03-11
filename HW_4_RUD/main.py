import sqlite3

import login as login
import academics as acad
import student as student
import faculty as faculty
import time
import os


def welcome():
    print("""Login before continue
1.Student
2.faculty
3.academics""")
    choice = input()
    return choice


if __name__ == '__main__':
    while 1:
        os.system("clear")
        choice = welcome()
        while (choice not in ["1", "2", "3"]):
            print("Not a valid choice")
            time.sleep(3)
            os.system("clear")
            choice = welcome()
        con = sqlite3.connect("aims.db")
        cur = con.cursor()
        if choice == "1":
            user = "student"
        if choice == "2":
            user = "faculty"
        if choice == "3":
            user = "acad"
        query = f"""SELECT usertype FROM sessiontable where usertype = '{user}'"""
        res = cur.execute(query)
        res = res.fetchone()
        flag = 1
        if res != None:
            i = input("Already a session exist you want  to terminate [Y/N] : ")
            if i == 'y' or i == 'Y':
                query_2 = f"""DELETE FROM sessiontable where usertype ='{user}'"""
                cur.execute(query_2)
                con.commit()
                flag = 1
            else:
                flag = 0
        if flag == 1:
            result = login.login(user)
            if result == 1:
                if user == "student":
                    student.main(user)
                elif user == "faculty":
                    faculty.main(user)
                elif user == "acad":
                    acad.main(user)
        else:
            os.system("clear")
