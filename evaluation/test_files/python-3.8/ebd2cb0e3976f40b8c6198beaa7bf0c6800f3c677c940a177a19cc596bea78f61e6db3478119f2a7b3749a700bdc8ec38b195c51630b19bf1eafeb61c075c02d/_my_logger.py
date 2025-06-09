import logging
import sys
logging_level = logging.INFO
logger = logging.getLogger(__name__)
logger.setLevel(logging_level)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging_level)
formatter = logging.Formatter('%(levelname)7s - %(filename)s %(funcName)s() line:%(lineno)d -- %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)