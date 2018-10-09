from gjsp import Screen
from gjsp.common import FindPic
from gjsp.common.const_value import *


class SmFuWen(Screen):

    def is_ok(self) -> bool:
        return self.exist(SmVal.img_fu_wen_empty) or self.exist(SmVal.img_fu_wen_empty_plus)

    def is_wait(self) -> bool:
        return self.exist(SmVal.img_fu_wen_wait)

    def exist(self, img):
        return FindPic(original=self.screen().crop(area_fu_wen), goal=img).isFind()
