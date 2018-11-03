import logging

from gjsp import Screen
from gjsp.common import FindPic

from abc import ABCMeta, abstractmethod


class AreaScreen(Screen,metaclass=ABCMeta):
    def __init__(self):
        super().__init__()
        self.__area = None
        self.__name = self.__class__.__name__
        self.__logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def icon(self):
        pass

    @abstractmethod
    def func(self, x, y) -> (int, int, int, int):
        pass
    def area(self):
        return self.__area

    def update_after(self):
        if self.__area is None:
            screen = self.screen()
            fp = FindPic(screen, self.icon())
            if fp.isFind():
                x, y = fp.maxPoint()
                self.__area = self.func(x, y)
                self.__logger.info("find %s area %s" % (self.__name, str(self.__area)))
            else:
                self.__logger.info(str({
                    "max point": fp.maxPoint(),
                    "max value": fp.maxValue()
                }))
