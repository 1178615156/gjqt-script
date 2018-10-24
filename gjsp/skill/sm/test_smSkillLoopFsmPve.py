from unittest import TestCase
from gjsp.common import WindowsBuild,get_gjqt_hwnd
from gjsp.skill.sm.sm_skill_loop_fsm import SmSkillLoopFsmPve

import logging
logging.basicConfig(level=logging.INFO)
class TestSmSkillLoopFsmPve(TestCase):
    windows = WindowsBuild().build()
    windows.init(get_gjqt_hwnd(windows))
    obj = SmSkillLoopFsmPve(windows)

    def test_ling_li(self):
        obj = self.obj
        obj.update()
        print(obj.ling_li().score())
        print(obj.ling_li().area)
