from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon


class InputTip(QToolButton):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setIcon(QIcon('icons/icon_b.png'))


class OutputTip(QToolButton):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setIcon(QIcon('icons/icon_b.png'))


class SamplingRateTip(QToolButton):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setIcon(QIcon('icons/icon_b.png'))

