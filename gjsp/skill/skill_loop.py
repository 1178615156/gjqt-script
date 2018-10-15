import logging
import time

from PIL.Image import Image
from functional import seq

from gjsp import Screen
from gjsp.common import Windows, FindPic
from gjsp.common.const_value import *
from gjsp.common.utensil import millisecond

_logger = logging.getLogger("skill")


class SkillLoop(Screen):
    def __init__(self, windows: Windows):
        super().__init__()
        self.start_time = millisecond()
        self.before_time = millisecond()
        self.windows: Windows = windows
        self.__skill = None
        self.exec_func = None

    def mouse_tap_if_need(self):
        # img = self.screen().crop(Area.mouse_tap)
        # if FindPic(original=img, goal=Global.img_mouse_left).isFind():
        #     print("mouse left click")
        #     self.windows.mouse_left_click()
        #     return True
        # if FindPic(original=img, goal=Global.img_mouse_right).isFind():
        #     print("mouse right click")
        #     self.windows.mouse_right_click()
        #     return True
        return False

    ### help func
    def update_time(self):
        self.before_time = millisecond()

    def wait(self, t=0.1):
        time.sleep(t)

    def random_wait(self):
        self.windows.random_wait()

    def become(self, exec_func):
        _logger.info("become :%s -> %s" % (self.exec_func, exec_func))
        self.exec_func = exec_func

    def is_doing_war_npc(self, screen: Image):
        return FindPic(
            original=screen.crop((0, 500, screen.width, screen.height)),
            goal=img_war_npc
        ).isFind()

    ### screen
    def update(self, screen=None):
        if screen is None:
            super().update(self.windows.screen_shot())
        else:
            super().update(screen)

        wait_update_attr = seq(vars(self).items()).filter(lambda x: isinstance(x[1], Screen)).to_list()
        exec_time = {}
        for name, value in wait_update_attr:
            start_time = millisecond()
            value.update(self.screen())
            exec_time[name] = millisecond() - start_time
        _logger.info("update time -- %s" % (str(exec_time)))

    def clear(self):
        pass

    def run(self):
        pass

    def exist_buffer(self, img):
        return FindPic(original=self.screen().crop(area_buff), goal=img).isFind()

    def exist_skill(self, img):
        return FindPic(original=self.screen().crop(area_skill), goal=img, sim=0.99).isFind()

    def exist_fu_wen(self, img):
        return FindPic(original=self.screen().crop(area_fu_wen), goal=img).isFind()
