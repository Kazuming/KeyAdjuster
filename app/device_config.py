import pyaudio
from PyQt5.QtWidgets import *

import global_variables as gv


class InputDeviceComboBox(QComboBox):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.device, _, self.virtual_device = getDevice()
        self.addItems(self.device.keys())
        self.activated.connect(self.onActivated)
        # 仮想オーディオのインストールを推奨するポップアップ
        if len(self.device) == 0:
            QMessageBox.information(None, "Key Adjusterのご利用にあたって", "仮想オーディオ（VB-CABLEなど）をインストールすることをお勧めします。", QMessageBox.Yes)
        else:
            for virtual_device in ["CABLE Output (VB-Audio Virtual "]:
                if virtual_device in self.device.keys():
                    self.setCurrentText("CABLE Output (VB-Audio Virtual ")
                    gv.INPUT_DEVICE_INDEX = self.device[self.currentText()]["index"]
                    gv.INPUT_CHANNELS = self.device[self.currentText()]["maxInputChannels"]
                    return
            self.setCurrentText(list(self.virtual_device.keys())[0])
        gv.INPUT_DEVICE_INDEX = self.device[self.currentText()]["index"]
        gv.INPUT_CHANNELS = self.device[self.currentText()]["maxInputChannels"]

    def onActivated(self):
        gv.INPUT_DEVICE_INDEX = self.device[self.currentText()]["index"]
        gv.INPUT_CHANNELS = self.device[self.currentText()]["maxInputChannels"]


class OutputDeviceComboBox(QComboBox):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        _, self.device, _ = getDevice()
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
    virtual_device = {}
    for x in range(pa.get_device_count()):
        info = pa.get_device_info_by_index(x)
        if info["maxInputChannels"] > 2:
            input_device[info["name"]] = info
        if info["maxOutputChannels"] == 2:
            output_device[info["name"]] = info
        if info["maxInputChannels"] >= 2 and info["maxOutputChannels"] >= 2 and info["name"] != "Microsoft Teams Audio":
            input_device[info["name"]] = info
            virtual_device[info["name"]] = info
    return input_device, output_device, virtual_device
