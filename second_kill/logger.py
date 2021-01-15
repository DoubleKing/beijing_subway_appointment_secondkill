import logging
import logging.handlers

LOG_FILENAME = './secondkill.log'
g_logger = logging.getLogger()


def set_logger():
    g_logger.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s ]- %(process)d-%(threadName)s - '
                                  '%(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    g_logger.addHandler(console_handler)
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILENAME, maxBytes=10485760, backupCount=5, encoding="utf-8")
    file_handler.setFormatter(formatter)
    g_logger.addHandler(file_handler)


set_logger()
