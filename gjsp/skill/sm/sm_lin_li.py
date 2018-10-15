import numpy as np

from gjsp.skill.ling_li import LingLi


class SmLingLi(LingLi):
    area_ling_li = (444, 898, 750, 913)
    a, b = (115.31076412, 2.00410678)

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
        x = self.area_size(self.screen().crop(self.area_ling_li))
        a = self.a
        b = self.b
        return a * x + b
