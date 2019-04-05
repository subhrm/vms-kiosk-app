import os
import numpy as np
import cv2
from . import sql_utils, image_utils
from time import time
from vms_kiosk_app import logger
from vms_kiosk_app.models import FM


def get_all_photos():
    resp1 = sql_utils.get_all_visitor_photos()
    resp2 = sql_utils.get_all_poi_photos()

    names = ["Unknown"] + ["Visitor-"+r[0] for r in resp1] + [r[0]+"-"+r[1] for r in resp2]
    logger.info("#of  active visitors found : %d", len(names))
    logger.info("active visitors found : %s", " | ".join(names))

    images = [np.zeros((1,224,224,3), dtype=np.uint8)]
    t0 = time()
    for _, img_b64 in resp1:
        img = image_utils.read_b64(img_b64)
        face = FM.get_face_from_image(img)
        images.append(face.reshape((1,224,224,3)))

    for _,_, img_b64 in resp2:
        img = image_utils.read_b64(img_b64)
        face = FM.get_face_from_image(img)
        images.append(face.reshape((1,224,224,3)))

    all_faces = np.vstack(images)
    logger.info("Shape of all faces : %s", str(all_faces.shape))
    visitor_vectors = FM.vectorize(all_faces)
    logger.info("Shape of vecs : %s", str(visitor_vectors.shape))
    logger.info(
        "Vectorization done. Time taken {:.3f} seconds".format(time()-t0))

    return [names, visitor_vectors]
