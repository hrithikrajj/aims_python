#include <QtCore/QSharedMemory>

#include "singleapplication.h"
#include"globals.h"
SingleApplication::SingleApplication(int &argc, char **argv):QApplication(argc, argv, true)
{
    _singular = new QSharedMemory(APP_NAME, this);
}

SingleApplication::~SingleApplication()
{
    if(_singular->isAttached())
        _singular->detach();
}

bool SingleApplication::lock()
{
    if(_singular->attach(QSharedMemory::ReadOnly)){
        _singular->detach();
        //return false;
    }

    if(_singular->create(1))
        return true;
    else
    return false;
}

void SingleApplication::unlock()
{
    if(_singular->isAttached())
        _singular->detach();
}
