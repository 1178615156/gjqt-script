from gjsp import Screen
from gjsp.common import FindPic
from gjsp.common.const_value import *


class SmFuWen(Screen):

    def is_ok(self) -> bool:
        img = self.screen().crop(area_fu_wen)
        x1 = FindPic(original=img, goal=SmVal.img_fu_wen_empty).isFind()
        x2 = FindPic(original=img, goal=SmVal.img_fu_wen_empty_plus).isFind()
        return x1 or x2

    def is_wait(self) -> bool:
        return FindPic(original=self.screen().crop(area_fu_wen), goal=SmVal.img_fu_wen_wait).isFind()

    def exist(self, img):
        return FindPic(original=self.screen().crop(area_fu_wen), goal=img).isFind()
