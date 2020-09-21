
import sys
#从qt.py文件内调用模块
from qt import Ui_Form
from PyQt5 import QtWidgets

class myWin(QtWidgets.QWidget, Ui_Form):

    def __init__(self):
        super(myWin, self).__init__()
        self.setupUi(self)

if __name__ == '__main__':

    app=QtWidgets.QApplication(sys.argv)
    Widget=myWin()
    Widget.show()
    sys.exit(app.exec_())

