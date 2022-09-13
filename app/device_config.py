import sys

import pyaudio
from PyQt5.QtWidgets import *

import global_variables as gv


class InputDeviceComboBox(QComboBox):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.device, _ = getDevice()
        self.addItems(self.device.keys())
        self.activated.connect(self.onActivated)
        for virtual_device in ["Soundflower (2ch)", "BlackHole 2ch"]:
            if virtual_device in self.device.keys():
                self.setCurrentText(virtual_device)
                gv.INPUT_DEVICE_INDEX = self.device[self.currentText()]["index"]
                gv.INPUT_CHANNELS = self.device[self.currentText()]["maxInputChannels"]
                return
        gv.INPUT_DEVICE_INDEX = self.device[self.currentText()]["index"]
        gv.INPUT_CHANNELS = self.device[self.currentText()]["maxInputChannels"]
        # ダイアログにした方がいいかも
        print("Please install virtual audio device.", file=sys.stderr)

    def onActivated(self):
        gv.INPUT_DEVICE_INDEX = self.device[self.currentText()]["index"]
        gv.INPUT_CHANNELS = self.device[self.currentText()]["maxInputChannels"]


class OutputDeviceComboBox(QComboBox):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        _, self.device = getDevice()
        self.addItems(self.device.keys())
        self.activated.connect(self.onActivated)
        self.setCurrentIndex(0)
        gv.OUTPUT_DEVICE_INDEX = self.device[self.currentText()]["index"]
        gv.OUTPUT_CHANNELS = self.device[self.currentText()]["maxOutputChannels"]

    def onActivated(self):
        gv.OUTPUT_DEVICE_INDEX = self.device[self.currentText()]["index"]
        gv.OUTPUT_CHANNELS = self.device[self.currentText()]["maxOutputChannels"]


class SamplingRateComboBox(QComboBox):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.addItems(["44100", "48000", "88200", "96000"])
        self.activated[str].connect(self.onActivated)
        gv.SAMPLING_RATE = int(self.currentText())

    def onActivated(self,rate):
        gv.SAMPLING_RATE = int(rate)


def getDevice():
    pa = pyaudio.PyAudio()
    input_device = {}
    output_device = {}
    for x in range(pa.get_device_count()):
        info = pa.get_device_info_by_index(x)
        if info["maxInputChannels"] != 0:
            input_device[info["name"]] = info
        if info["maxOutputChannels"] != 0:
            output_device[info["name"]] = info
    return input_device, output_device
