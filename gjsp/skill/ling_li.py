import numpy as np

ling_li_default_color = np.array([52, 215, 242], dtype="uint8")
area_ling_li = (440, 895, 750, 915)
a, b = (274.635922330097, -98.74029126213588)


class LingLi:
    def score(self, screen) -> int: pass


class LingLiSiMing(LingLi):
    def ling_li_pretreatment(self, img):
        x = np.array(img) - ling_li_default_color
        x = np.mean(x, axis=2)
        x = (x - np.min(x)) / (np.max(x) - np.min(x))
        x = x > 0.4
        x = x * 255
        x = x.astype("uint8")
        return x

    def area_size(self, img):
        x = self.ling_li_pretreatment(img)
        return np.count_nonzero(x) / x.size

    def score(self, screen):
        x = self.area_size(screen.crop(area_ling_li))
        return a * x + b
