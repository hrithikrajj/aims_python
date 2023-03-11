#include "stumainwindow.h"
#include "ui_stumainwindow.h"
#include "globals.h"
#include<QMessageBox>
// QString CURR_USER_NAME;

StuMainWindow::StuMainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::StuMainWindow)
{
    ui->setupUi(this);
    this->setFixedSize(this->geometry().width(),this->geometry().height());
    login obj_login;
    // obj_login = new login();
    if(!obj_login.conOpen())
        ui->label->setText("Failed to open db!!");
    else
        ui->label->setText("connected");


   QSqlQuery query;
   query.prepare("select * from studentinfo where username='"+CURR_USER_NAME +"'");

   if(query.exec())
   {
       while(query.next())
       {
           ui->le_entryid->setText((query.value(0).toString()));
           ui->le_name->setText((query.value(1).toString()));
           ui->le_sname->setText((query.value(2).toString()));
           ui->le_age->setText((query.value(3).toString()));
           ui->le_uname->setText((query.value(4).toString()));
           ui->le_passwd->setText((query.value(5).toString()));
           ui->le_utype->setText((query.value(6).toString()));

           //qDebug() << CURR_USER_NAME ;

       }
   }
   obj_login.conClose();

}

StuMainWindow::~StuMainWindow()
{
    delete ui;
}

void StuMainWindow::on_pushButton_clicked()
{

    //         "entryid"
    //         "name"
    //         "surname"
    //         "age"
    //         "username"
    //         "password"
    //         "usertype"

    QString  name, surname,  username, password, usertype;
//     int entryid,age ;
     QString entryid,age;

     entryid=ui->le_entryid->text();
     name=ui->le_name->text();
    surname= ui->le_sname->text();
    age = ui->le_age->text();
    username=ui->le_uname->text();
    password= ui->le_passwd->text();
     usertype=ui->le_utype->text();

     qDebug() <<entryid<< name<< surname<< age<< username<< password<< usertype;
     login obj_login;
    obj_login.conOpen();
    QSqlQuery query;
    query.prepare("update studentinfo set entryid='"+entryid+"',"
                                          " name='"+name+"',"
                                          " surname='"+surname+"',"
                                          " age='"+age+"',"
                                          " username='"+username+"',"
                                          " password='"+password+"',"
                                          " usertype='"+usertype+"'"
                                          " where username='"+CURR_USER_NAME+"' ");


    if(query.exec())
    {

    //QMessageBox::information(this,"Update", "Updated!!!");
    on_pushButton_2_clicked();
    }
    else
    {
        QMessageBox::critical(this,"Error::",query.lastError().text());

    }
    obj_login.conClose();

}

void StuMainWindow::on_pushButton_2_clicked()
{
    QSqlQueryModel *model = new QSqlQueryModel;

    login obj_login;
   obj_login.conOpen();
   QSqlQuery *query= new QSqlQuery(obj_login.studb);
   query->prepare("select * from studentinfo ");


   if(query->exec())
   {
//       ui->tableView->setVisible(false);

    model->setQuery(*query);

//    ui->tableView->verticalHeader()->setStretchLastSection(true);
//    ui->tableView->resizeColumnsToContents();
//    ui->tableView->resizeRowsToContents();

//ui->tableView->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);
    ui->tableView->setModel(model);
//    ui->tableView->resizeColumnsToContents();
//    ui->tableView->resizeRowsToContents();


//    ui->tableView->setVisible(true);

   //QMessageBox::information(this,"Load", "Loaded!!!");
   }
   else
   {
       QMessageBox::critical(this,"Error::",query->lastError().text());

   }
   obj_login.conClose();

}
