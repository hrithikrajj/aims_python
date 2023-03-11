#ifndef LOGIN_H
#define LOGIN_H

#include <QMainWindow>
#include<QtSql>
#include<QFileInfo>
//#include"globals.h"


QT_BEGIN_NAMESPACE
namespace Ui { class login; }
QT_END_NAMESPACE

class login : public QMainWindow
{
    Q_OBJECT
public:
    QSqlDatabase studb;

    void conClose()
    {
        studb.close();
        studb.removeDatabase(QSqlDatabase::defaultConnection);
        QSqlDatabase::addDatabase("QSQLITE");
    }
    bool conOpen()
    {

    studb=QSqlDatabase::addDatabase("QSQLITE");
    studb.setDatabaseName("aims.db");

    if(!studb.open())
        //ui->label->setText("Failed to open db!!");
    return false;
    else
//        ui->label->setText("connected");
    return true;
    }
public:
    login(QWidget *parent = nullptr);
    ~login();

private slots:
    void on_pushButton_clicked();

private:
    Ui::login *ui;
    //StuMainWindow *obj_stu;

};
#endif // LOGIN_H
