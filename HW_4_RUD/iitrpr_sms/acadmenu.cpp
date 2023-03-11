#include "acadmenu.h"
#include "ui_acadmenu.h"
#include "globals.h"
#include<QMessageBox>

AcadMenu::AcadMenu(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::AcadMenu)
{
    ui->setupUi(this);
    this->setFixedSize(this->geometry().width(),this->geometry().height());
    login obj_login;
    // obj_login = new login();
    if(!obj_login.conOpen())
        ui->label->setText("Failed to open db!!");
    else
        ui->label->setText("DB Connected!");
    obj_login.conClose();

}

AcadMenu::~AcadMenu()
{
    delete ui;
}

void AcadMenu::on_pushButton_12_clicked()
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
