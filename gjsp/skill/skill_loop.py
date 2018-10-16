import logging

from functional import seq

from gjsp import Screen
from gjsp.common import Windows, FindPic
from gjsp.common.const_value import area_buff, area_skill, area_fu_wen
from gjsp.common.utensil import millisecond
from gjsp.skill.fsm import FSM


class SkillLoop(FSM, Screen):
    def __init__(self, windows):
        super().__init__()
        self.windows: Windows = windows
        self.start_time = millisecond()
        self.before_time = millisecond()
        self._logger = logging.getLogger("skill")

    def logger(self):
        return self._logger

    def update_time(self):
        self.before_time = millisecond()

    def wait(self, t=0.1):
        self.windows.wait(t)

    def random_wait(self):
        self.windows.random_wait()

    def delay(self):
        self.wait(0.15)

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
            exec_time[name.replace(self.__class__.__name__, "")] = millisecond() - start_time
        self.logger().info("update time -- %s" % (str(exec_time)))

    def exist_buffer(self, img):
        return FindPic(original=self.screen().crop(area_buff), goal=img).isFind()

    def exist_skill(self, img):
        return FindPic(original=self.screen().crop(area_skill), goal=img, sim=0.99).isFind()

    def exist_fu_wen(self, img):
        return FindPic(original=self.screen().crop(area_fu_wen), goal=img).isFind()

    def run(self):
        self.update()
        super().run()
        self.delay()
