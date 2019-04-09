import cv2
import numpy as np
import time
from PyQt5 import QtCore
from vms_kiosk_app import logger, signals
from vms_kiosk_app.models.visitor_model import Visitor_Model


class VideoAnalyser(QtCore.QThread):
    # image_data = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, camera_port=0, signal=None):
        super().__init__()
        self.camera = cv2.VideoCapture(camera_port)
        self.VM = Visitor_Model()
        # self.signal = camera_signal
        # self.started = False

    def __del__(self):
        self.wait()

    def run(self):
        logger.info("Starting Camera thread")
        cnt = 0
        while (True):
            read, data = self.camera.read()
            updated_image = self.VM.process(data)
            signals.camera_signal.emit(updated_image)
            # if cnt % 7 == 0:
            #     signals.detect_faces.emit(data)
            cnt += 1
            logger.info("Frame : %d", cnt)
            # time.sleep(0.01)
