import PyQt5
from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)
import sys
import subprocess

class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        self.originalPalette = QApplication.palette()

        styleComboBox = QComboBox()
        styleComboBox.addItems(QStyleFactory.keys())

        styleLabel = QLabel("&Style:")
        styleLabel.setBuddy(styleComboBox)

        self.useStylePaletteCheckBox = QCheckBox("&Use style's standard palette")
        self.useStylePaletteCheckBox.setChecked(True)

        disableWidgetsCheckBox = QCheckBox("&Disable widgets")

        self.createTopRightGroupBox()

        styleComboBox.activated[str].connect(self.changeStyle)
        self.useStylePaletteCheckBox.toggled.connect(self.changePalette)
        disableWidgetsCheckBox.toggled.connect(self.topRightGroupBox.setDisabled)

        topLayout = QHBoxLayout()
        topLayout.addWidget(styleLabel)
        topLayout.addWidget(styleComboBox)
        topLayout.addStretch(1)
        topLayout.addWidget(self.useStylePaletteCheckBox)
        topLayout.addWidget(disableWidgetsCheckBox)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.topRightGroupBox, 1, 0)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("Styles")
        self.changeStyle('Windows')

        self.play_flag = False
        self.proc: subprocess.Popen
    
    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    def changePalette(self):
        if (self.useStylePaletteCheckBox.isChecked()):
            QApplication.setPalette(QApplication.style().standardPalette())
        else:
            QApplication.setPalette(self.originalPalette)
    
    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox("Group 2")

        defaultPushButton = QPushButton("Play Button")
        defaultPushButton.setDefault(False)
        defaultPushButton.clicked.connect(self.play)

        togglePushButton = QPushButton("Stop Button")
        togglePushButton.clicked.connect(self.stop)

        layout = QVBoxLayout()
        layout.addWidget(defaultPushButton)
        layout.addWidget(togglePushButton)
        layout.addStretch(1)
        self.topRightGroupBox.setLayout(layout)
    
    def play(self):
        if not self.play_flag:
            self.proc = subprocess.Popen(["python", "realtime_nonblocking.py"]) #Popenならサブプロセス中も、次のメインプロセスが実行される
        self.play_flag = True

    def stop(self):
        if self.play_flag:
            self.proc.kill()
        self.play_flag = False

def exit():
    app.exec()
    gallery.proc.kill()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(exit())

