import cv2
import numpy as np
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from vms_kiosk_app import logger
from vms_kiosk_app.models.visitor_model import Visitor_Model

MAX = 200

class FaceDetectionWidget(QtWidgets.QWidget):
    def __init__(self, haar_cascade_filepath, parent=None):
        super().__init__(parent)
        self.classifier = cv2.CascadeClassifier(haar_cascade_filepath)
        self.image = QtGui.QImage()
        self._red = (0, 0, 255)
        self._blue = (255, 0, 0)
        self._green = (0, 255, 0)
        self._yellow = (0, 255, 255)
        self._white = (255, 255, 255)
        self._width = 2
        self._min_size = (30, 30)
        self.vm = Visitor_Model()
        self.cnt = MAX - 1

    def detect_faces(self, image: np.ndarray):
        # haarclassifiers work better in black and white
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_image = cv2.equalizeHist(gray_image)

        faces = self.classifier.detectMultiScale(gray_image,
                                                 scaleFactor=1.3,
                                                 minNeighbors=4,
                                                 flags=cv2.CASCADE_SCALE_IMAGE,
                                                 minSize=self._min_size)

        return faces

    def image_data_slot(self, image_data):
        
        if self.cnt == MAX:
            self.vm.update()

        faces = self.detect_faces(image_data)

        if len(faces) > 0:
            cropped_faces = [ image_data[y:y+h, x:x+w] for x,y,w,h in faces]
            res = self.vm.find(cropped_faces)

            for (x, y, w, h), name in zip(faces, res):
                user_type = list(name.split("-"))[0]
                color = self._white
                if user_type == "VIP":
                    color = self._yellow
                elif user_type == "Threat":
                    color = self._red
                elif user_type == "Missing":
                    color = self._blue
                elif user_type == "Visitor":
                    color = self._green
                cv2.rectangle(image_data,
                            (x, y),
                            (x+w, y+h),
                            color,
                            self._width)

                # Write the person's name
                # Write some Text

                cv2.putText(img=image_data, text=name,
                            org=(x, y-10),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            # fontFace=cv2.FONT_HERSHEY_PLAIN,
                            fontScale=0.7,
                            color=color,
                            thickness=self._width)

        self.cnt = self.cnt - 1

        if self.cnt > 0:
            self.image = self.get_qimage(image_data)
            if self.image.size() != self.size():
                self.setFixedSize(self.image.size())

            self.update()
        else:
            logger.info("Updating Vistor faces from database")
            empty_image = np.zeros_like(image_data).astype(np.uint8)
            # logger.info(str(empty_image.shape))
            cv2.putText(img=empty_image, text="Wait ......",
                        org=(10, 100),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1,
                        color=self._white,
                        thickness=self._width)
            cv2.putText(img=empty_image, text="Refreshing images from Database",
                        org=(10, 150),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1,
                        color=self._white,
                        thickness=self._width)

            self.image = self.get_qimage(empty_image)
            if self.image.size() != self.size():
                self.setFixedSize(self.image.size())

            self.update()
            self.cnt = MAX


    def get_qimage(self, image: np.ndarray):
        height, width, _ = image.shape
        bytesPerLine = 3 * width
        QImage = QtGui.QImage

        image = QImage(image.data,
                       width,
                       height,
                       bytesPerLine,
                       QImage.Format_RGB888)

        image = image.rgbSwapped()
        return image

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()

    def update_faces(self, faces_list):
        logger.info("updating faces")
