import signal
import sys

import PyQt5

import key_adjuster_gui


if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(PyQt5.QtGui.QIcon('icons/icon_b.png'))
    mainWidget = key_adjuster_gui.MainWidget()
    mainWidget.show()
    signal.signal(signal.SIGINT, lambda sig,_: app.quit())
    sys.exit(mainWidget.exec(app))
