import time

from PIL.Image import Image

from gjsp.common.utensil import goal_image, millisecond
from gjsp.common import Windows, FindPic
from gjsp.skill import SkillStatus
import logging

logger = logging.getLogger("skill")


class SkillLoop:
    area_fu_wen = (800, 800, 1000, 1080)
    area_buff = (400, 800, 850, 900)
    area_skill = (5, 645, 400, 686)
    area_mouse_tap = (1000, 400, 1300, 600)
    img_war_npc = goal_image("war_npc.bmp")
    img_mouse_left = goal_image("mouse_left.bmp")
    img_mouse_right = goal_image("mouse_right.bmp")

    def __init__(self, windows: Windows):
        self.start_time = millisecond()
        self.before_time = millisecond()
        self.status: SkillStatus = None
        self.windows: Windows = windows
        self._screen: Image = None
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
            goal=self.img_war_npc
        ).isFind()

    ### screen
    def update_screen(self, screen=None):
        if screen is None:
            self._screen = self.windows.screen_shot()
        else:
            self._screen = screen

        self.update_after_screen()

    def screen(self) -> Image:
        return self._screen

    def update_after_screen(self):
        pass

    def clear(self):
        pass

    def run(self):
        pass

    def pvp(self):
        self.run()

    def pve(self):
        self.run()

    def exist_buffer(self, img):
        return FindPic(original=self.screen().crop(self.area_buff), goal=img).isFind()

    def exist_skill(self, img):
        return FindPic(original=self.screen().crop(self.area_skill), goal=img, sim=0.99).isFind()

    def exist_fu_wen(self, img):
        return FindPic(original=self.screen().crop(self.area_fu_wen), goal=img).isFind()
