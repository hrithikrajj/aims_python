#!/bin/sh
rm -f test.db
adm="'admin','admin'"
# aa="'c','d'"
# while IFS= read -r line
# do
#     # echo $line |awk '{printf "\""$1 ",\""$2 }' 
# #   echo "\"'"$line","
# done < stu.txt


sqlite3 test.db <<EOF
# create table n (id INTEGER PRIMARY KEY,f TEXT,l TEXT);
# insert into n (f,l) values ('john','smith');
# select * from n;

CREATE TABLE student_credentials(username  ,password , primary key (username));
CREATE TABLE faculty_credentials(username ,password ,primary key (username));
CREATE TABLE acad_credentials(username ,password ,primary key (username));
CREATE TABLE course(courseid,coursname, primary key(courseid));
CREATE TABLE registration(rid,username,name,courseid, primary key(rid),foreign key(courseid) references course);
CREATE TABLE prerequisite (preid INTEGER,pre1,pre2,pre3,primary key (preid));
CREATE TABLE subcatalogue(preid, subid,title,courseid,ltpsc,semid,credit,pc, primary key (subid), foreign key(preid) references prerequisite,foreign key (courseid) references course );
CREATE TABLE prerecord(semid, rid,subid,grade, foreign key(rid) references registration , foreign key (subid) references subcatalogue);
CREATE TABLE currentstudying(rid,semid,cid,creditreq,foreign key (cid) references course , foreign key (rid) references registration );
CREATE TABLE faculty(fid,username, fname,primary key(fid));
CREATE TABLE constraints(consid,cons1,cons2, primary key(consid));
CREATE TABLE offered(fid, subid,consid,foreign key (fid) references faculty, foreign key (subid) references subcatalogue , foreign key (consid) references constraints);
CREATE TABLE runningcourses(subid, regid,grades,fid, foreign key (fid) references faculty,foreign key (subid) references subcatalogue,foreign key(regid) references registration) ;
CREATE TABLE sessiontable(sessionid INTEGER , username ,usertype , primary key (sessionid)) ;
CREATE TABLE semresult(semID, regid,creditsearned,foreign key (regid) references registration);

# INSERT INTO student_credentials(username  ,password) values ('a', 'b');
# INSERT INTO student_credentials(username  ,password) values ($aa);



EOF
    
sqlite3 test.db "INSERT INTO student_credentials(username  ,password) values ($adm);"
sqlite3 test.db "INSERT INTO acad_credentials(username  ,password) values ($adm);"
sqlite3 test.db "INSERT INTO faculty_credentials(username  ,password) values ($adm);"

while IFS= read -r line
do
    sqlite3 test.db "INSERT INTO student_credentials(username  ,password) values ($line);"
done < 2020pwd.txt

while IFS= read -r line
do
    sqlite3 test.db "INSERT INTO student_credentials(username  ,password) values ($line);"
done < 2021pwd.txt

while IFS= read -r line
do
    sqlite3 test.db "INSERT INTO student_credentials(username  ,password) values ($line);"
done < 2022pwd.txt

while IFS= read -r line
do
    sqlite3 test.db "INSERT INTO registration(rid,username,name,courseid) values ($line);"
done < 2020reg.txt

while IFS= read -r line
do
    sqlite3 test.db "INSERT INTO registration(rid,username,name,courseid) values ($line);"
done < 2021reg.txt

while IFS= read -r line
do
    sqlite3 test.db "INSERT INTO registration(rid,username,name,courseid) values ($line);"
done < 2022reg.txt

while IFS= read -r line
do
    sqlite3 test.db "INSERT INTO subcatalogue(preid, subid,title,courseid,ltpsc,semid,credit,pc) values ($line);"
done < subcatcomma.txt

while IFS= read -r line
do
    sqlite3 test.db "INSERT INTO faculty(fid,username, fname) values ($line);"
done < facultycomma.txt

while IFS= read -r line
do
    sqlite3 test.db "INSERT INTO faculty_credentials(username ,password) values ($line);"
done < facultypwd.txt

while IFS= read -r line
do
    sqlite3 test.db "INSERT INTO prerecord(semid, rid,subid,grade) values ($line);"
done < prerec.txt

while IFS= read -r line
do
    sqlite3 test.db "INSERT INTO semresult(semID, regid,creditsearned) values ($line);"
done < semres.txt
