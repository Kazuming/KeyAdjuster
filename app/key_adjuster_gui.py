from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtWidgets import *

import sys, signal
import start, deviceConfig, keySlider, wakeup


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
        slider = keySlider.KeySllider(Qt.Horizontal, keyLabel)
        self.keylayout.addWidget(keyLabel)
        self.keylayout.addWidget(slider)

    def createConfigWidget(self):
        self.configWidget = QGroupBox()
        self.configWidget.setAlignment(Qt.AlignCenter)

        # INPUT
        inputComboBox = deviceConfig.InputDeviceComboBox()
        inputLabel = QLabel("Input:")
        inputLabel.setBuddy(inputComboBox)
        inputlayout = QHBoxLayout()
        inputlayout.addWidget(inputLabel)
        inputlayout.addWidget(inputComboBox)

        # OUTPUT
        outputComboBox = deviceConfig.OutputDeviceComboBox()
        outputLabel = QLabel("Output:")
        outputLabel.setBuddy(outputComboBox)
        outputlayout = QHBoxLayout()
        outputlayout.addWidget(outputLabel)
        outputlayout.addWidget(outputComboBox)

        #SAMPLING RATE
        samplingRateComboBox = deviceConfig.SamplingRateComboBox()
        samplingRateLabel = QLabel("Samplingrate:")
        samplingRateLabel.setBuddy(samplingRateComboBox)
        samplingRateLayout = QHBoxLayout()
        samplingRateLayout.addWidget(samplingRateLabel)
        samplingRateLayout.addWidget(samplingRateComboBox)

        # CHUNK
        chunkComboBox = deviceConfig.ChunkComboBox()
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


def exit():
    app.exec()
    mainWidget.startButtonGroup.stop()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('icons/anplifier.png'))
    wakeup.SignalWakeupHandler(app)
    signal.signal(signal.SIGINT, lambda sig,_: app.quit())
    mainWidget = MainWidget()
    mainWidget.show()
    sys.exit(exit())
