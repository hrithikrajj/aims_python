import os
import sqlite3
import csv
import time
import student
import login
import math
from tabulate import  tabulate
def insert_student():
    c = input("You want to insetrt using csv or manual entry \n1.Using CSV \n2.Manual Entry\n")
    temp = sqlite3.connect("aims.db")
    newcur = temp.cursor()
    if c == "2":
        rid, username, name, courseid = input("Please enter Registration ID , username , name , courseid \n").split()
        query = "INSERT INTO registration values (?,?,?,?)"
        val = (rid, username, name, courseid)
        newcur.execute(query, val)
    if c == "1":
        csv_file = open('registration.csv')
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        query_2 = "INSERT INTO registration values (?,?,?,?)"
        try:
            for row in csv_reader:
                if(line_count != 0):
                    rid = row[0]
                    username = row[1]
                    name = row[2]
                    courseid = row[3]
                    val = (rid,username,name,courseid)
                    newcur.execute(query_2, val)
                line_count += 1
            print("Students added sucessfully")
        except:
            print("Problem in adding students")
    temp.commit()
    temp.close()


def insert_faculty():
    temp = sqlite3.connect("aims.db")
    newcur = temp.cursor()
    fid, username, fname = input("Please enter FacultyID , faculty username , faculty name \n").split()
    query = "INSERT INTO faculty values (?,?,?)"
    val = (fid,username,fname)
    newcur.execute(query,val)
    temp.commit()
    temp.close()



def insert_courses():
    a = input("1.Edit a subject \n2.Register a subject\n")
    if a == "1":
        print("All cources are : \n")
        con = sqlite3.connect("aims.db")
        cur = con.cursor()
        query = "SELECT subid, title, credit, pc FROM subcatalogue"
        res = cur.execute(query)
        res = res.fetchall()
        table = []
        for row in res:
            list = [row[0], row[1], row[2],row[3]]
            table.append(list)
        print(tabulate(table, headers=["Course ID", "Title", "Credits","Core course [Y/N]"], tablefmt="fancy_outline"))
        code = input("Please enter course code you want to Edit from above list of courses :")
        code = code.upper()
        query = f"""SELECT subid  from subcatalogue where subid = '{code}'"""
        res = cur.execute(query)
        res = res.fetchone()
        if res != None:
            preid ,title,courseid,ltpsc,semid,credit,pc = input("Enter details in the order Prerequisite ID, TITLE, Course ID,LTPSC, SEM ID, credit, CORE [Y/N]\n").split()
            query = f"""UPDATE subcatalogue SET preid = '{preid}',title = '{title}' , courseid='{courseid}', ltpsc='{ltpsc}',semid='{semid}', credit='{credit}' , pc = '{pc}' WHERE subid='{code}'"""
            cur.execute(query)
        else:
            print("wrong course name")
        con.commit()
        con.close()
    if a == "2":
        c = input("You want to insetrt using csv or manual entry \n1.Using CSV \n2.Manual Entry\n")
        temp = sqlite3.connect("aims.db")
        newcur = temp.cursor()
        if c == "2":
            preid, subid,title, couseid, ltpsc, semid, credit, pc =  input("Please enter Prerequisite id, subject id, title, course id, LTPSC, semid, credit, CORE[y/n]\n").split()
            query = "INSERT INTO subcatalogue values (?,?,?,?,?,?,?,?)"
            val = (preid,subid,title,couseid,ltpsc, semid, credit, pc)
            newcur.execute(query,val)
            if c == "1":
                with open('catalogue.csv') as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    line_count = 0
                    for row in csv_reader:
                        if(line_count != 0):
                            preid = row[0]
                            subid = row[1]
                            title = row[2]
                            couseid = row[3]
                            ltpsc = row[4]
                            semid = row[5]
                            credit = row[6]
                            pc = row[7]
                            query = "INSERT INTO subcatalogue values (?,?,?,?,?,?,?,?)"
                            val = (preid, subid,title, couseid, ltpsc, semid, credit, pc)
                            try:
                                newcur.execute(query, val)
                            except:
                                print(f"Errot in entry : {val}")
                        line_count += 1
        temp.commit()
        temp.close()


def student_check(rid):
    con = sqlite3.connect("aims.db")
    cur = con.cursor()
    queery = f"""SELECT rid from registration WHERE rid = '{rid}'"""
    res = cur.execute(queery)
    res = res.fetchone()
    return res


def view_grades():
    con = sqlite3.connect("aims.db")
    cur = con.cursor()
    option = input("1.view grades of current running courses\n2.View grades of previous batches\n")
    if option == "1":
        regid = input("Enter student Registration number : ")
        regid = regid.upper()
        r = student_check(regid.upper())
        if r != None:
            query = f"""SELECT T3.rid, T3.name,T2.subid, T2.title,T1.grades FROM runningcourses as T1 ,subcatalogue as T2, registration as T3 WHERE T1.subid = T2.subid AND T1.regid = T3.rid AND T3.rid = '{regid}'"""
            res = cur.execute(query)
            res = res.fetchall()
            if res.__len__() == 0:
               print("Student haven't taken any course")
            else:
                table  = []
                for row in res:
                    name = row[1]
                    list = [row[0], row[2], row[3], row[4]]
                    table.append(list)
                print(tabulate(table, headers=["Registration ID", "Course Code ", "Title ","Grade"], tablefmt="fancy_outline"))
        else:
            print("Student not found")
    if option == "2":
        regid = input("Enter student Registration number : ")
        regid = regid.upper()
        r = student_check(regid)
        if r != None:
            student.previous_performance(regid)
        else:
            print("student not found")

def grade_point_into_grade(point):
    if point == 10:
       return "A"
    if point == 9:
       return "A-"
    if point == 8:
       return "B"
    if point == 7:
       return "B-"
    if point == 6:
       return "C"
    if point == 5:
       return "c-"
    if point == 4:
       return "D"
    if point == 3:
       return "E"
def generate_transcript():
    rid = input("Enter id of the student : ")
    rid = rid.upper()
    con = sqlite3.connect("aims.db")
    cur = con.cursor()
    queery = f"""SELECT rid ,username,name,courseid from registration WHERE rid = '{rid}'"""
    res = cur.execute(queery)
    res = res.fetchone()
    if res != None:
        courseid = int(res[3])
        if courseid == 1:
            course = "Computer science"
        else:
            course = "Artificial intelligence"

        file = open(f'{rid}_transcript.txt','w')
        file.write(f'Name : {res[2]}\n')
        file.write(f'Registration id : {res[0]}\n')
        file.write(f'Programme Name : {course}\n')
        query = f"""SELECT semid FROM currentstudying WHERE rid = '{rid}'"""
        res = cur.execute(query)
        res = res.fetchone()
        sem = int(res[0])
        sem_1 = student.sem_marks("1", rid)
        sem_1_grades = 0
        sem_3_grades = 0
        sem_4_grades = 0
        total_credits_4 = 0
        total_credits_3 = 0
        sem_id = student.get_current_sem(rid)
        if sem_1 == None:
            print("No data found ")
        if sem_1 != None:
            file.write("Sem 1 Performance :\n")
            table = []
            total_credits_1 = 0
            sem_1_grades = 0
            for row in sem_1:
                sem_1_grades = sem_1_grades + int(row[0])
                subid = row[1]
                cred = int(row[0])
                query = f"""SELECT credit,title FROM subcatalogue where subid = '{subid}'"""
                res = cur.execute(query)
                res = res.fetchone()
                total_credits_1 = total_credits_1 + int(res[0])
                title = res[1]
                gradepoints = cred / int(res[0])
                grade = grade_point_into_grade(math.floor(gradepoints))
                list = [subid, res[0], title, grade, res[0], cred]
                table.append(list)
            file.write(tabulate(table, headers=["Course ID", "Course credit", "Title ", "Grade Rewarded", "Credit earned",
                                           "Points Secured"], tablefmt="fancy_outline"))
            file.write("\n")
            sem_1_CGPA = sem_1_grades / total_credits_1
            file.write(f"Sem 1 CGPA : %.2f \n" % sem_1_CGPA)
            file.write(f"Credits earned in first semester are : {total_credits_1}\n")
        else:
            print("No data found on SEMESTER 1")
        sem_2 = student.sem_marks("2", rid)
        if sem_2 != None:
            file.write("Sem 2 Performance : \n")
            table = []
            sem_2_grades = 0
            total_credits_2 = 0
            for row in sem_2:
                sem_2_grades = sem_2_grades + int(row[0])
                subid = row[1]
                cred = int(row[0])
                query = f"""SELECT credit,title FROM subcatalogue where subid = '{subid}'"""
                res = cur.execute(query)
                res = res.fetchone()
                total_credits_2 = total_credits_2 + int(res[0])
                title = res[1]
                gradepoints = cred / int(res[0])
                grade = grade_point_into_grade(math.floor(gradepoints))
                list = [subid, res[0], title, grade, res[0], cred]
                table.append(list)
            file.write(tabulate(table, headers=["Course ID", "Course credit", "Title ", "Grade Rewarded", "Credit earned",
                                           "Points Secured"], tablefmt="fancy_outline"))
            file.write("\n")
            sem_2_CGPA = sem_2_grades / total_credits_2
            file.write(f"Sem 2 CGPA : %.2f\n" % sem_2_CGPA)
            file.write(f"Credits earned in second semester are : {total_credits_2}\n")
        else:
            print("NO data on second semester")
        year_1_cgpa = (sem_1_grades + sem_2_grades) / (total_credits_2 + total_credits_1)
        file.write(f"Year 1 CGPA : %.2f\n" % year_1_cgpa)
        if sem_id == 5 or sem_id == '5':
            sem_3 = student.sem_marks("3", rid)
            table = []
            sem_3_grades = 0
            total_credits_3 = 0
            if sem_3 != None:
                for row in sem_3:
                    sem_3_grades = sem_3_grades + int(row[0])
                    subid = row[1]
                    cred = int(row[0])
                    query = f"""SELECT credit,title FROM subcatalogue where subid = '{subid}'"""
                    res = cur.execute(query)
                    res = res.fetchone()
                    total_credits_3 = total_credits_3 + int(res[0])
                    title = res[1]
                    gradepoints = cred / int(res[0])
                    grade =grade_point_into_grade(math.floor(gradepoints))
                    list = [subid, res[0], title, grade, res[0], cred]
                    table.append(list)
            file.write("Sem 3 Performance \n")
            file.write(tabulate(table, headers=["Course ID", "Course credit", "Title ", "Grade Rewarded", "Credit earned",
                                           "Points Secured"], tablefmt="fancy_outline"))
            file.write("\n")
            sem_3_CGPA = sem_3_grades / total_credits_3
            file.write(f"Sem 3 CPGA : %.2f\n" % sem_3_CGPA)
            file.write(f"Credits earned in third semester are : {total_credits_3}\n")
            sem_3 = student.sem_marks("4", rid)
            table = []
            sem_4_grades = 0
            total_credits_4 = 0
            if sem_3 != None:
                for row in sem_3:
                    sem_4_grades = sem_4_grades + int(row[0])
                    subid = row[1]
                    cred = int(row[0])
                    query = f"""SELECT credit,title FROM subcatalogue where subid = '{subid}'"""
                    res = cur.execute(query)
                    res = res.fetchone()
                    total_credits_4 = total_credits_4 + int(res[0])
                    title = res[1]
                    gradepoints = cred / int(res[0])
                    grade = grade_point_into_grade(math.floor(gradepoints))
                    list = [subid, res[0], title, grade, res[0], cred]
                    table.append(list)
            file.write("Sem 4 Performance \n")
            file.write(tabulate(table, headers=["Course ID", "Course credit", "Title ", "Grade Rewarded", "Credit earned",
                                           "Points Secured"], tablefmt="fancy_outline"))
            file.write("\n")
            sem_3_CGPA = sem_4_grades / total_credits_4
            file.write(f"Sem 4 CPGA : %.2f\n" % sem_3_CGPA)
            file.write(f"Credits earned in fourth semester are : {total_credits_4}\n")
            year_2_cgpa = (sem_3_grades + sem_4_grades) / (total_credits_3 + total_credits_4)
            file.write(f"Year 2 CGPA : %.2f\n" % year_2_cgpa)
        year_cgpa = (sem_1_grades + sem_2_grades + sem_3_grades + sem_4_grades) / (
                    total_credits_1 + total_credits_2 + total_credits_3 + total_credits_4)
        file.write(f"CGPA : %.2f\n" % year_cgpa)
        query_mtp = f"""SELECT T2.fname, T1.title, T1.description from faculty as T2, mtpinfo as T1 where T1.fid = T2.fid and T1.rid = '{rid}'"""
        res_mtp = cur.execute(query_mtp)
        res_mtp = res_mtp.fetchone()
        if res_mtp != None:
            file.write("MTP details are as follow:\n")
            file.write(f"Title : {res_mtp[1]}\n")
            file.write(f"Description : {res_mtp[2]}\n")
            file.write(f"Instructor Name : {res_mtp[0]}\n")
        print(f"Transcript sucessfully created in current directory names as ``` {rid}_transcript.txt ```")
    else:
        print("No such user exist")





def main(usertype):
    os.system("clear")
    con = sqlite3.connect("aims.db")
    cur = con.cursor()
    query = f"""SELECT username FROM sessiontable where usertype = '{usertype}' """
    res = cur.execute(query)
    res = res.fetchone()
    user_name  = res[0]
    print(f"Welcome {user_name}")
    more = 'y'
    while more == 'y' or more == 'Y':
        # print(f"welcome {username}\n")
        print(
"""1.Register student  
2.Register faculty
3.Update or EDIT subjects
4.View Grades
5.Create transcript 
6.Logout""")
        choice = input()
        if choice not in ["1", "2", "3", "4","5","6"]:
            print("wrong choice")
        else:
            if choice == "5":
                generate_transcript()
            if choice == "6":
                login.logout(usertype)
                return
            if choice == "1":
                insert_student()
            if choice == "2":
                insert_faculty()
            if choice == "3":
                if user_name == 'STAFDEAN':
                    insert_courses()
                else:
                    print("You are not authorized ")
            if choice == "4":
                view_grades()
        more = input("do you want to continue [Y / N] : ")
        if more in ['y', 'Y' ]:
            os.system("clear")
        else:
            login.logout(usertype)
            print("Logging out")
            time.sleep(1)
            con.close()
