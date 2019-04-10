import os


class Config():
    '''
        Define all global constants using the CONFIG.json file
    '''

    def __init__(self):
        self.DATA_DIR = "./data"

        self.FACE_CASCADE_MODELS = [
            "haarcascade_profileface.xml",
            "haarcascade_frontalface_alt.xml",
            "haarcascade_frontalface_alt_tree.xml"
        ]

        self.USE_DB = True

        self.SQL_SERVER_IP = "142.93.215.112"
        self.SQL_SERVER_PORT = "3306"
        self.DB_NAME = "vms"
        self.SQL_SERVER_USER_ID = os.environ.get("SQL_SERVER_USER_ID")
        self.SQL_SERVER_USER_PWD = os.environ.get("SQL_SERVER_USER_PWD")

        self.IMAGE_DIR = "./data/photos"
