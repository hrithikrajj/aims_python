#ifndef STUMENU_H
#define STUMENU_H
#include"login.h"

#include <QMainWindow>

namespace Ui {
class StuMenu;
}

class StuMenu : public QMainWindow
{
    Q_OBJECT

public:
    explicit StuMenu(QWidget *parent = nullptr);
    ~StuMenu();

private slots:
    void on_pushButton_5_clicked();

private:
    Ui::StuMenu *ui;
};

#endif // STUMENU_H
