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
        self.sl.setTickInterval(1)
        
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
        self.setGeometry(100,100,600,250)
        # self.changeStyle('Fusion')


        # ThreadPyaudio Props
        self.play_flag = False
        self.SAMPLING_RATE: int
        self.N: int
        # 複数のマイク/スピーカーがある場合はここでINDEXを設定する
        self.INPUT_DEVICE_INDEX: int
        self.OUTPUT_DEVICE_INDEX: int
        # キー
        self.N_STEPS = self.sl.value()
        self.thread_pyaudio: ThreadPyaudio
        self._stop = threading.Event()
    
    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    def changePalette(self):
        QApplication.setPalette(QApplication.style().standardPalette())
  
             
    def valuechange(self):
        key = self.sl.value()
        self.N_STEPS = key
        self.thread_pyaudio.N_STEPS = key

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

        self.startlayout = QVBoxLayout()
        self.startlayout.addStretch(0.5)
        self.startlayout.addWidget(self.togglePushButton)
        self.startlayout.addStretch(0.5)
        # self.StartButton.setLayout(layout)

    

    def createSettiongButton(self):
        p = pyaudio.PyAudio()

        input_device_list = {}
        output_device_list = {}

        # 複数のマイク/スピーカーがある場合、以下のfor文で確認して
        # INPUT_DEVICE_INDEXとOUTPUT_DEVICE_INDEXを書き換える
        for x in range(0, p.get_device_count()):
            if p.get_device_info_by_index(x)["maxInputChannels"] != 0:
                input_device_list[p.get_device_info_by_index(x)["name"]] = x
            if p.get_device_info_by_index(x)["maxOutputChannels"] != 0:
                output_device_list[p.get_device_info_by_index(x)["name"]] = x
        
        sampling_rate_list = ["44100", "44800"]
        chunk_list = ["20", "50"]
        
        # self.SettiongButton = QGroupBox("機器設定")
        self.SettiongButton = QGroupBox()
        self.SettiongButton.setAlignment(Qt.AlignCenter)
        # self.setFont(QtGui.QFont("Verdana", 5,QtGui.QFont.Black))

        def inputChange():
            print(inputComboBox.currentText())
            self.INPUT_DEVICE_INDEX = input_device_list[inputComboBox.currentText()]
        def outputChange():
            print(outputComboBox.currentText())
            self.OUTPUT_DEVICE_INDEX = output_device_list[outputComboBox.currentText()]
        def samplingRateChange():
            print(samplingRateComboBox.currentText())
            self.SAMPLING_RATE = int(samplingRateComboBox.currentText())
        def chunkChange():
            print(chunkComboBox.currentText())
            self.N = int(chunkComboBox.currentText())
          
          
        # INPUT  
        inputComboBox = QComboBox()
        inputComboBox.addItems(input_device_list.keys())
        inputComboBox.activated.connect(inputChange)
        
        inputLabel = QLabel("Input:")
        inputLabel.setBuddy(inputComboBox)
        inputlayout = QHBoxLayout()
        inputlayout.addWidget(inputLabel)
        inputlayout.addWidget(inputComboBox)
        
        
        # OUTPUT
        outputComboBox = QComboBox()
        outputComboBox.addItems(output_device_list.keys())
        outputComboBox.activated.connect(outputChange)
        
        outputLabel = QLabel("Output:")
        outputLabel.setBuddy(outputComboBox)
        outputlayout = QHBoxLayout()
        outputlayout.addWidget(outputLabel)
        outputlayout.addWidget(outputComboBox)

        #SAMPLING RATE
        samplingRateComboBox = QComboBox()
        samplingRateComboBox.addItems(sampling_rate_list)
        samplingRateComboBox.activated.connect(samplingRateChange)
        
        samplingRateLabel = QLabel("Samplingrate:")
        samplingRateLabel.setBuddy(samplingRateComboBox)
        samplingRateLayout = QHBoxLayout()
        samplingRateLayout.addWidget(samplingRateLabel)
        samplingRateLayout.addWidget(samplingRateComboBox)
        
        
        # CHUNK
        chunkComboBox = QComboBox()
        chunkComboBox.addItems(chunk_list)
        chunkComboBox.activated.connect(chunkChange)
        
        chunkLabel = QLabel("Chunk(1024×N):")
        chunkLabel.setBuddy(chunkComboBox)
        chunkLayout = QHBoxLayout()
        chunkLayout.addWidget(chunkLabel)
        chunkLayout.addWidget(chunkComboBox)
        
        # init ThreadPyaudio Props
        self.INPUT_DEVICE_INDEX = input_device_list[inputComboBox.currentText()]
        self.OUTPUT_DEVICE_INDEX = output_device_list[outputComboBox.currentText()]
        self.SAMPLING_RATE = int(samplingRateComboBox.currentText())
        self.N = int(chunkComboBox.currentText())
        
        parentLayout = QVBoxLayout()
        parentLayout.addLayout(inputlayout)
        parentLayout.addLayout(outputlayout)
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
            self.thread_pyaudio = ThreadPyaudio(self.SAMPLING_RATE, self.N, self.INPUT_DEVICE_INDEX, self.OUTPUT_DEVICE_INDEX, self.N_STEPS)
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
