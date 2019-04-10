'''
    find visitor by face
'''
import os
import numpy as np
import cv2
from vms_kiosk_app import logger, config
from vms_kiosk_app.models import FM
from vms_kiosk_app.utils import sql_utils, image_utils, download_utils
from sklearn.metrics.pairwise import cosine_similarity


class Visitor_Model:
    def __init__(self):
        self.update()
        self._red = (0, 0, 255)
        self._blue = (255, 0, 0)
        self._green = (0, 255, 0)
        self._yellow = (0, 255, 255)
        self._white = (255, 255, 255)
        self._width = 2
        self._min_size = (30, 30)
        self.count = 0
        self.faces = []
        self.res = []
        haar_cascade_filepath = os.path.join(
            config.DATA_DIR, config.FACE_CASCADE_MODELS[1])
        self.classifier = cv2.CascadeClassifier(haar_cascade_filepath)

    def update(self):
        names, face_vectors = download_utils.get_all_photos()
        self.names = names
        self.vectors = face_vectors
        logger.info("Photos refreshed")

    def detect_faces(self, image: np.ndarray):
        # haarclassifiers work better in black and white
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # gray_image = cv2.equalizeHist(gray_image)

        faces = self.classifier.detectMultiScale(gray_image,
                                                 scaleFactor=1.3,
                                                 minNeighbors=4,
                                                 flags=cv2.CASCADE_SCALE_IMAGE,
                                                 minSize=self._min_size)

        return faces

    def find(self, img_set):

        res = []
        if len(img_set) > 0:
            images = [cv2.resize(img, (224, 224)) for img in img_set]
            images = [cv2.cvtColor(img, cv2.COLOR_BGR2RGB) for img in images]
            x = np.vstack([img.reshape(1, 224, 224, 3) for img in images])
            new_vecs = FM.vectorize(x)

            c = cosine_similarity(new_vecs, self.vectors)

            max_c = np.max(c, axis=1)
            max_ac = np.argmax(c, axis=1)

            for score, idx in zip(max_c, max_ac):
                if score > 0.65:
                    res.append(self.names[idx])
                else:
                    res.append("")

        return res

    def process(self, frame):
        ''' 
        Process each frame

        Arguments:
            frame {np.ndarray} -- A camera frame
        '''

        if self.count < 0:
            self.update()
            self.count = 0

        if self.count % 7 == 0:
            self.faces = self.detect_faces(frame)
            cropped_faces = [frame[y:y+h, x:x+w]
                             for x, y, w, h in self.faces]
            self.res = self.find(cropped_faces)

        self.count += 1

        if self.count == config.UPDATE_INTERVAL:
            self.count = -1
            return self.schedule_update(frame)

        if len(self.faces) > 0:

            for (x, y, w, h), name in zip(self.faces, self.res):
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
                cv2.rectangle(frame,
                              (x, y),
                              (x+w, y+h),
                              color,
                              self._width)

                # Write the person's name
                # Write some Text

                cv2.putText(img=frame, text=name,
                            org=(x, y-10),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            # fontFace=cv2.FONT_HERSHEY_PLAIN,
                            fontScale=0.7,
                            color=color,
                            thickness=self._width)

        return frame

    def schedule_update(self, frame):
        logger.info("Scheduling updatation of faces from central database")
        empty_image = np.zeros_like(frame).astype(np.uint8)
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
        return empty_image
