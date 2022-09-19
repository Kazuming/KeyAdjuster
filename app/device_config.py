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
        if len(self.virtual_device) == 0:
            QMessageBox.information(None, "Key Adjusterのご利用にあたって", "仮想オーディオ（VB-CABLEなど）をインストールすることをお勧めします。", QMessageBox.Yes)
        else:
            for recommend_device in ["CABLE Output"]:
                for device in self.device.keys():
                    if recommend_device in device:
                        self.setCurrentText(device)
                        gv.INPUT_DEVICE_INDEX = self.device[self.currentText()]["index"]
                        gv.INPUT_CHANNELS = self.device[self.currentText()]["maxInputChannels"]
                        return
            if len(self.virtual_device.keys()) != 0:
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
        for recommend_device in ["ヘッドホン", "スピーカー"]:
                for device in self.device.keys():
                    if recommend_device in device:
                        self.setCurrentText(device)
                        gv.OUTPUT_DEVICE_INDEX = self.device[self.currentText()]["index"]
                        gv.OUTPUT_CHANNELS = self.device[self.currentText()]["maxOutputChannels"]
                        return
        gv.OUTPUT_DEVICE_INDEX = self.device[self.currentText()]["index"]
        gv.OUTPUT_CHANNELS = self.device[self.currentText()]["maxOutputChannels"]

    def onActivated(self):
        gv.OUTPUT_DEVICE_INDEX = self.device[self.currentText()]["index"]
        gv.OUTPUT_CHANNELS = self.device[self.currentText()]["maxOutputChannels"]


class SamplingRateComboBox(QComboBox):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.addItems(["44100", "48000", "88200", "96000", "16000"])
        self.activated[str].connect(self.onActivated)
        gv.SAMPLING_RATE = int(self.currentText())

    def onActivated(self,rate):
        gv.SAMPLING_RATE = int(rate)


def getDevice():
    pa = pyaudio.PyAudio()
    input_device = {}
    output_device = {}
    virtual_device = {}
    devices = pa.get_host_api_info_by_index(0)
    numdevices = devices.get('deviceCount')

    for i in range(0, numdevices):
        info = pa.get_device_info_by_host_api_device_index(0, i)
        device_name = info.get('name')
        max_input_channels = info.get('maxInputChannels')
        max_output_channels = info.get('maxOutputChannels')

        if max_input_channels > 0 and "Microsoft Sound Mapper" not in device_name:
            input_device[device_name] = info

        if max_input_channels > 2 and "Microsoft Sound Mapper" not in device_name:
            virtual_device[device_name] = info

        if max_output_channels > 0 and "Microsoft Sound Mapper" not in device_name:
            output_device[device_name] = info

    return input_device, output_device, virtual_device
