import math
import os
import sqlite3
import time
import login
import academics
from tabulate import tabulate
def get_current_sem(rid):
    con = sqlite3.connect("aims.db")
    cur = con.cursor()
    query = f"""SELECT semid from currentstudying where rid = '{rid}'"""
    res = cur.execute(query)
    res= res.fetchone()
    con.commit()
    con.close()
    return res[0]

def getcredits(rid):
    con = sqlite3.connect('aims.db')
    cur = con.cursor()
    query = f"""SELECT semID,creditsearned FROM semresult WHERE regid = '{rid}' ORDER BY semID DESC"""
    res = cur.execute(query)
    res = res.fetchone()
    if res == None or res.__len__() == 0:
        return 24
    credit = res[1]
    credit = math.ceil(1.25 * int(credit))
    con.commit()
    con.close()
    return credit
def getCourseid(rid):
    con = sqlite3.connect("aims.db")
    cur = con.cursor()
    query = f"""SELECT courseid FROM registration where rid = '{rid}'"""
    res = cur.execute(query)
    res = res.fetchone()
    con.commit()
    con.close()
    return res[0]


def sem_result(semID, rid):
    con = sqlite3.connect("aims.db")
    cur = con.cursor()
    query = f"""SELECT creditsearned FROM semresult where regid = '{rid}' AND semID = '{semID}'"""
    res = cur.execute(query)
    res = res.fetchone()
    con.close()
    return res


def sem_marks(semid, rid):
    con = sqlite3.connect("aims.db")
    cur = con.cursor()
    query = f"""SELECT grade,subid FROM prerecord WHERE rid = '{rid}' AND semid = '{semid}'"""
    res = cur.execute(query)
    res = res.fetchall()
    return res


def get_CGPA(rid, semid):
    sem = sem_marks(semid, rid)
    sum_1_grades = 0
    if sem != None:
        for row in sem:
            sum_1_grades = sum_1_grades + int(row[0])
        sum_1_grades = sum_1_grades / 14
    return sum_1_grades

def compute_CGPA(rid):
    sem_id = get_current_sem(rid)
    if sem_id == 1 or sem_id == '1':
        print("No record found")
        return
    con = sqlite3.connect("aims.db")
    cur = con.cursor()
    sem_1 = sem_marks("1", rid)
    sem_3_grades = 0
    sem_4_grades = 0
    total_credits_4 = 0
    total_credits_3 = 0
    if sem_1 == None:
        print("No data found ")
    if sem_1 != None:
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
            grade = academics.grade_point_into_grade(math.floor(gradepoints))
            list = [subid, res[0], title, grade, res[0], cred]
            table.append(list)
        sem_1_CGPA = sem_1_grades / total_credits_1
        print(f"Sem 1 CGPA : %.2f " % sem_1_CGPA)
    else:
        print("No data found on SEMESTER 1")
    sem_2 = sem_marks("2", rid)
    if sem_2 != None:
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
            grade = academics.grade_point_into_grade(math.floor(gradepoints))
            list = [subid, res[0], title, grade, res[0], cred]
            table.append(list)
        sem_2_CGPA = sem_2_grades / total_credits_2
        print(f"Sem 2 CGPA : %.2f" % sem_2_CGPA)
    else:
        print("NO data on second semester")
    year_1_cgpa = (sem_1_grades + sem_2_grades) / (total_credits_2 + total_credits_1)
    print(f"Year 1 CGPA : %.2f" % year_1_cgpa)
    if sem_id == 5 or sem_id == '5':
        sem_3 = sem_marks("3", rid)
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
                grade = academics.grade_point_into_grade(math.floor(gradepoints))
                list = [subid, res[0], title, grade, res[0], cred]
                table.append(list)
        sem_3_CGPA = sem_3_grades / total_credits_3
        print(f"Sem 3 CPGA : %.2f" % sem_3_CGPA)
        sem_3 = sem_marks("4", rid)
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
                grade = academics.grade_point_into_grade(math.floor(gradepoints))
                list = [subid, res[0], title, grade, res[0], cred]
                table.append(list)
        print("Sem 4 Performance ")
        sem_3_CGPA = sem_4_grades / total_credits_4
        print(f"Sem 4 CPGA : %.2f" % sem_3_CGPA)
        year_2_cgpa = (sem_3_grades + sem_4_grades) / (total_credits_3 + total_credits_4)
        print(f"Year 2 CGPA : %.2f" % year_2_cgpa)
    year_cgpa = (sem_1_grades + sem_2_grades + sem_3_grades + sem_4_grades) / (
                total_credits_1 + total_credits_2 + total_credits_3 + total_credits_4)
    print(f"CGPA : %.2f" % year_cgpa)
    con.commit()
    con.close()


def mtpinfo(rid):
    con = sqlite3.connect("aims.db")
    cur = con.cursor()
    query = f"""SELECT semid from currentstudying where rid ='{rid}'"""
    res = cur.execute(query)
    res = res.fetchone()
    cid = res[0]
    if cid == "3" or cid == 3 or cid == 4 or cid == '4'or cid == '5' or cid == 5 :
        query = f"""SELECT T1.title ,T1.description , T3.fname from mtpinfo as T1, registration as T2, faculty as T3 where T1.rid = '{rid}' And T1.rid = T2.rid and T1.fid = T3.fid"""
        res = cur.execute(query)
        res =res.fetchone()
        if res != None:
            print(f"Title : {res[0]} \nDescription: {res[1]} ")
            print(f"Instructor : {res[2]}")
        else:
            print("No MTP details found")
    else:
        print("No MTP details found ")
    con.commit()
    con.close()


def graduation_check(rid):
    sem_id = get_current_sem(rid)
    if sem_id != 5:
        print("Not Eligible for graduation check")
        return
    con = sqlite3.connect("aims.db")
    cur = con.cursor()
    query_pre = f"""SELECT DISTINCT T1.subid from prerecord as T1 , subcatalogue as T2 where T1.subid = T2.subid and T2.pc = 'Y' and T1.rid = '{rid}'"""
    res_pre = cur.execute(query_pre)
    res_pre = res_pre.fetchall()
    query_sub= """SELECT subid from  subcatalogue where pc = 'Y'"""
    res_sub = cur.execute(query_sub)
    res_sub = res_sub.fetchall()
    if res_sub.__len__() != res_pre.__len__():
        print("All core courses are not done")
        return
    sem1_credit = sem_result("1", rid)
    sem2_credit = sem_result("2", rid)
    sem3_credit = sem_result("3", rid)
    sem4_credit = sem_result("4", rid)
    if sem1_credit != None:
        sem1_credit = int(sem1_credit[0])
        if sem2_credit != None:
            sem2_credit = int(sem2_credit[0])
            if sem3_credit != None:
                sem3_credit = int(sem3_credit[0])
                if sem4_credit != None:
                    sem4_credit = int(sem4_credit[0])
                    cid = getCourseid(rid)
                    s_credit = sem4_credit + sem3_credit + sem2_credit + sem1_credit
                    if cid == 1 or cid == '1':
                        if s_credit == 60:
                            print("Congratulations you are graduated !!!")
                        else:
                            print("Credit requirement doesn't met you are a failure you suck")
                    elif cid == 2 or cid == '2':
                        if s_credit == 62:
                            print("Congratulations you are graduated !!!")
                        else:
                            print("Credit requirement doesn't met you are a failure you suck")
                    else:
                        print("Some thing is wrong please try later")
                else:
                    print("Not graduated")
            else:
                print("Not graduated")
        else:
            print("Not graduated")
    else:
        print("Not graduated")


def previous_performance(rid):
    sem_id = get_current_sem(rid)
    if sem_id == 1 or sem_id == '1':
        print("No record found")
        return
    con = sqlite3.connect("aims.db")
    cur = con.cursor()
    sem_1 = sem_marks("1", rid)
    sem_3_grades = 0
    sem_4_grades = 0
    total_credits_4 = 0
    total_credits_3 = 0
    if sem_1 == None:
        print("No data found ")
    if sem_1 != None:
        print("Sem 1 Performance :")
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
            grade = academics.grade_point_into_grade(math.floor(gradepoints))
            list = [subid,res[0],title,grade,res[0],cred]
            table.append(list)
        print(tabulate(table, headers=["Course ID", "Course credit", "Title ", "Grade Rewarded","Credit earned","Points Secured"],tablefmt="fancy_outline"))
        sem_1_CGPA = sem_1_grades / total_credits_1
        print(f"Sem 1 CGPA : %.2f "%sem_1_CGPA)
        print(f"Credits earned in first semester are : {total_credits_1}\n")
    else:
        print("No data found on SEMESTER 1")
    sem_2 = sem_marks("2", rid)
    if sem_2 != None:
        print("Sem 2 Performance : ")
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
            grade = academics.grade_point_into_grade(math.floor(gradepoints))
            list = [subid,res[0],title,grade,res[0],cred]
            table.append(list)
        print(tabulate(table, headers=["Course ID", "Course credit", "Title ", "Grade Rewarded","Credit earned","Points Secured"],tablefmt="fancy_outline"))
        sem_2_CGPA = sem_2_grades / total_credits_2
        print(f"Sem 2 CGPA : %.2f"%sem_2_CGPA)
        print(f"Credits earned in second semester are : {total_credits_2}\n")
    else:
        print("NO data on second semester")
    year_1_cgpa = (sem_1_grades + sem_2_grades) / (total_credits_2 + total_credits_1)
    print(f"Year 1 CGPA : %.2f"%year_1_cgpa)
    if sem_id == 5 or sem_id == '5':
        sem_3 = sem_marks("3",rid)
        table = []
        sem_3_grades = 0
        total_credits_3 = 0
        if sem_3 !=None:
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
                grade = academics.grade_point_into_grade(math.floor(gradepoints))
                list = [subid, res[0],title, grade, res[0], cred]
                table.append(list)
        print("Sem 3 Performance ")
        print(tabulate(table, headers=["Course ID", "Course credit", "Title ", "Grade Rewarded","Credit earned","Points Secured"],tablefmt="fancy_outline"))
        sem_3_CGPA = sem_3_grades / total_credits_3
        print(f"Sem 3 CPGA : %.2f"%sem_3_CGPA)
        print(f"Credits earned in third semester are : {total_credits_3}\n")
        sem_3 = sem_marks("4",rid)
        table = []
        sem_4_grades = 0
        total_credits_4 = 0
        if sem_3 !=None:
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
                grade = academics.grade_point_into_grade(math.floor(gradepoints))
                list = [subid, res[0],title, grade, res[0], cred]
                table.append(list)
        print("Sem 4 Performance ")
        print(tabulate(table, headers=["Course ID", "Course credit", "Title ", "Grade Rewarded","Credit earned","Points Secured"],tablefmt="fancy_outline"))
        sem_3_CGPA = sem_4_grades / total_credits_4
        print(f"Sem 4 CPGA : %.2f"%sem_3_CGPA)
        print(f"Credits earned in fourth semester are : {total_credits_4}")
        year_2_cgpa = (sem_3_grades + sem_4_grades) / (total_credits_3 + total_credits_4)
        print(f"Year 2 CGPA : %.2f"%year_2_cgpa)
    year_cgpa = (sem_1_grades+ sem_2_grades+sem_3_grades + sem_4_grades) / (total_credits_1+total_credits_2+total_credits_3 + total_credits_4)
    print(f"CGPA : %.2f"%year_cgpa)
    con.commit()
    con.close()


def main(usertype):
    os.system("clear")
    con = sqlite3.connect("aims.db")
    cur = con.cursor()
    query = f"""SELECT username FROM sessiontable where usertype = '{usertype}' """
    res = cur.execute(query)
    res = res.fetchone()
    username = res[0]
    query = f"""SELECT rid, name ,courseid FROM registration WHERE username = '{username}'"""
    res = cur.execute(query)
    res = res.fetchone()
    rid = res[0]
    name = res[1]
    print(f"welcome {name}")
    query = f"""SELECT semid,cid FROM currentstudying WHERE rid = '{rid}'"""
    res_2 = cur.execute(query)
    res_2 = res_2.fetchone()
    if res_2 == None:
        q = f"""SELECT semid FROM semresult WHERE regid = '{rid}' ORDER BY semid DESC"""
        res_q = cur.execute(q)
        res_q = res_q.fetchone()
        sem = 0
        if res_q != None:
            sem = int(res_q[0])
        sem = sem + 1
        c = getcredits(rid)
        cid = getCourseid(rid)
        q = f"""INSERT INTO currentstudying values(?,?,?,?)"""
        val_q = (rid, sem, cid, c)
        cur.execute(q, val_q)
        con.commit()
        if sem == 1:
            query = f"""SELECT subid,title , ltpsc , credit from subcatalogue WHERE pc='Y'"""
            res_w = cur.execute(query)
            res_w = res_w.fetchall()
            for row in res_w:
                query = """INSERT INTO runningcourses values (?,?,?,?)"""
                query_fid = f"""SELECT fid from offered where subid='{row[0]}'"""
                res_fid = cur.execute(query_fid)
                res_fid = res_fid.fetchone()
                val = (row[0], rid, '0', res_fid[0])
                cur.execute(query,val)
                cre = row[3]
                c = c - int(cre)
            quer_up  = f"""UPDATE currentstudying set creditreq='{c}' where rid ='{rid}'"""
            cur.execute(quer_up)
            con.commit()
        sem_id = sem
    else:
        sem_id = res_2[0]
    course_id = getCourseid(rid)
    choice = 'y'
    while choice == 'y' or choice == 'Y':
        print("1.ADD OR REMOVE Courses \n2.CHECK grades \n3.Graduation check\n4.Compute CGPA\n5.Previous Scores\n6.MTP info\n7.Logout")
        choose = input()
        if choose in ["1", "2", "3", "4", "5", "6", "7"]:
            if choose == "6":
                mtpinfo(rid)
            if choose == "7":
                login.logout(usertype)
                return
            if choose == "4":
                compute_CGPA(rid)
            if choose == "3":
                graduation_check(rid)
            if choose == "5":
                previous_performance(rid)
            if choose == "1":
                    sem_id_c = get_current_sem(rid)
                    if sem_id_c == 5:
                        print("Not able to check you are passed")
                    else:
                        query = f"""SELECT T1.subid , T2.title, T2.credit, T3.fname FROM runningcourses as T1 ,subcatalogue as T2,faculty as T3 WHERE T1.subid = T2.subid AND T1.fid = T3.fid AND regid = '{rid}'"""
                        res = cur.execute(query)
                        res = res.fetchall()
                        if res.__len__ != 0:
                            print("chosed courses are :")
                            table = []
                            for row in res:
                                list = [row[0],row[1],row[2],row[3]]
                                table.append(list)
                            print(tabulate(table, headers=["Course ID", "Course Title", "Credit", "Instrutor"],tablefmt="fancy_outline"))
                        else:
                            print("No courses are taken currently\n")
                        query = f"""SELECT creditreq FROM currentstudying WHERE rid = '{rid}'"""
                        res = cur.execute(query)
                        res = res.fetchone()
                        credits = int(res[0])
                        option = input("1.Add a course \n2.Remove a course\n")
                        if option in ["1", "2"]:
                            if option == "1":
                                print("Following courses are availabe to choose from ")
                                query = f"""SELECT T2.subid, T2.title, T2.credit , T5.fname FROM offered as T1 ,subcatalogue as T2 ,faculty as T5  WHERE T1.subid = T2.subid AND T2.pc='N' and T1.fid = T5.fid AND T2.courseid = '{course_id}' AND NOT EXISTS(SELECT subid FROM runningcourses as T3 WHERE T3.subid = T2.subid AND T3.regid = '{rid}') """
                                res = cur.execute(query)
                                res = res.fetchall()
                                table = []
                                for row in res:
                                    list = [row[0],row[1],row[2],row[3]]
                                    table.append(list)
                                print(tabulate(table, headers=["Course ID", "Course Title", "Credit", "Instrutor"],tablefmt="fancy_outline"))
                                code = input(
                                    "Please enter course code you want to register from above list of courses : ")
                                code = code.upper()
                                query = f"""SELECT subid ,fid ,cgpa from offered where subid = '{code}'"""
                                res = cur.execute(query)
                                res = res.fetchone()
                                if res != None:
                                    subid = res[0]
                                    fid = res[1]
                                    flag = 1
                                    flag_2 = 1
                                    query_pre = f"""SELECT preid from subcatalogue where subid = '{subid}'"""
                                    res_pre = cur.execute(query_pre)
                                    res_pre = res_pre.fetchone()
                                    query_pre = f"""SELECT pre1,pre2,pre3 from prerequisite where preid='{int(res_pre[0])}'"""
                                    res_pre = cur.execute(query_pre)
                                    res_pre = res_pre.fetchone()
                                    if res_pre != None:
                                        sub = ''
                                        list = [res_pre[0], res_pre[1], res_pre[2]]
                                        for i in list:
                                            if i != 'None':
                                                query_sub = f"""SELECT subid from prerecord where subid = '{i}' and rid = '{rid}'"""
                                                res_sub = cur.execute(query_sub)
                                                res_sub = res_sub.fetchone()
                                                if res_sub == None:
                                                    sub = i
                                                    flag_2 = 0
                                                    break
                                    cgpa = int(get_CGPA(rid, "1"))
                                    cgpa_fid = res[2]
                                    if cgpa > cgpa_fid:
                                        flag = 1
                                    else:
                                        flag = 0
                                    if flag != 0 and flag_2 != 0:
                                        query = f"""SELECT credit from subcatalogue WHERE subid = '{code}'"""
                                        res = cur.execute(query)
                                        res = res.fetchone()
                                        temp_credits = int(res[0])
                                        if credits >= temp_credits:
                                            cre = credits - temp_credits
                                            query = f"""INSERT INTO runningcourses values(?,?,?,?)"""
                                            query_2 = f"""UPDATE currentstudying SET creditreq = '{cre}' WHERE rid = '{rid}'"""
                                            val = (subid, rid, "0", fid)
                                            try:
                                                cur.execute(query, val)
                                                cur.execute(query_2)
                                                print("Course added sucessfully")
                                            except:
                                                print(
                                                    "Some problem in adding the course please try later")
                                        else:
                                            print(f"Credit limit reached remainin credit left : ({credits})")
                                    else:
                                        if flag == 0:
                                            print("CGPA is low you are not eligible for this course")
                                        if flag_2 == 0:
                                            print(f"Does not clear the pre requisite : {i}")
                                else:
                                    print("Wrong subject code")
                            if option == "2":
                                delete_code = input("Enter course Name to be removed : ")
                                delete_code = delete_code.upper()
                                query = f"""SELECT subid ,fid from offered where subid = '{delete_code}'"""
                                res = cur.execute(query)
                                res = res.fetchone()
                                query_s = f"""SELECT pc from subcatalogue WHERE subid = '{delete_code}'"""
                                res_s = cur.execute(query_s)
                                res_s = res_s.fetchone()
                                if res != None:
                                    if res_s[0] == 'Y':
                                        print("Can't be removed it is a core course you fool")
                                    else:
                                        query = f"""SELECT credit from subcatalogue WHERE subid = '{delete_code}'"""
                                        res = cur.execute(query)
                                        res = res.fetchone()
                                        temp_credits = int(res[0])
                                        cre = credits + temp_credits
                                        query = f"""DELETE FROM runningcourses WHERE regid = '{rid}' AND subid = '{delete_code}' """
                                        query_2 = f"""UPDATE currentstudying SET creditreq = '{cre}' WHERE rid = '{rid}'"""
                                        try:
                                            cur.execute(query)
                                            cur.execute(query_2)
                                            print("Course removed sucessfully")
                                        except:
                                            print(
                                                "Some problem in removing the course please try later")
                                else:
                                    print("wrong course code")
                        else:
                            print("wrong choice")

            if choose == "2":
                if sem_id == 5:
                    print("Not able to check you are passed")
                else:
                    query = f"""SELECT T1.subid , T1.grades, T3.fname, T2.title from runningcourses  as T1 , subcatalogue as T2 , faculty as T3  WHERE T1.subid = T2.subid AND T1.fid = T3.fid AND  regid = '{rid}'"""
                    temp_res = cur.execute(query)
                    temp_res = temp_res.fetchall()
                    if temp_res != None:
                        table = []
                        for row in temp_res:
                            list = [row[0], row[1], row[3], row[2]]
                            table.append(list)
                        print(tabulate(table, headers=["Course ID", "Grades", "Title ", "Instructor"], tablefmt="fancy_outline"))
                    else:
                        print("You are not enrolled in any course")
        choice = input("Do you want to continue [Y/N]: ")

        con.commit()
        if choice in ['y', 'Y']:
            os.system("clear")
        else:
            login.logout(usertype)
            print("Logging out")
            time.sleep(1)
            con.close()



