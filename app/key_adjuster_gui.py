from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtWidgets import *

import sys
import start, deviceConfig, globalVariables


class WidgetGallery(QWidget):
    def __init__(self):
        super().__init__()
        keylayout = QVBoxLayout()
        self.l1 = QLabel("原曲キー: ±0")
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
        self.sl.valueChanged.connect(self.valuechange)

        self.createConfigWidget()
        self.startButtonGroup = start.startButtonGroup(self.configWidget)

        mainLayout = QGridLayout()
        mainLayout.addLayout(keylayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.configWidget, 0, 2)
        mainLayout.addWidget(self.startButtonGroup.startButton, 1, 0, 1, 3)
        mainLayout.addWidget(self.startButtonGroup.stopButton, 1, 0, 1, 3)

        self.setLayout(mainLayout)
        self.setWindowTitle("KeyAdjuster")
        self.setGeometry(100,100,600,300)
        self.changeStyle('win')

    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    def changePalette(self):
            QApplication.setPalette(QApplication.style().standardPalette())


    def valuechange(self):
        key = self.sl.value()
        globalVariables.N_STEPS = key
        if key > 0:
            self.l1.setText('原曲キー: +'+str(key))
        elif key < 0:
            self.l1.setText('原曲キー: '+str(key))
        else:
            self.l1.setText('原曲キー: ±0')


    def createConfigWidget(self):
        self.configWidget = QGroupBox()
        self.configWidget.setAlignment(Qt.AlignCenter)

        # INPUT
        inputComboBox = deviceConfig.inputDeviceComboBox()
        inputLabel = QLabel("Input:")
        inputLabel.setBuddy(inputComboBox)
        inputlayout = QHBoxLayout()
        inputlayout.addWidget(inputLabel)
        inputlayout.addWidget(inputComboBox)

        # OUTPUT
        outputComboBox = deviceConfig.outputDeviceComboBox()
        outputLabel = QLabel("Output:")
        outputLabel.setBuddy(outputComboBox)
        outputlayout = QHBoxLayout()
        outputlayout.addWidget(outputLabel)
        outputlayout.addWidget(outputComboBox)

        #SAMPLING RATE
        samplingRateComboBox = deviceConfig.samplingRateComboBox()
        samplingRateLabel = QLabel("Samplingrate:")
        samplingRateLabel.setBuddy(samplingRateComboBox)
        samplingRateLayout = QHBoxLayout()
        samplingRateLayout.addWidget(samplingRateLabel)
        samplingRateLayout.addWidget(samplingRateComboBox)

        # CHUNK
        chunkComboBox = deviceConfig.chunkComboBox()
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec())
