from gjsp.common.find_pic import FindPic
from gjsp.common import Windows
from functools import reduce
from PIL.Image import Image
import logging
from gjsp import Screen
from gjsp.common.utensil import millisecond
from functional import seq

_logger = logging.getLogger("skill")


class Skill(Screen):
    def __init__(self, name, key, windows: Windows, icons=None):
        super().__init__()
        self.__name = name
        self.__key = key
        self.__windows = windows
        self.__icons = self.process_icons(icons)
        self.__ok = None
        self.__first_ok_time = None
        self.__ok_time = None

    def process_icons(self, icons):
        if icons is None:
            return None
        if not type(icons) is list:
            icons = [icons]
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
        if self.icons() is None:
            return
        result = seq(self.icons()).map(lambda e: FindPic(self.screen(), e, sim=0.99).isFind()).exists(lambda x: x)
        if not result and self.__ok and (millisecond() - self.__ok_time < 1500):
            pass
        elif not result:
            self.__ok = result
            self.__ok_time = None
            self.__first_ok_time = None
        elif result and self.__ok:
            self.__ok_time = millisecond()
        elif result and not self.__ok:
            self.__ok = result
            self.__ok_time = millisecond()
            self.__first_ok_time = millisecond()

    def is_ok(self) -> bool:
        return self.__ok

    def wait_time(self):
        if self.__first_ok_time is None:
            return 0
        else:
            return (millisecond() - self.__first_ok_time) / 1000

    def freed(self):
        _logger.info("freed:%s - %s" % (self.name(), self.key()))
        self.__windows.key_press(self.key())
        self.__windows.wait(0.05)
        self.__ok = None
        self.__first_ok_time = None

    def just_down(self):
        _logger.info("down:%s - %s" % (self.name(), self.key()))
        self.__windows.key_down(self.key())
        self.__windows.wait(0.05)
        self.__ok = None
        self.__first_ok_time = None

    def just_up(self):
        _logger.info("up:%s - %s" % (self.name(), self.key()))
        self.__windows.key_up(self.key())
        self.__windows.wait(0.05)

    def auto(self):
        self.just_up()
        self.__windows.wait(0.05)
        self.just_down()

    def free_auto(self):
        self.just_up()
