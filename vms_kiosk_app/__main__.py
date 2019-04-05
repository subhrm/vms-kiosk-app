import sys
import os
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from vms_kiosk_app import config, logger
from vms_kiosk_app.gui.MainWidget import MainWidget


def main():
    '''
        The main method
    '''

    logger.info("Starting desktop app !")

    haar_cascade_filepath = os.path.join(
        config.DATA_DIR, config.FACE_CASCADE_MODELS[1])

    # app = QtWidgets.QApplication(sys.argv)
    app = QtWidgets.QApplication(["Visitor Management System"])

    main_window = QtWidgets.QMainWindow()
    main_window.setWindowTitle("Visitor Management System")
    main_widget = MainWidget(haar_cascade_filepath)
    main_window.setCentralWidget(main_widget)
    main_window.show()
    sys.exit(app.exec_())


'''
    The main entry point
'''

if __name__ == '__main__':
    main()
