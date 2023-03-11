#include "login.h"
#include "ui_login.h"
#include"globals.h"
#include"stumainwindow.h"
#include"stumenu.h"
#include"facmenu.h"
#include"acadmenu.h"
#include<QMessageBox>
QString CURR_USER_NAME;
QString CURR_UTYPE;
QString CURR_SESSION_ID="";

login::login(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::login)
{
    ui->setupUi(this);
    this->setFixedSize(this->geometry().width(),this->geometry().height());

    QPixmap bkgnd("../iitrpr_sms/images/login_bg.jpg");
    bkgnd = bkgnd.scaled(this->size(), Qt::IgnoreAspectRatio);
    QPalette palette;
    palette.setBrush(QPalette::Background, bkgnd);
    this->setPalette(palette);

    //ui->comboBox->setIconSize((QSize(40,20)));
    ui->comboBox->addItem(QIcon("../iitrpr_sms/images/stu.jpg"),"Student");
    ui->comboBox->addItem(QIcon("../iitrpr_sms/images/fac.jpg"),"Faculty");
    ui->comboBox->addItem(QIcon("../iitrpr_sms/images/acad.jpg"),"Academics");
   // setIconSize
    if(!conOpen())
        ui->label->setText("Failed to open db!!");
    else
        ui->label->setText("DB connected!");
    conClose();

    //       QComboBox *comboBox = new QComboBox;
    //       ui->
    //           ui->comboBox->addItem(tr("item 1"));
    //           comboBox->addItem(tr("item 2"));
    //           comboBox->addItem(tr("item 3"));

    //           QComboBox *iconComboBox = new QComboBox;
    //           iconComboBox->addItem(QIcon(":/images/bad.svg"), tr("Bad"));
    //           iconComboBox->addItem(QIcon(":/images/heart.svg"), tr("Heart"));
    //           iconComboBox->addItem(QIcon(":/images/trash.svg"), tr("Trash"));
}

login::~login()
{
    delete ui;
}


void login::on_pushButton_clicked()
{
    QString uname, tmppasswd, utype;
    uname=ui->le_uname->text();
    tmppasswd=ui->le_passwd->text();
    utype=ui->comboBox->currentText().toLower();
    CURR_USER_NAME=uname;
    CURR_UTYPE=utype;

    QByteArray passwd = QCryptographicHash::hash(tmppasswd.toLocal8Bit(), QCryptographicHash::Sha3_512);
    qDebug() << "pwdhash="  << passwd;

    if(!conOpen())
    {
        QMessageBox::warning(this, "Database", "Failed to open db!!");
        return;
    }
    QSqlQuery query;
//    query.prepare("INSERT INTO student_credentials (username,password) VALUES (:username,:password)");
//    query.bindValue(":username", CURR_USER_NAME);
//    query.bindValue(":password", passwd);
//    if(!query.exec())
//    {
//        QMessageBox::critical(this,"Error::",query.lastError().text());
//    }

    if(utype=="student")
    {
        query.prepare("select * from student_credentials where username='"+uname+"' and password='"+passwd+"'");
    }
    else if(utype=="faculty")
    {
        query.prepare("select * from faculty_credentials where username='"+uname+"' and password='"+passwd+"'");
    }
    else if(utype=="academics")
    {
        query.prepare("select * from acad_credentials where username='"+uname+"' and password='"+passwd+"'");
    }
    if(query.exec())
    {
        int ucount=0;
        while(query.next())
        {
            ucount++;
        }
        if(ucount==1)
        {
            QString sid_suffix = QDateTime::currentDateTime().toString("ddhhmmsszzz");
            QString sid=CURR_USER_NAME+sid_suffix;
            QSqlQuery query1;
            bool new_sid_flag=false;
            int scount=0;
            query1.prepare("select * from sessiontable where username='"+CURR_USER_NAME +"' and usertype='"+utype+"'");
            if(query1.exec())
            {
                while(query1.next())
                {
                    scount++;
                }
            }
            else
                QMessageBox::critical(this,"Error::",query1.lastError().text());

            if(scount!=0)
            {
                QMessageBox::StandardButton reply;
                reply = QMessageBox::question(this, "Session", "Session Id for "+CURR_USER_NAME+" "
                                                                                                "already exist!!It will be deleted to re-login. Want to continue?",
                                              QMessageBox::Yes|QMessageBox::Cancel);
                if (reply == QMessageBox::Yes)
                {
                    //QApplication::quit();
                    new_sid_flag=true;
                    query1.prepare("DELETE FROM sessiontable");
                    if(!query1.exec())
                    {
                        QMessageBox::critical(this,"Error::",query1.lastError().text());
                    }
                }
                else
                {
                    return;
                }
            }
            if(scount==0||new_sid_flag==true)
            {
                query1.prepare("INSERT INTO sessiontable (sessionid,username,usertype) VALUES (:sessionid,:username,:usertype)");
                query1.bindValue(":sessionid", sid);
                query1.bindValue(":username", CURR_USER_NAME);
                query1.bindValue(":usertype", utype);

                if(!query1.exec())
                {
                    QMessageBox::critical(this,"Error::",query1.lastError().text());
                }
                CURR_SESSION_ID=sid;
            }

            studb.close();
            ui->label->setText("username and password are correct!");
            //            StuMainWindow *obj_stumain;
            //            obj_stumain = new StuMainWindow(this);
            //            obj_stumain->show();


            if(utype=="student")
            {
                StuMenu *obj_stu;
                obj_stu = new StuMenu(this);
                this->hide();
                obj_stu->show();            }
            else if(utype=="faculty")
            {
                FacMenu *obj_fac;
                obj_fac = new FacMenu(this);
                this->hide();
                obj_fac->show();
            }
            else if(utype=="academics")
            {
                AcadMenu *obj_acad;
                obj_acad = new AcadMenu(this);
                this->hide();
                obj_acad->show();
            }
        }
        if(ucount>1)
        {
            QMessageBox::critical(this,"Duplicate User", "Duplicate Users are present in database!!!");

            ui->label->setText("Duplicate username and password!!");
        }
        if(ucount<1)
        {
            QMessageBox::critical(this,"Authentication Failed", "Username and password did not match!! Please retry again!!");
            ui->label->setText("Username and password did not match!! Please retry again!!");
        }
    }
    conClose();
}
