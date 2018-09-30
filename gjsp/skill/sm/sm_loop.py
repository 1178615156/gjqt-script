import logging
import time

from gjsp.common import Windows
from gjsp.common.const_value import SmVal
from gjsp.common.utensil import millisecond
from gjsp.skill import SkillStatus, SkillLoop
from gjsp.skill.sm import SmLingLi, SmFuWen, SmSkill

_logger = logging.getLogger("skill")


class SmSkillLoop(SkillLoop):

    def __init__(self, windows: Windows):
        super().__init__(windows)
        self.__ling_li: SmLingLi = SmLingLi()
        self.__skills: SmSkill = SmSkill(windows)
        self.__fu_wen: SmFuWen = SmFuWen()

    def skill(self):
        return self.__skills

    def ling_li(self):
        return self.__ling_li

    def fu_wen(self):
        return self.__fu_wen

    def update(self, screen=None):
        start_time = millisecond()
        super().update(screen)
        super_time = millisecond()
        self.skill().update(self.screen())
        skill_time = millisecond()
        self.ling_li().update(self.screen())
        ling_li_time = millisecond()
        self.fu_wen().update(self.screen())
        end_time = millisecond()
        _logger.debug("update time :%s,super:%s, skill:%s, ll:%s, fu_wen:%s" %
                      (end_time - start_time,
                       super_time-start_time,
                       skill_time-super_time,
                       ling_li_time-skill_time,
                       end_time-ling_li_time))

    ### status logic loop
    def start(self):
        for i in range(5):
            self.skill().gun_si.freed()
            self.wait(0.15)
        self.skill().min_si.freed()

    def normal(self):
        skill = self.skill()
        fu_wen = self.fu_wen()

        if self.exist_buffer(SmVal.img_buff_zu_fu):
            _logger.info("exist ci fu ,wait 0.3")
            self.wait(0.3)

        if self.ling_li().score() < 15 and self.skill().ci_fu.is_ok():
            self.skill().ci_fu.freed()
            self.wait(0.4)
            return

        if self.fu_wen().is_wait():
            self.wait()
            self.skill().yu_hong.freed()

        if self.fu_wen().is_ok():
            self.wait()
            self.skill().gun_si.freed()

        if skill.hong_guang.is_ok() or self.exist_buffer(SmVal.img_buff_liu_guang):
            skill.hong_guang.freed()
            self.wait()

        if skill.min_si.is_ok() and self.exist_fu_wen(SmVal.img_fu_wen_some):
            skill.min_si.freed()

        if not self.exist_buffer(SmVal.img_buff_zu_fu) and (millisecond() - self.before_time > 1500):
            skill.e.freed()

        if self.exist_buffer(SmVal.img_buff_qjwh):
            self.become(SkillStatus.Explosive)

    def explosive(self):
        if self.exist_buffer(SmVal.img_buff_qjwh):
            self.skill().e.freed()
        else:
            self.become(SkillStatus.Normal)

    def clear(self):
        if self.status is not None:
            self.status = None
            time.sleep(0.1)
            self.windows.key_press("q")
            print("clear")

    def pve(self):
        # _logger.debug("run - start")
        if self.status is None:
            print("pve start")
            self.windows.key_down("q")
            time.sleep(2.2)
            self.windows.key_up("q")
        self.update()
        self.run()
        # _logger.debug("run - end")

    def pvp(self):
        self.update()
        if self.status is not None:
            self.run()
            return
        if self.skill().jin_yu.is_ok():
            self.skill().jin_yu.freed()
            self.wait(0.3)
            self.update()
            if self.exist_fu_wen(SmVal.img_fu_wen_jin_yu):
                _logger.info("金羽 释放成功")
                self.skill().hong_guang.freed()
                self.run()
            else:
                _logger.info("金羽 释放失败")

    def run(self):
        if self.mouse_tap_if_need():
            logging.info("mouse tap")
            return

        elif self.status is None:
            self.become(SkillStatus.Start)

        elif self.status is SkillStatus.Start:
            self.start()
            self.become(SkillStatus.Normal)

        elif self.status is SkillStatus.Normal:
            self.normal()

        elif self.status is SkillStatus.Explosive:
            self.explosive()
