import logging
import time

_logger = logging.getLogger("even_loop")


class EvenLoop:
    def __init__(self, name, key):
        self.name = name
        self.__key = key
        self.is_run: bool = False

    def delay(self):
        time.sleep(0.1)

    def update(self):
        if self.is_run:
            self.set_stop()
        else:
            self.is_run = not self.is_run
        _logger.info("update : %s,%s,%s" % (self.name, self.key(), self.is_run))

    def set_stop(self):
        if self.is_run:
            self.is_run = False
            self.clear()
            logging.info("set stop %s" % (self.name))

    def key(self) -> str:
        return self.__key

    def run(self):
        pass

    def clear(self):
        pass
