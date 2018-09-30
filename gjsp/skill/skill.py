from gjsp.common.find_pic import FindPic
from gjsp.common import Windows
from functools import reduce
from PIL.Image import Image
import logging
from gjsp import Screen

_logger = logging.getLogger("skill")


class Skill(Screen):
    def __init__(self, name, key, windows: Windows, icons=None):
        super().__init__()
        self.__name = name
        self.__key = key
        self.__windows = windows
        self.__icons = self.process_icons(icons)
        self.__result = None

    def process_icons(self, icons):
        if icons is None:
            return None
        if type(icons) is Image:
            icons = [icons]
        assert type(icons) is list
        return icons

    def icons(self):
        assert self.__icons is not None
        return self.__icons

    def key(self):
        return self.__key

    def name(self):
        return self.__name

    def update(self, screen):
        super().update(screen)
        if self.__icons is not None:
            self.__result = reduce(
                lambda l, r: l or r,
                map(lambda e: FindPic(self.screen(), e, sim=0.95).isFind(), self.icons()))

    def is_ok(self) -> bool:
        return self.__result

    def freed(self):
        _logger.info("freed:%s - %s" % (self.name(), self.key()))
        self.__windows.key_press(self.key())
