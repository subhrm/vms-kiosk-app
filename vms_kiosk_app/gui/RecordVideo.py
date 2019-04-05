import cv2
import numpy as np
from PyQt5 import QtCore
from vms_kiosk_app import logger


class RecordVideo(QtCore.QObject):
    image_data = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, camera_port=0, parent=None):
        super().__init__(parent)
        self.camera = cv2.VideoCapture(camera_port)

        self.timer = QtCore.QBasicTimer()
        self.started = False

    def set_button(self, btn):
        self.btn = btn

    def start_recording(self, e):
        if not self.started:
            self.timer.start(0, self)
            self.started = True
            self.btn.setText("STOP")
        else:
            self.started = False
            self.timer.stop()
            self.btn.setText("START")

    def timerEvent(self, event):
        if (event.timerId() != self.timer.timerId()):
            return

        read, data = self.camera.read()
        if read:
            self.image_data.emit(data)
