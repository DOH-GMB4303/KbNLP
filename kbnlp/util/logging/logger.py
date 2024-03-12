import logging
from logging import FileHandler, StreamHandler

import kbnlp.configs as cfg
def init_logger():
    if "logger" in globals():
        return "Logger already initialized"

    logger = logging.getLogger('kbnlp')
    format = logging.Formatter("[%(asctime)s] %(name)s : %(levelname)s -- %(message)s")
    logger.setLevel(logging.DEBUG)

    fh = FileHandler(cfg.LOG_FILE, mode='w')
    sh = StreamHandler()

    fh.setFormatter(format)
    sh.setFormatter(format)

    fh.setLevel('DEBUG')
    sh.setLevel('INFO')

    logger.addHandler(fh)
    logger.addHandler(sh)