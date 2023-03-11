import sqlite3
import csv
import os
os.system("rm aims.db")
con = sqlite3.connect("aims.db")

cur = con.cursor()
cur.execute("CREATE TABLE student_credentials(username  ,password , primary key (username))")
cur.execute(" CREATE TABLE faculty_credentials(username ,password ,primary key (username))")
cur.execute(" CREATE TABLE acad_credentials(username ,password ,primary key (username))")
cur.execute(" CREATE TABLE course(courseid,coursname, primary key(courseid))")
cur.execute(" CREATE TABLE registration(rid,username,name,courseid, primary key(rid),foreign key(courseid) references course)")
cur.execute(" CREATE TABLE prerequisite (preid INTEGER,pre1,pre2,pre3,primary key (preid))")
cur.execute(" CREATE TABLE subcatalogue(preid, subid,title,courseid,ltpsc,semid,credit,pc, primary key (subid), foreign key(preid) references prerequisite,foreign key (courseid) references course )")
cur.execute("CREATE TABLE prerecord(semid, rid,subid,grade, foreign key(rid) references registration , foreign key (subid) references subcatalogue)")
cur.execute("CREATE TABLE currentstudying(rid,semid,cid,creditreq,foreign key (cid) references course , foreign key (rid) references registration )")
cur.execute("CREATE TABLE faculty(fid,username, fname,primary key(fid))")
cur.execute("CREATE TABLE offered(fid, subid,cgpa,foreign key (fid) references faculty, foreign key (subid) references subcatalogue  )")
cur.execute("CREATE TABLE runningcourses(subid, regid,grades,fid, foreign key (fid) references faculty,foreign key (subid) references subcatalogue,foreign key(regid) references registration) ")
cur.execute("CREATE TABLE sessiontable(sessionid , username ,usertype , primary key (sessionid)) ")
cur.execute("CREATE TABLE semresult(semID, regid,creditsearned,foreign key (regid) references registration)")
cur.execute("CREATE TABLE mtpinfo(rid,fid,title,description,foreign key (rid) references registration,foreign key (fid) references faculty)")
val = ("admin", "admin")
sql = "INSERT INTO student_credentials VALUES (?,?)"
cur.execute(sql, val)
sql = "INSERT INTO acad_credentials VALUES (?,?)"
cur.execute(sql, val)
sql = "INSERT INTO faculty_credentials VALUES (?,?)"
cur.execute(sql, val)
list = ['2020reg.txt', '2021reg.txt', '2022reg.txt' ]
for item in list :
    with open(item) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            query = f"""INSERT INTO registration values (?,?,?,?)"""
            val = (row[0].upper(), row[1].upper(), row[2], row[3].upper())
            cur.execute(query, val)

with open('subcatcomma.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            query = f"""INSERT INTO subcatalogue values (?,?,?,?,?,?,?,?)"""
            val = (row[0].upper(), row[1].upper(), row[2], row[3].upper(),row[4].upper(), row[5].upper(), row[6].upper(), row[7].upper())
            cur.execute(query, val)
with open('prerec.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        query = f"""INSERT INTO prerecord values (?,?,?,?)"""
        val = (row[0].upper(), row[1].upper(),row[2].upper(), row[3].upper())
        cur.execute(query, val)
with open('facultycomma.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        query = f"""INSERT INTO faculty values (?,?,?)"""
        val = (row[0].upper(), row[1].upper(), row[2])
        cur.execute(query, val)
with open('semend.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        query = f"""INSERT INTO semresult values (?,?,?)"""
        val = (row[0].upper(), row[1].upper(), row[2].upper())
        cur.execute(query, val)

with open('current.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        query = f"""INSERT INTO currentstudying values (?,?,?,?)"""
        val = (row[0].upper(), row[1].upper(), row[2].upper(),row[3].upper())
        cur.execute(query, val)
con.commit()
con.close()