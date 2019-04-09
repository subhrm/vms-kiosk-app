import cv2
import numpy as np
from PyQt5 import QtCore
from vms_kiosk_app import logger

from .VideoAnalyser import VideoAnalyser


class RecordVideo(QtCore.QObject):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = VideoAnalyser()
        self.started = False

    def set_button(self, btn):
        self.btn = btn

    def start_recording(self, e):
        if not self.started:
            self.started = True
            self.btn.setText("STOP")
            self.worker.start()
        else:
            self.started = False
            self.worker.terminate()
            self.btn.setText("START")
