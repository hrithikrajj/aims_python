#include "stumenu.h"
#include "ui_stumenu.h"
#include "globals.h"
#include<QMessageBox>

StuMenu::StuMenu(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::StuMenu)
{
    ui->setupUi(this);
    this->setFixedSize(this->geometry().width(),this->geometry().height());
    login obj_login;
    // obj_login = new login();
    if(!obj_login.conOpen())
        ui->label->setText("Failed to open db!!");
    else
        ui->label->setText("DB Connected!");

ui->label_2->setText("Welcome "+CURR_USER_NAME+"!");
//    QSqlQuery query;
//    query.prepare("select rid, name ,courseid FROM registration WHERE username='"+CURR_USER_NAME+"' ");


//    if(!query.exec())
//    {
//        QMessageBox::critical(this,"Error::",query.lastError().text());
//    }
//    else
//    {
//        int nameCol = query.record().indexOf("name");
//        while (query.next())
//        {
//            QString wlcm="Welcome "+query.value(nameCol).toString()+"!";
//            ui->label_2->setText(wlcm);
//        }
//    }

    obj_login.conClose();

}

StuMenu::~StuMenu()
{
    delete ui;
}

void StuMenu::on_pushButton_5_clicked()
{
    if(CURR_SESSION_ID.isNull())
        return;
    login *obj_login;
    obj_login = new login(this);

    obj_login->conOpen();
    QSqlQuery query;
    query.prepare("DELETE FROM sessiontable where usertype='"+CURR_UTYPE+"' ");
    if(!query.exec())
    {
        QMessageBox::critical(this,"Error::",query.lastError().text());
    }
    obj_login->conClose();
    this->close();

    obj_login->show();

}
