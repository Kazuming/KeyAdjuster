from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtGui

import global_variables as gv


class KeySlider(QSlider):

    def __init__(self) -> None:
        super().__init__(Qt.Horizontal)
        self.setMinimum(-6)
        self.setMaximum(6)
        self.setValue(0)
        self.setTickPosition(QSlider.TicksBelow)
        self.setTickInterval(1)
        self.label = QLabel("原曲キー")
        self.label.setFont(QtGui.QFont("Verdana", 20,QtGui.QFont.Black))
        self.label.setAlignment(Qt.AlignCenter)
        gv.N_STEPS = 0
        self.valueChanged.connect(self.keyAdjust)

    def keyAdjust(self):
        key = self.value()
        gv.N_STEPS = key
        if key > 0:
            self.label.setText("♯"+str(key))
        elif key < 0:
            self.label.setText("♭"+str(abs(key)))
        else:
            self.label.setText("原曲キー")
