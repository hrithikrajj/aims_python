#ifndef STUMAINWINDOW_H
#define STUMAINWINDOW_H
#include"login.h"


#include <QMainWindow>
namespace Ui {
class StuMainWindow;
}

class StuMainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit StuMainWindow(QWidget *parent = nullptr);
    ~StuMainWindow();

private slots:
    void on_pushButton_clicked();

    void on_pushButton_2_clicked();

private:
    Ui::StuMainWindow *ui;

};

#endif // STUMAINWINDOW_H
