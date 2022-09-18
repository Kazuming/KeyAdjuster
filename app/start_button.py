from PyQt5.QtWidgets import *

from audio import ThreadPyaudio
import global_variables as gv


class StartButtonGroup():

    def __init__(self, config, parent=None):
        self.startButton = QPushButton("START")
        self.startButton.clicked.connect(self.onClickStart)
        self.startButton.setDefault(True)
        self.stopButton = QPushButton("STOP")
        self.stopButton.clicked.connect(self.onClickStop)
        self.stopButton.hide()
        self.config = config
        self.audio = ThreadPyaudio()

    def onClickStart(self):
        self.config.setDisabled(True)
        self.startButton.hide()
        self.stopButton.setDefault(True)
        self.stopButton.show()
        self.play()

    def onClickStop(self):
        self.config.setEnabled(True)
        self.stopButton.hide()
        self.startButton.show()
        self.stop()

    def play(self):
        self.audio.start()
        if gv.ERROR_FLAG:
            QMessageBox.critical(None, "エラー", "デバイスが正しくありません。\nInput Device、もしくはOutput Deviceの値を変更してください。", QMessageBox.Yes)
            self.onClickStop()
            gv.ERROR_FLAG = False

    def stop(self):
        self.audio.stop()
