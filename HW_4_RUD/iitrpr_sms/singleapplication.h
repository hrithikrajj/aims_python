#ifndef SINGLEAPPLICATION_H
#define SINGLEAPPLICATION_H

#include <QApplication>

class QSharedMemory;

class SingleApplication:public QApplication{

    Q_OBJECT

public:
    SingleApplication(int &argc, char **argv);
    ~SingleApplication();

    bool lock();
    void unlock();

private:
    QSharedMemory *_singular;
};

#endif //SINGLEAPPLICATION_H
