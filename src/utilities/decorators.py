import logging
from functools import wraps
import psutil
import time
import datetime
from alf_fw import alf_assets

loggers = {}


def init_log(filename, subdir):
    log_f = f'{subdir}_{filename}'
    if log_f in loggers:
        return loggers[log_f]

    logger = logging.getLogger(log_f)
    # Create handlers
    log_file = alf_assets.get_file_path(f'{filename}.csv', alf_assets.get_assets_dir('decorators', subdir))
    # [RotatingFileHandler(filename=track_file, mode='w', maxBytes=512, backupCount=4)]
    f_handler = logging.FileHandler(log_file)

    f_handler.setLevel(logging.INFO)

    # Create formatters and add it to handlers
    f_format = logging.Formatter('%(message)s')
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(f_handler)

    loggers[log_f] = logger

    return logger


def tracking_timer(f):
    """
    Decorator provides timer
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        before_time = time.time()
        result = f(*args, **kwargs)
        after_time = time.time()
        print("Timer (s): ", (after_time - before_time))
        return result

    return wrapper
