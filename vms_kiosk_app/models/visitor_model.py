'''
    find visitor by face
'''
import numpy as np
import cv2
from vms_kiosk_app import logger
from vms_kiosk_app.models import FM
from vms_kiosk_app.utils import sql_utils, image_utils, download_utils
from sklearn.metrics.pairwise import cosine_similarity

class Visitor_Model:
    def __init__(self):
        self.update()
        
    def update(self):
        names , face_vectors = download_utils.get_all_photos()
        self.names = names
        self.vectors = face_vectors
        logger.info("Visitor Model initialized")

    def find(self, img_set):
        
        images = [cv2.resize(img,(224,224)) for img in img_set]
        images = [cv2.cvtColor(img, cv2.COLOR_BGR2RGB) for img in images]
        x = np.vstack([img.reshape(1,224,224,3) for img in images])
        new_vecs = FM.vectorize(x)

        c = cosine_similarity(new_vecs, self.vectors)

        max_c = np.max(c, axis=1)
        max_ac = np.argmax(c,axis=1)

        res = []
        for score, idx in zip(max_c, max_ac):
            if score > 0.65:
                res.append(self.names[idx])
            else:
                res.append("")
        return res