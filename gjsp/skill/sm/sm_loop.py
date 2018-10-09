import logging
import time

from gjsp.common import Windows
from gjsp.common.const_value import SmVal
from gjsp.common.utensil import millisecond
from gjsp.skill import SkillStatus, SkillLoop
from gjsp.skill.sm import SmLingLi, SmFuWen, SmSkill, SmDot

_logger = logging.getLogger("skill")


class SmSkillLoop(SkillLoop):

    def __init__(self, windows: Windows):
        super().__init__(windows)
        self.__ling_li: SmLingLi = SmLingLi()
        self.__skills: SmSkill = SmSkill(windows)
        self.__fu_wen: SmFuWen = SmFuWen()
        self.__dot: SmDot = SmDot()
        self.is_pve = True
        self.is_pvp = False

    def skill(self):
        return self.__skills

    def ling_li(self):
        return self.__ling_li

    def fu_wen(self):
        return self.__fu_wen

    def dot(self):
        return self.__dot

    def update(self, screen=None):
        start_time = millisecond()

        super().update(screen)
        super_time = millisecond()

        self.skill().update(self.screen())
        skill_time = millisecond()

        self.ling_li().update(self.screen())
        ling_li_time = millisecond()

        self.fu_wen().update(self.screen())
        self.dot().update(self.screen())
        end_time = millisecond()

        _logger.debug("update time :%s,super:%s, skill:%s, ll:%s, fu_wen:%s" %
                      (end_time - start_time,
                       super_time - start_time,
                       skill_time - super_time,
                       ling_li_time - skill_time,
                       end_time - ling_li_time))

    def auto_q(self):
        self.skill().q.just_down()

    def free_q(self):
        self.skill().q.just_up()

    ### status logic loop
    def start(self):
        self.skill().q.just_down()

        for i in range(4):
            self.skill().gun_si.freed()
            self.wait(0.2)

        self.wait(0.2)
        self.skill().min_si.freed()

    def normal(self):
        skill = self.skill()
        fu_wen = self.fu_wen()
        dot = self.dot()

        self.skill().q.just_up()
        self.wait(0.05)
        self.skill().q.just_down()

        if self.ling_li().score() < 50 and skill.ci_fu.is_ok():
            self.skill().ci_fu.freed()
            self.wait(0.2)
            skill.hong_guang_ci_fu.freed()
            return

        if fu_wen.is_wait() and skill.yu_hong.is_ok():
            self.wait()
            skill.yu_hong.freed()
            return

        if skill.gun_si.is_ok() or fu_wen.is_ok():
            skill.gun_si.freed()
            self.wait()

        if skill.min_si.is_ok() and self.exist_fu_wen(SmVal.img_fu_wen_gun_si):
            skill.min_si.freed()
            self.wait()

        if self.exist_buffer(SmVal.img_buff_qjwh):
            self.free_q()
            self.become(SkillStatus.Explosive)
            return

        if self.is_pvp:
            if skill.hong_guang.is_ok() or skill.hong_guang_free.is_ok() or skill.hong_guang_ci_fu.is_ok():
                skill.hong_guang.freed()

        if self.is_pve:
            if skill.hong_guang_free.is_ok():
                if dot.exist_ben_huai(1):
                    skill.hong_guang_free.freed()
                if skill.hong_guang_free.wait_time() > 3:
                    skill.hong_guang_free.freed()
                if not fu_wen.exist(SmVal.img_fu_wen_gun_si):
                    skill.hong_guang_free.freed()

            if skill.hong_guang_ci_fu.is_ok():
                skill.hong_guang_ci_fu.freed()

            if skill.hong_guang.is_ok() and dot.exist_ben_huai(1):
                skill.hong_guang.freed()

        if not self.exist_buffer(SmVal.img_buff_zu_fu) and (millisecond() - self.before_time > 1500):
            skill.e.freed()
            self.update_time()
            return

    def explosive(self):
        if self.exist_buffer(SmVal.img_buff_qjwh):
            self.skill().e.just_down()
        else:
            self.skill().e.just_up()
            self.become(SkillStatus.Normal)

    def clear(self):
        if self.status is not None:
            self.status = None
            time.sleep(0.1)
            self.free_q()
            print("clear")

    def pve(self):
        self.is_pve = True
        self.is_pvp = False
        self.update()
        if self.status is None:
            print("pve start")
            self.start_time = millisecond()
            self.skill().yu_hong.freed()
            self.wait(0.2)
        self.run()

    def pvp(self):
        self.is_pve = False
        self.is_pvp = True
        self.update()
        if self.status is None:
            if self.skill().jin_yu.is_ok():
                self.start_time = millisecond()
                self.skill().jin_yu.freed()
                self.wait(0.3)
                self.update()
                if self.exist_fu_wen(SmVal.img_fu_wen_jin_yu):
                    _logger.info("金羽 释放成功")
                    self.skill().hong_guang.freed()
                    self.run()
                else:
                    _logger.info("金羽 释放失败")
                return
        self.run()

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
