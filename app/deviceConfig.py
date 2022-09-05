import sys
from PyQt5.QtWidgets import *
import pyaudio, globalVariables

class InputDeviceComboBox(QComboBox):
    device = []
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        paudio = pyaudio.PyAudio()
        for x in range(0, paudio.get_device_count()):
            info = paudio.get_device_info_by_index(x)
            self.device.append(info["name"])
            if info["maxInputChannels"] != 0:
                self.addItem(info["name"])
        self.activated.connect(self.onActivated)
        try:
            self.setCurrentIndex(2)
            globalVariables.INPUT_DEVICE_INDEX = self.device.index(self.currentText())
        except:
            print('Please install virtual audio device.', file=sys.stderr)
            self.setCurrentIndex(0)
            globalVariables.INPUT_DEVICE_INDEX = self.device.index(self.currentText())

    def onActivated(self,text):
        globalVariables.INPUT_DEVICE_INDEX = self.device.index(text)


class OutputDeviceComboBox(QComboBox):
    device = []
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        paudio = pyaudio.PyAudio()
        for x in range(0, paudio.get_device_count()):
            info = paudio.get_device_info_by_index(x)
            self.device.append(info["name"])
            if info["maxOutputChannels"] != 0:
                self.addItem(info["name"])
        self.activated.connect(self.onActivated)
        self.setCurrentIndex(0)
        globalVariables.OUTPUT_DEVICE_INDEX = self.device.index(self.currentText())

    def onActivated(self,text):
        globalVariables.OUTPUT_DEVICE_INDEX = self.device.index(text)


class SamplingRateComboBox(QComboBox):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.addItems(["44100", "48000", "88200", "96000"])
        self.activated.connect(self.onActivated)
        globalVariables.SAMPLING_RATE = int(self.currentText())

    def onActivated(self,rate):
        globalVariables.SAMPLING_RATE = int(rate)


class ChunkComboBox(QComboBox):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.addItems(["5", "10", "20", "30", "40", "50", "80", "100"])
        self.activated.connect(self.onActivated)
        self.setCurrentIndex(2)
        globalVariables.CHUNK = int(self.currentText())

    def onActivated(self,chunk):
        globalVariables.CHUNK = int(chunk)

