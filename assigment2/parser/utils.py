import logging

logging.basicConfig(
    filename="sample.log",
    level='INFO',
    format='[%(asctime)s] %(filename)s: %(levelname)-8s %(message)s'
)


class Logger:
    def __init__(self, name):
        self.log = logging.getLogger(name)

    def set_logger_level(self, s):
        return self.log.setLevel(s)

    def logger_info_message(self, s):
        return self.log.info(s)

    def logger_warning_message(self, s):
        return self.log.warning(s)

    def logger_critical_message(self, s):
        return self.log.critical(s)
