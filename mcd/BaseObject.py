import logging


class BaseObject(object):
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(self.__module__ + '.' + self.__class__.__qualname__)
        self.logger.debug(self.logger)
