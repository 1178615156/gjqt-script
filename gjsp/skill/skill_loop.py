import logging
import time

from PIL.Image import Image

from gjsp import Screen
from gjsp.common import Windows, FindPic
from gjsp.common.utensil import millisecond
from gjsp.skill import skill_status
from gjsp.common.const_value import *

logger = logging.getLogger("skill")


class SkillLoop(Screen):
    def __init__(self, windows: Windows):
        super().__init__()
        self.start_time = millisecond()
        self.before_time = millisecond()
        self.status: skill_status = None
        self.windows: Windows = windows
        self.__skill = None

    def mouse_tap_if_need(self):
        # img = self.screen().crop(self.area_mouse_tap)
        # # img.save( user_dir +"image_tmp\\%s.jpg" %(millisecond()))
        # if FindPic(original=img, goal=self.img_mouse_left).isFind():
        #     print("mouse left click")
        #     self.windows.mouse_left_click()
        #     return True
        # if FindPic(original=img, goal=self.img_mouse_right).isFind():
        #     print("mouse right click")
        #     self.windows.mouse_right_click()
        #     return True
        return False

    ### help func
    def update_time(self):
        self.before_time = millisecond()

    def check(self, s):
        assert self.status == s, "expect:%s actual:%s" % (s, self.status)

    def wait(self, t=0.1):
        time.sleep(t)

    def become(self, status):
        logger.info("become :%s -> %s" % (self.status, status))
        self.status = status

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

    def clear(self):
        pass

    def run(self):
        pass

    def pvp(self):
        self.run()

    def pve(self):
        self.run()

    def exist_buffer(self, img):
        return FindPic(original=self.screen().crop(area_buff), goal=img).isFind()

    def exist_skill(self, img):
        return FindPic(original=self.screen().crop(area_skill), goal=img, sim=0.99).isFind()

    def exist_fu_wen(self, img):
        return FindPic(original=self.screen().crop(area_fu_wen), goal=img).isFind()
