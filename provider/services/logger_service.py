import logging
import sys


class LoggerService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.set_logger()

    def set_logger(self):
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)

    def info(self):
        self.logger.info("started logging")
