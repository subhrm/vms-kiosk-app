from PyQt5 import QtCore
import numpy as np


class Signals(QtCore.QObject):
    camera_signal = QtCore.pyqtSignal(np.ndarray)
    detect_faces = QtCore.pyqtSignal(np.ndarray)
