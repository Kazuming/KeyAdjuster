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
import threading
import pyaudio
from thread_pyaudio import ThreadPyaudio


class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)
        
        keyLayout = QVBoxLayout()
        self.l1 = QLabel("原曲キー: +-0")
        self.l1.setFont(QtGui.QFont("Verdana", 20,QtGui.QFont.Black))
        self.l1.setAlignment(Qt.AlignCenter)
        keyLayout.addWidget(self.l1)
        
        self.sl = QSlider(Qt.Horizontal)
        self.sl.setMinimum(-6)
        self.sl.setMaximum(6)
        self.sl.setValue(0)
        self.sl.setTickPosition(QSlider.TicksBelow)
        self.sl.setTickInterval(1)
        
        keyLayout.addWidget(self.sl)
        # keyLayout.addStretch(0.1)
        self.sl.valueChanged.connect(self.valuechange)
        
        self.createSettiongButton()
        self.createStartButton()


        mainLayout = QGridLayout()
        
        mainLayout.addLayout(keyLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.SettiongButton, 0, 2)
        mainLayout.addLayout(self.startLayout, 1, 0, 1, 3)
        
        # mainLayout.setRowStretch(1, 1)
        # mainLayout.setRowStretch(2, 1)
        # mainLayout.setColumnStretch(0, 1)
        # mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)
        self.setWindowTitle("KeyAdjuster")
        self.setGeometry(100,100,700,250)
        # self.changeStyle('Fusion')


        # ThreadPyaudio Props
        self.play_flag = False
        self.sampling_rate: int
        self.n: int
        # 複数のマイク/スピーカーがある場合はここでINDEXを設定する
        self.input_device_index: int
        self.output_device_index: int
        # キー
        self.key = self.sl.value()
        self.thread_pyaudio: ThreadPyaudio
        self._stop = threading.Event()
    
    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    def changePalette(self):
        QApplication.setPalette(QApplication.style().standardPalette())
  
             
    def valuechange(self):
        key = self.sl.value()
        self.key = key
        self.thread_pyaudio.key = key

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
        # self.togglePushButton.toggled.connect(lambda:(self.togglePushButton.setText('STOP')) if (self.togglePushButton.isChecked()) else (self.togglePushButton.setText('START')))
        self.togglePushButton.clicked.connect(self.changePlayStatus)

        self.startLayout = QVBoxLayout()
        self.startLayout.addStretch(0.5)
        self.startLayout.addWidget(self.togglePushButton)
        self.startLayout.addStretch(0.5)
        # self.StartButton.setLayout(layout)

    

    def createSettiongButton(self):
        p = pyaudio.PyAudio()

        input_device_list = {}
        output_device_list = {}

        # 複数のマイク/スピーカーがある場合、以下のfor文で確認して
        # input_device_indexとoutput_device_indexを書き換える
        for x in range(0, p.get_device_count()):
            if p.get_device_info_by_index(x)["maxInputChannels"] != 0:
                input_device_list[p.get_device_info_by_index(x)["name"]] = x
            if p.get_device_info_by_index(x)["maxOutputChannels"] != 0:
                output_device_list[p.get_device_info_by_index(x)["name"]] = x
        
        sampling_rate_list = ["44100", "44800"]
        chunkList = ["20", "50"]
        
        # self.SettiongButton = QGroupBox("機器設定")
        self.SettiongButton = QGroupBox()
        self.SettiongButton.setAlignment(Qt.AlignCenter)
        # self.setFont(QtGui.QFont("Verdana", 5,QtGui.QFont.Black))

        def inputChange():
            print(inputComboBox.currentText())
            self.input_device_index = input_device_list[inputComboBox.currentText()]
        def outputChange():
            print(outputComboBox.currentText())
            self.output_device_index = output_device_list[outputComboBox.currentText()]
        def samplingRateChange():
            print(samplingRateComboBox.currentText())
            self.sampling_rate = int(samplingRateComboBox.currentText())
        def chunkChange():
            print(chunkComboBox.currentText())
            self.n = int(chunkComboBox.currentText())
          
          
        # INPUT  
        inputComboBox = QComboBox()
        inputComboBox.addItems(input_device_list.keys())
        inputComboBox.activated.connect(inputChange)
        
        inputLabel = QLabel("Input Device:")
        inputLabel.setBuddy(inputComboBox)
        inputLayout = QHBoxLayout()
        inputLayout.addWidget(inputLabel)
        inputLayout.addWidget(inputComboBox)
        
        
        # OUTPUT
        outputComboBox = QComboBox()
        outputComboBox.addItems(output_device_list.keys())
        outputComboBox.activated.connect(outputChange)
        
        outputLabel = QLabel("Output Device:")
        outputLabel.setBuddy(outputComboBox)
        outputLayout = QHBoxLayout()
        outputLayout.addWidget(outputLabel)
        outputLayout.addWidget(outputComboBox)

        # SAMPLING RATE
        samplingRateComboBox = QComboBox()
        samplingRateComboBox.addItems(sampling_rate_list)
        samplingRateComboBox.activated.connect(samplingRateChange)
        
        samplingRateLabel = QLabel("Sampling Rate:")
        samplingRateLabel.setBuddy(samplingRateComboBox)
        samplingRateLayout = QHBoxLayout()
        samplingRateLayout.addWidget(samplingRateLabel)
        samplingRateLayout.addWidget(samplingRateComboBox)
        
        
        # CHUNK
        chunkComboBox = QComboBox()
        chunkComboBox.addItems(chunkList)
        chunkComboBox.activated.connect(chunkChange)
        
        chunkLabel = QLabel("Chunk(1024×N):")
        chunkLabel.setBuddy(chunkComboBox)
        chunkLayout = QHBoxLayout()
        chunkLayout.addWidget(chunkLabel)
        chunkLayout.addWidget(chunkComboBox)
        
        # init ThreadPyaudio Props
        self.input_device_index = input_device_list[inputComboBox.currentText()]
        self.output_device_index = output_device_list[outputComboBox.currentText()]
        self.sampling_rate = int(samplingRateComboBox.currentText())
        self.n = int(chunkComboBox.currentText())
        
        parentLayout = QVBoxLayout()
        parentLayout.addLayout(inputLayout)
        parentLayout.addLayout(outputLayout)
        parentLayout.addLayout(samplingRateLayout)
        parentLayout.addLayout(chunkLayout)
        self.SettiongButton.setLayout(parentLayout)
    
    def changePlayStatus(self):
        if self.togglePushButton.isChecked():
            self.play()
            self.togglePushButton.setText("STOP")
        else:
            self.stop()
            self.togglePushButton.setText("START")


    def play(self):
        if not self.play_flag:
            self.thread_pyaudio = ThreadPyaudio(self.sampling_rate, self.n, self.input_device_index, self.output_device_index, self.key)
            self.thread_pyaudio.start()
        self.play_flag = True

    def stop(self):
        if self.play_flag:
            # 実行中のスレッドを終了する
            self.thread_pyaudio.kill_flag = True
        self.play_flag = False


def exit():
    app.exec()
    gallery.stop()

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(exit())
