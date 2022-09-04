import chunk
# from msilib.schema import Font
import PyQt5
from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)

import sys


class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)
        
        keylayout = QVBoxLayout()
        self.l1 = QLabel("原曲キー: +-0")
        self.l1.setFont(QtGui.QFont("Verdana", 20,QtGui.QFont.Black))
        self.l1.setAlignment(Qt.AlignCenter)
        keylayout.addWidget(self.l1)
        
        self.sl = QSlider(Qt.Horizontal)
        self.sl.setMinimum(-6)
        self.sl.setMaximum(6)
        self.sl.setValue(0)
        self.sl.setTickPosition(QSlider.TicksBelow)
        self.sl.setTickInterval(2)
        
        keylayout.addWidget(self.sl)
        # keylayout.addStretch(0.1)
        self.sl.valueChanged.connect(self.valuechange)
        
        self.createSettiongButton()
        self.createStartButton()

     
        mainLayout = QGridLayout()
        
        mainLayout.addLayout(keylayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.SettiongButton, 0, 2)
        mainLayout.addLayout(self.startlayout, 1, 0, 1, 3)
        
        # mainLayout.setRowStretch(1, 1)
        # mainLayout.setRowStretch(2, 1)
        # mainLayout.setColumnStretch(0, 1)
        # mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)
        self.setWindowTitle("KeyAdjuster")
        self.setGeometry(100,100,450,250)
        # self.changeStyle('Fusion')
    
    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    def changePalette(self):
            QApplication.setPalette(QApplication.style().standardPalette())
  
             
    def valuechange(self):
        key = self.sl.value()
        if key>0:
            self.l1.setText('原曲キー: +'+ str(key))
        elif key <0:
            self.l1.setText('原曲キー: '+str(key))
        else:
            self.l1.setText('原曲キー: +-0')  
            

    def createStartButton(self):
        self.StartButton = QGroupBox()

        self.togglePushButton = QPushButton("START")
        self.togglePushButton.setCheckable(True)
        self.togglePushButton.setChecked(False)
        
        # self.togglePushButton.setIcon(QIcon(QPixmap("python.gif")))
        # def system_stop(self):
        #     self.SettiongButton.setDisabled() 
        
        self.togglePushButton.toggled.connect(self.SettiongButton.setDisabled)
        self.togglePushButton.toggled.connect(lambda:(self.togglePushButton.setText('STOP')) if (self.togglePushButton.isChecked()) else (self.togglePushButton.setText('START')))
        

        self.startlayout = QVBoxLayout()
        self.startlayout.addStretch(0.5)
        self.startlayout.addWidget(self.togglePushButton)
        self.startlayout.addStretch(0.5)
        # self.StartButton.setLayout(layout)   

    def createSettiongButton(self):
        
        input_list = ['a','b','c']
        output_list = ['d','e','f']
        samplingRate_list = ['44800','44100']
        chunk_list = ['20','50']
        
        # self.SettiongButton = QGroupBox("機器設定")
        self.SettiongButton = QGroupBox()
        self.SettiongButton.setAlignment(Qt.AlignCenter)
        # self.setFont(QtGui.QFont("Verdana", 5,QtGui.QFont.Black))

        def input_change():
            print(inputComboBox.currentText())
        def output_change():
            print(outputComboBox.currentText())
        def samplingRate_change():
            print(samplingRateComboBox.currentText())
        def chunk_change():
            print(chunkComboBox.currentText())
          
          
        # INPUT  
        inputComboBox = QComboBox()
        inputComboBox.addItems(input_list)
        inputComboBox.activated.connect(input_change)
        
        inputLabel = QLabel("Input:")
        inputLabel.setBuddy(inputComboBox)
        inputlayout = QHBoxLayout()
        inputlayout.addWidget(inputLabel)
        inputlayout.addWidget(inputComboBox)
        
        
        # OUTPUT
        outputComboBox = QComboBox()
        outputComboBox.addItems(output_list)
        outputComboBox.activated.connect(output_change)
        
        outputLabel = QLabel("Output:")
        outputLabel.setBuddy(outputComboBox)
        outputlayout = QHBoxLayout()
        outputlayout.addWidget(outputLabel)
        outputlayout.addWidget(outputComboBox)

        #SAMPLING RATE
        samplingRateComboBox = QComboBox()
        samplingRateComboBox.addItems(samplingRate_list)
        samplingRateComboBox.activated.connect(samplingRate_change)
        
        samplingRateLabel = QLabel("Samplingrate:")
        samplingRateLabel.setBuddy(samplingRateComboBox)
        samplingRateLayout = QHBoxLayout()
        samplingRateLayout.addWidget(samplingRateLabel)
        samplingRateLayout.addWidget(samplingRateComboBox)
        
        
        # CHUNK
        chunkComboBox = QComboBox()
        chunkComboBox.addItems(chunk_list)
        chunkComboBox.activated.connect(chunk_change)
        
        chunkLabel = QLabel("Chunk:")
        chunkLabel.setBuddy(chunkComboBox)
        chunkLayout = QHBoxLayout()
        chunkLayout.addWidget(chunkLabel)
        chunkLayout.addWidget(chunkComboBox)
        

        
        parentLayout = QVBoxLayout()
        parentLayout.addLayout(inputlayout)
        parentLayout.addLayout(outputlayout)
        parentLayout.addLayout(samplingRateLayout)
        parentLayout.addLayout(chunkLayout)
        self.SettiongButton.setLayout(parentLayout)

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec())
