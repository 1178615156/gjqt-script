import numpy as np
from gjsp.common.const_value import SmVal
from gjsp.skill.ling_li import LingLi
from gjsp.common import FindPic
import logging


class SmLingLi(LingLi):
    # ling_li_default_color = np.array([52, 215, 242], dtype="uint8")
    # area_ling_li = (444, 898, 750, 913)

    def __init__(self):
        super().__init__()
        self.area = None
        self.__logger = logging.getLogger("sm-ling-li")
        a, b = (115.31076412, 2.00410678)
        self.a = a
        self.b = b

    def update_after(self):
        if self.area is None:
            screen = self.screen()
            screen = screen.crop((0, 0, int(screen.width / 2), screen.height))
            fp = FindPic(screen, SmVal.ling_li_word, sim=0.92)
            if fp.isFind():
                x, y = fp.maxPoint()
                self.area = (x - 6, y, x - 6 + 306, y + 15)
                self.__logger.info("find ling li area %s" % (str(self.area)))
            else:
                self.__logger.info(str({
                    "max point": fp.maxPoint(),
                    "max value": fp.maxValue()
                }))

    @staticmethod
    def pretreatment(img):
        r, g, b = img.split()
        b = np.array(b)
        b = b > 190
        b = b * 255
        return b

    @staticmethod
    def area_size(img):
        x = SmLingLi.pretreatment(img)
        return np.count_nonzero(x) / x.size

    def score(self):
        if self.area is None:
            self.__logger.info("area is none ,just return 100")
            return 100
        else:
            x = self.area_size(self.screen().crop(self.area))
            a = self.a
            b = self.b
            return a * x + b
