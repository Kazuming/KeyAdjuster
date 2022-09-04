import sys
from PyQt5.QtWidgets import *
import pyaudio, globalVariables

class inputDeviceComboBox(QComboBox):
    device = []
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        paudio = pyaudio.PyAudio()
        for x in range(0, paudio.get_device_count()):
            info = paudio.get_device_info_by_index(x)
            self.device.append(info["name"])
            if info["maxInputChannels"] != 0:
                self.addItem(info["name"])
        self.activated[str].connect(self.onActivated)
        try:
            self.setCurrentIndex(2)
            globalVariables.INPUT_DEVICE_INDEX = self.device.index(self.itemText(2))
        except:
            print('Please install virtual audio device.', file=sys.stderr)
            self.setCurrentIndex(0)
            globalVariables.INPUT_DEVICE_INDEX = 0

    def onActivated(self,text):
        globalVariables.INPUT_DEVICE_INDEX = self.device.index(text)


class outputDeviceComboBox(QComboBox):
    device = []
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        paudio = pyaudio.PyAudio()
        for x in range(0, paudio.get_device_count()):
            info = paudio.get_device_info_by_index(x)
            self.device.append(info["name"])
            if info["maxOutputChannels"] != 0:
                self.addItem(info["name"])
        self.activated[str].connect(self.onActivated)
        self.setCurrentIndex(0)

    def onActivated(self,text):
        globalVariables.OUTPUT_DEVICE_INDEX = self.device.index(text)


class samplingRateComboBox(QComboBox):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.addItems(["44100", "48000", "88200", "96000"])
        self.activated[int].connect(self.onActivated)

    def onActivated(self,rate):
        globalVariables.SAMPLING_RATE = int(rate)


class chunkComboBox(QComboBox):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.addItems(["10", "20", "30", "40", "50", "60", "70", "80", "90", "100"])
        self.activated[int].connect(self.onActivated)
        self.setCurrentIndex(4)
        globalVariables.CHUNK = 50*1024

    def onActivated(self,chunk):
        globalVariables.CHUNK = int(chunk)*1024

