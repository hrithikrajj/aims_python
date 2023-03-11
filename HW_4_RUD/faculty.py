import os
import sqlite3
import csv

import academics
import login
import time
from tabulate import tabulate
def deregister(id):
    con = sqlite3.connect('aims.db')
    cur = con.cursor()
    currentoffering(id)
    code = input("Enter course code you want to degister :")
    code = code.upper()
    query = f"""DELETE FROM offered WHERE fid='{id}' AND subid='{code}'"""
    try:
        cur.execute(query)
    except:
        print("There is some problem please try again")
    con.commit()
    con.close()

def current_enrolled_students(fid):

    con = sqlite3.connect("aims.db")
    cur = con.cursor()
    query = f"""SELECT T1.rid , T1.name , T2.title , t3.subid from registration as T1, subcatalogue as T2, runningcourses as T3 where T1.rid = T3.regid and T2.subid = T3.subid and T3.fid = '{fid}'"""
    res = cur.execute(query)
    res = res.fetchall()
    if res.__len__() > 0:
        print("list of enrolled students")
        table = []
        for row in res:
            list = [row[0],row[1],row[2], row[3]]
            table.append(list)
    print(tabulate(table, headers=["Registration ID", "Student name", "Course Name", "Sub code"],tablefmt="fancy_outline"))
    con.commit()
    con.close()


def offercourse(fid):
    con = sqlite3.connect("aims.db")
    cur = con.cursor()
    query = """SELECT subid,title , ltpsc FROM subcatalogue WHERE pc = 'N'"""
    res = cur.execute(query)
    res = res.fetchall()
    print("List of available courses : \n")
    i = 1
    table = []
    for row in res:
        if row[0] != 'CS699' and row[0] != 'CS799':
            list = [row[0],row[1],f"{row[2][0]}-{row[2][1]}-{row[2][2]}-{row[2][3]}-{row[2][4]}",]
            table.append(list)
    print(tabulate(table, headers=["Course ID", "Course Title", "Structure (L-T-P-S-C)"],tablefmt="fancy_outline"))
    code = input("Please enter course code you want to teach from above list of courses :")
    code = code.upper()
    query = f"""SELECT subid from subcatalogue where subid = '{code}'"""
    res = cur.execute(query)
    res.fetchone()
    if res != None :
        query = f"""SELECT fid ,subid from offered where subid = '{code}' AND fid = '{fid}'"""
        res = cur.execute(query)
        res = res.fetchone()
        if res == None :
            query = """INSERT INTO offered values (?,?,?)"""
            choice = 1000
            while choice not in range(0, 10):
                choice = int(input("Enter constraints of CGPA in course (Put 0 if no constraints are on the course) : "))
            val = (fid, code, choice)
            res = cur.execute(query, val)
        else:
            print("Already offered by you ")
    else:
        print("Error in course Name please check")
    con.commit()
    con.close()


def currentoffering(fid):
    con = sqlite3.connect("aims.db")
    cur = con.cursor()
    query = f"""SELECT  T2.subid, T2.title  from offered as T1 NATURAL  JOIN  subcatalogue as T2 WHERE T1.fid = '{fid}'"""
    res = cur.execute(query)
    res = res.fetchall()
    table = []
    if res != None :
        for row in res:
            list = [row[0],row[1],]
            table.append(list)
        print(tabulate(table, headers=["Course ID", "Course Title" ],tablefmt="fancy_outline"))

def changegrades(fid):
    con = sqlite3.connect("aims.db")
    cur = con.cursor()
    current_enrolled_students(fid)
    choice = input("1.Enter manually\n2.Enter by using CSV\n")
    if choice == "1":
        subid, regid, grades = input("Enter subject id , registration id, grades :\n").split()
        query = f"""UPDATE runningcourses set grades = '{grades}' where subid='{subid}' AND fid='{fid}'"""
        try:
            cur.execute(query)
        except:
            print("something is wrong scores not updated")
        con.commit()
    if choice == "2":
        path = input("Enter path of CSV file : ")
        try:
            with open(path) as csv_file:
                if csv_file.closed:
                    print("wrong path please check")
                else:
                    csv_reader = csv.reader(csv_file, delimiter=",")
                    line_count = 0
                    for row in csv_reader:
                        if line_count != 0:
                            try:
                                if fid == row[3]:
                                    query = f"""UPDATE runningcourses set grades = '{row[2]}' WHERE subid='{row[0]}' AND fid = '{row[3]}' AND regid='{row[1]}'"""
                                else:
                                    print("You are trying to update marks of someone else course")
                                cur.execute(query)
                            except:
                                print(f"Some error please check for : subid :{row[0]} and fid : {row[3]}")
                        line_count += 1
                    con.commit()
                print("Operation done without error sucessfully")
        except:
            print("Some erroe while openenin please check path")
    con.close()

def current_mtp(fid):
    con = sqlite3.connect("aims.db")
    cur = con.cursor()
    query = f"""SELECT T1.title, T2.name from registration as T2, mtpinfo as T1 where T1.rid = T2.rid and T1.fid = '{fid}'"""
    res = cur.execute(query)
    res = res.fetchall()
    if res.__len__() != 0:
        i = 1
        print("Following is the list of all the MTP currently been persuing under you")
        for row in res:
            print(f"{i}. Title : {row[0]} Student Name : {row[1]}")
            i += 1
    else:
        print("NO one is pursuing mtp under you")
    con.commit()
    con.close()
    pass

def main(usertype):
    os.system("clear")
    con = sqlite3.connect("aims.db")
    cur = con.cursor()
    query = f"""SELECT username FROM sessiontable where usertype = '{usertype}' """
    res = cur.execute(query)
    res = res.fetchone()
    username = res[0]
    query = f"""SELECT fname,fid FROM faculty WHERE username='{username}'"""
    res = cur.execute(query)
    res = res.fetchone()
    name = res[0]
    id = res[1]
    con.close()
    print(f"welcome {name}")
    more = 'y'
    while more == 'y' or more == 'Y':
        print("1.ADD or REMOVE a course \n2.See which course are being offered by you\n3.Change grades of the students\n4.Current pursing MTP\n5.Enrolled Students \n6.View Grades \n7.Logout")
        choice = input()
        if choice not in ["1", "2", "3", "4", "5","6","7"]:
            print("wrong choice")
        else:
            if choice == "6":
                academics.view_grades()
            if choice == "5":
                current_enrolled_students(id)
            if choice == "4":
                current_mtp(id)
            if choice == "7":
                login.logout(usertype)
                return
            if choice == "1":
                try:
                    option = input("1.Register a course\n2.DeRegister a course\n")
                    if option == "1":
                        offercourse(id)
                    if option == "2":
                        deregister(id)
                except:
                    print("some error")
            if choice == "2":
                currentoffering(id)
            if choice == "3":
                try:
                    changegrades(id)
                except:
                    print("some problem")
        more = input("Do you want to continue [Y / N] : ")
        if more in ['y', 'Y']:
            os.system("clear")
        else:
            login.logout(usertype)
            print("Logging out")
            time.sleep(1)
            con.close()
