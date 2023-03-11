#ifndef ACADMENU_H
#define ACADMENU_H
#include"login.h"
#include <QMainWindow>

namespace Ui {
class AcadMenu;
}

class AcadMenu : public QMainWindow
{
    Q_OBJECT

public:
    explicit AcadMenu(QWidget *parent = nullptr);
    ~AcadMenu();

private slots:
    void on_pushButton_12_clicked();

private:
    Ui::AcadMenu *ui;
};

#endif // ACADMENU_H
