import sys
import os

import PyQt5

import key_adjuster_gui


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


if __name__ == "__main__":
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(PyQt5.QtGui.QIcon(resource_path("key_adjuster.ico")))
    mainWidget = key_adjuster_gui.MainWidget()
    mainWidget.show()
    sys.exit(mainWidget.exec(app))
