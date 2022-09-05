
from PyQt5.QtWidgets import *
from thread_pyaudio import ThreadPyaudio

class StartButtonGroup():
    def __init__(self, config, parent=None):
        self.startButton = QPushButton("START")
        self.startButton.clicked.connect(self.onClickStart)
        self.startButton.setDefault(False)
        self.stopButton = QPushButton("STOP")
        self.stopButton.clicked.connect(self.onClickStop)
        self.stopButton.hide()
        self.play_flag = False
        self.thread_pyaudio : ThreadPyaudio
        self.config = config

    def onClickStart(self):
        self.config.setDisabled(True)
        self.startButton.hide()
        self.stopButton.setDefault(True)
        self.stopButton.show()
        self.play()
        pass

    def onClickStop(self):
        self.config.setEnabled(True)
        self.stopButton.hide()
        self.startButton.show()
        self.stop()
        pass

    def play(self):
        if not self.play_flag:
            self.thread_pyaudio = ThreadPyaudio()
            self.thread_pyaudio.start()
        self.play_flag = True

    def stop(self):
        if self.play_flag:
            self.thread_pyaudio.kill_flag = True
        self.play_flag = False