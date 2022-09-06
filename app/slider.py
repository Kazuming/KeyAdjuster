from PyQt5.QtWidgets import *
import global_variables as gv


class KeySlider(QSlider):

    def __init__(self, parent=None, label=None) -> None:
        super().__init__(parent)
        self.setMinimum(-6)
        self.setMaximum(6)
        self.setValue(0)
        self.setTickPosition(QSlider.TicksBelow)
        self.setTickInterval(1)
        self.label = label
        gv.N_STEPS = 0
        self.valueChanged.connect(self.keyAdjust)

    def keyAdjust(self):
        key = self.value()
        gv.N_STEPS = key
        if key > 0:
            self.label.setText('原曲キー: +'+str(key))
        elif key < 0:
            self.label.setText('原曲キー: '+str(key))
        else:
            self.label.setText('原曲キー: ±0')


