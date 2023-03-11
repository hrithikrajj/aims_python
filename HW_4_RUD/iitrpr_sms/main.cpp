#include <QApplication>
#include "login.h"
#include"globals.h"
#include "singleapplication.h"
#include <QMessageBox>


int main(int argc, char *argv[])
{
    SingleApplication a(argc, argv);
    a.setAttribute(Qt::AA_EnableHighDpiScaling);
    a.setOrganizationName(ORG_NAME);
    a.setApplicationName(APP_NAME);

    if(!a.lock()){
        qDebug() << "Application allready running";
        QMessageBox::critical(nullptr, "Error", "Application is already running. Please close the running process and try again.");
        exit(1);
    }
   // QApplication a(argc, argv);
    login w;
    w.show();
    int ret=a.exec();

    return ret;
}
