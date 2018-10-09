from gjsp import Screen
from gjsp.common import FindPic
from gjsp.common.const_value import SmVal, Area


class SmDot(Screen):
    def __init__(self):
        super().__init__()

    def ben_huai_1(self):
        return self.exist(SmVal.dot_ben_huai_1)

    def ben_huai_2(self):
        return self.exist(SmVal.dot_ben_huai_2)

    def ben_huai_3(self):
        return self.exist(SmVal.dot_ben_huai_3)

    def ben_huai_4(self):
        return self.exist(SmVal.dot_ben_huai_4)

    def exist_ben_huai(self, n: int):
        if n == 1:
            return self.ben_huai_1() or self.ben_huai_2() or self.ben_huai_3() or self.ben_huai_4()
        elif n == 2:
            return self.ben_huai_2() or self.ben_huai_3() or self.ben_huai_4()
        elif n == 3:
            return self.ben_huai_3() or self.ben_huai_4()
        elif n == 4:
            return self.ben_huai_4()
        else:
            assert False, "number error %s" % (n)

    def exist(self, img):
        return FindPic(original=self.screen().crop(Area.dot), goal=img).isFind()
