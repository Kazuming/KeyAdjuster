from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont

class tipGroup():

    def __init__(self):
        QToolTip.setFont(QFont("Verdana", 14))

        # インプットデバイス用のツールチップ
        self.inputTip = QToolButton()
        self.inputTip.setEnabled(False)
        self.inputTip.setIcon(QApplication.style().standardIcon(QStyle.SP_MessageBoxQuestion))
        self.inputTip.setToolTip("入力するデバイスを選んでください。\n【推奨】: 仮想オーディオ（Soundflower, BlackHoleなど）")

        # アウトプットデバイス用のツールチップ
        self.outputTip = QToolButton()
        self.outputTip.setEnabled(False)
        self.outputTip.setIcon(QApplication.style().standardIcon(QStyle.SP_MessageBoxQuestion))
        self.outputTip.setToolTip("出力するデバイスを選んでください。\n【推奨】: スピーカー（PC, イヤフォンなど）")

        # サンプリングレート用のツールチップ
        self.samplingRateTip = QToolButton()
        self.samplingRateTip.setEnabled(False)
        self.samplingRateTip.setIcon(QApplication.style().standardIcon(QStyle.SP_MessageBoxQuestion))
        self.samplingRateTip.setToolTip("サンプリング周波数を選んでください。\n【推奨】: 44100Hz")
