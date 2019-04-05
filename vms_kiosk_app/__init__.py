import sys
import os
from datetime import datetime

from vms_kiosk_app.__version__ import name, version
print("%s - Version : %s" % (name, version))

'''
    Define common logger.
'''
import logging
from .config import Config
config = Config()

logging.basicConfig(format='%(asctime)s - %(filename)s:%(lineno)d %(levelname)s - %(message)s',
                    level=logging.INFO,
                    handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(name)

logger.info("=" * 80)
logger.info("%s %s - Version : %s %s", " " * 5, name, version, " " * 5)
logger.info("=" * 80)
