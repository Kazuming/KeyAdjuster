from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

import device_config
import slider
import start


class MainWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.createKeyArea()
        self.createConfigWidget()
        self.createStartWidget()

        mainLayout = QGridLayout()
        mainLayout.addLayout(self.keylayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.configWidget, 0, 2)
        mainLayout.addLayout(self.startlayout, 1, 0, 1, 3)

        self.setLayout(mainLayout)
        self.setWindowTitle("KeyAdjuster")
        self.setGeometry(100,100,600,300)
        # self.changeStyle('Macintosh')

    def createKeyArea(self):
        self.keylayout = QVBoxLayout()
        keyLabel = QLabel("原曲キー: ±0")
        keyLabel.setFont(QtGui.QFont("Verdana", 20,QtGui.QFont.Black))
        keyLabel.setAlignment(Qt.AlignCenter)
        keySlider = slider.KeySlider(Qt.Horizontal, keyLabel)
        self.keylayout.addWidget(keyLabel)
        self.keylayout.addWidget(keySlider)

    def createConfigWidget(self):
        self.configWidget = QGroupBox()
        self.configWidget.setAlignment(Qt.AlignCenter)

        # INPUT
        inputComboBox = device_config.InputDeviceComboBox()
        inputLabel = QLabel("Input:")
        inputLabel.setBuddy(inputComboBox)
        inputlayout = QHBoxLayout()
        inputlayout.addWidget(inputLabel)
        inputlayout.addWidget(inputComboBox)

        # OUTPUT
        outputComboBox = device_config.OutputDeviceComboBox()
        outputLabel = QLabel("Output:")
        outputLabel.setBuddy(outputComboBox)
        outputlayout = QHBoxLayout()
        outputlayout.addWidget(outputLabel)
        outputlayout.addWidget(outputComboBox)

        #SAMPLING RATE
        samplingRateComboBox = device_config.SamplingRateComboBox()
        samplingRateLabel = QLabel("Samplingrate:")
        samplingRateLabel.setBuddy(samplingRateComboBox)
        samplingRateLayout = QHBoxLayout()
        samplingRateLayout.addWidget(samplingRateLabel)
        samplingRateLayout.addWidget(samplingRateComboBox)

        # DELAY
        delayComboBox = device_config.DelayComboBox()
        delayLabel = QLabel("Delay:")
        delayLabel.setBuddy(delayComboBox)
        delayLayout = QHBoxLayout()
        delayLayout.addWidget(delayLabel)
        delayLayout.addWidget(delayComboBox)

        parentLayout = QVBoxLayout()
        parentLayout.addLayout(inputlayout)
        parentLayout.addLayout(outputlayout)
        parentLayout.addLayout(samplingRateLayout)
        parentLayout.addLayout(delayLayout)
        self.configWidget.setLayout(parentLayout)

    def createStartWidget(self):
        self.startlayout = QVBoxLayout()
        self.startButtonGroup = start.StartButtonGroup(self.configWidget)
        self.startlayout.addWidget(self.startButtonGroup.startButton)
        self.startlayout.addWidget(self.startButtonGroup.stopButton)

    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    def changePalette(self):
            QApplication.setPalette(QApplication.style().standardPalette())

    def exec(self, app):
        app.exec()
        self.startButtonGroup.stop()