from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

import device_config
import key_slider
import start_button
import tip


class MainWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.createKeyWidget()
        self.createConfigWidget()
        self.createStartWidget()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.keyWidget, 0, 0, 1, 2)
        mainLayout.addWidget(self.configWidget, 0, 2)
        mainLayout.addLayout(self.startLayout, 1, 0, 1, 3)

        self.setLayout(mainLayout)
        self.setWindowTitle("Key Adjuster")
        self.setGeometry(100,100,900,450)
        # self.changeStyle('Fusion')
    def createKeyWidget(self):
        keyLayout = QVBoxLayout()
        keySlider = key_slider.KeySlider()
        keyLabel = keySlider.label
        keyLayout.addWidget(keyLabel)
        keyLayout.addWidget(keySlider)
        self.keyWidget = QGroupBox()
        self.keyWidget.setLayout(keyLayout)

    def createConfigWidget(self):
        # TIPS
        tips = tip.tipGroup()

        # INPUT
        inputLayout = QVBoxLayout()
        inputTipLayout = QHBoxLayout()
        inputComboBox = device_config.InputDeviceComboBox()
        inputTip = tips.inputTip
        inputLabel = QLabel("Input Device:")
        inputLabel.setBuddy(inputComboBox)
        inputTipLayout.addWidget(inputComboBox)
        inputTipLayout.addWidget(inputTip)
        inputLayout.addWidget(inputLabel)
        inputLayout.addLayout(inputTipLayout)

        # OUTPUT
        outputLayout = QVBoxLayout()
        outputTipLayout = QHBoxLayout()
        outputComboBox = device_config.OutputDeviceComboBox()
        outputTip = tips.outputTip
        outputLabel = QLabel("Output Device:")
        outputLabel.setBuddy(outputComboBox)
        outputTipLayout.addWidget(outputComboBox)
        outputTipLayout.addWidget(outputTip)
        outputLayout.addWidget(outputLabel)
        outputLayout.addLayout(outputTipLayout)

        #SAMPLING RATE
        samplingRateLayout = QVBoxLayout()
        samplingRateTipLayout = QHBoxLayout()
        samplingRateComboBox = device_config.SamplingRateComboBox()
        samplingRateTip = tips.samplingRateTip
        samplingRateLabel = QLabel("Sampling Rate:")
        samplingRateLabel.setBuddy(samplingRateComboBox)
        samplingRateTipLayout.addWidget(samplingRateComboBox)
        samplingRateTipLayout.addWidget(samplingRateTip)
        samplingRateLayout.addWidget(samplingRateLabel)
        samplingRateLayout.addLayout(samplingRateTipLayout)

        parentLayout = QVBoxLayout()
        parentLayout.addLayout(inputLayout)
        parentLayout.addLayout(outputLayout)
        parentLayout.addLayout(samplingRateLayout)
        self.configWidget = QGroupBox()
        self.configWidget.setAlignment(Qt.AlignCenter)
        self.configWidget.setLayout(parentLayout)

    def createStartWidget(self):
        self.startLayout = QVBoxLayout()
        self.startButtonGroup = start_button.StartButtonGroup(self.configWidget)
        self.startLayout.addWidget(self.startButtonGroup.startButton)
        self.startLayout.addWidget(self.startButtonGroup.stopButton)
        self.startLayout.setStretch(1,1)

    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    def changePalette(self):
        QApplication.setPalette(QApplication.style().standardPalette())

    def exec(self, app):
        app.exec()
        self.startButtonGroup.stop()
