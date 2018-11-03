import logging
from abc import ABCMeta, abstractmethod

from gjsp import AreaScreen
from gjsp.common import FindPic
from gjsp.common.const_value import *
import numpy as np


class SmFuWen(AreaScreen):
    def __init__(self):
        super().__init__()
        self.__logger = logging.getLogger("sm-fu-wen")
        self.__fu_wen = None

        self.fu_wen_pos_1 = 30, 28
        self.fu_wen_pos_2 = 66, 9
        self.fu_wen_pos_3 = 102, 28

        self.wait_fu_wen_1 = None
        self.wait_fu_wen_2 = None
        self.wait_fu_wen_3 = None

    def color_is_yellow(self, color):
        yellow = np.array([244.33333333, 206.66666667, 76.33333333])
        return np.count_nonzero(np.abs(yellow - color) < 15) == 3

    def update_after(self):
        super().update_after()
        self.__fu_wen = self.screen().crop(self.area())

        self.wait_fu_wen_1 = self.color_is_yellow(self.__fu_wen.getpixel(self.fu_wen_pos_1))
        self.wait_fu_wen_2 = self.color_is_yellow(self.__fu_wen.getpixel(self.fu_wen_pos_2))
        self.wait_fu_wen_3 = self.color_is_yellow(self.__fu_wen.getpixel(self.fu_wen_pos_3))

    def icon(self):
        return SmVal.fu_wen_icon

    def func(self, x, y):
        return (x - 50, y - 50, x + 80, y - 80 + 150)

    def is_ok(self) -> bool:
        return self.exist(SmVal.img_fu_wen_empty) or self.exist(SmVal.img_fu_wen_empty_plus)

    def is_wait(self) -> bool:
        return self.wait_fu_wen_1 or self.wait_fu_wen_2 or self.wait_fu_wen_3

    def exist(self, img):
        return FindPic(original=self.__fu_wen, goal=img).isFind()
