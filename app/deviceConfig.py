import sys
from PyQt5.QtWidgets import *
import pyaudio

import globalVariables as gv


class InputDeviceComboBox(QComboBox):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.deviceInfo = getDevice()
        for name, info in self.deviceInfo.items():
            if info["maxInputChannels"] != 0:
                self.addItem(name)
        self.activated[str].connect(self.onActivated)
        try:
            self.setCurrentIndex(2)
            gv.INPUT_DEVICE_INDEX = self.deviceInfo[self.currentText()]["index"]
            gv.INPUT_CHANNELS = self.deviceInfo[self.currentText()]["maxInputChannels"]
        except:
            print('Please install virtual audio device.', file=sys.stderr)

    def onActivated(self,text):
        gv.INPUT_DEVICE_INDEX = self.deviceInfo[text]["index"]
        gv.INPUT_CHANNELS = self.deviceInfo[text]["maxInputChannels"]


class OutputDeviceComboBox(QComboBox):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.deviceInfo = getDevice()
        for name, info in self.deviceInfo.items():
            if info["maxOutputChannels"] != 0:
                self.addItem(name)
        self.setCurrentIndex(0)
        self.activated[str].connect(self.onActivated)
        gv.OUTPUT_DEVICE_INDEX = self.deviceInfo[self.currentText()]["index"]
        gv.OUTPUT_CHANNELS = self.deviceInfo[self.currentText()]["maxOutputChannels"]

    def onActivated(self,text):
        print(text)
        gv.OUTPUT_DEVICE_INDEX = self.deviceInfo[text]["index"]
        gv.OUTPUT_CHANNELS = self.deviceInfo[text]["maxOutputChannels"]


class SamplingRateComboBox(QComboBox):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.addItems(["44100", "48000", "88200", "96000"])
        self.activated[str].connect(self.onActivated)
        gv.SAMPLING_RATE = int(self.currentText())

    def onActivated(self,rate):
        print(rate)
        gv.SAMPLING_RATE = int(rate)


class ChunkComboBox(QComboBox):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.addItems(["5", "10", "20", "30", "40", "50", "80", "100"])
        self.activated[str].connect(self.onActivated)
        self.setCurrentIndex(2)
        gv.CHUNK = int(self.currentText())

    def onActivated(self,chunk):
        print(chunk)
        gv.CHUNK = int(chunk)


def getDevice():
    pa= pyaudio.PyAudio()
    d = dict()
    for x in range(pa.get_device_count()):
        name = pa.get_device_info_by_index(x)["name"]
        info = pa.get_device_info_by_index(x)
        d[name] = info
    return d
