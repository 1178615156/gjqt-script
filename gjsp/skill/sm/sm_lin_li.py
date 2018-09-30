import numpy as np

from gjsp.skill.ling_li import LingLi


class SmLingLi(LingLi):
    area_ling_li = (440, 895, 750, 915)
    a, b = (274.635922330097, -98.74029126213588)

    def ling_li_pretreatment(self, img):
        x = np.array(img) - self.ling_li_default_color
        x = np.mean(x, axis=2)
        x = (x - np.min(x)) / (np.max(x) - np.min(x))
        x = x > 0.4
        x = x * 255
        x = x.astype("uint8")
        return x

    def area_size(self, img):
        x = self.ling_li_pretreatment(img)
        return np.count_nonzero(x) / x.size

    def score(self):
        x = self.area_size(self.screen().crop(self.area_ling_li))
        a = self.a
        b = self.b
        return a * x + b
