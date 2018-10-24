import logging

from gjsp.common import Windows
from gjsp.common.const_value import SmVal
from gjsp.common.utensil import millisecond
from gjsp.skill import SkillLoop
from gjsp.skill.sm import SmLingLi, SmSkill, SmFuWen, SmDot
from enum import IntEnum


class Status(IntEnum):
    Start = 0
    Normal = 1
    Explosive = 2
    WaitLingLi = 3
    HongGuang = 4
    CiFu = 5


class SmSkillLoopFsmPve(SkillLoop):
    def __init__(self, windows: Windows):
        super().__init__(windows)
        self.__ling_li = SmLingLi()
        self.__skills = SmSkill(windows)
        self.__fu_wen = SmFuWen()
        self.__dot = SmDot()
        self._logger = logging.getLogger("sm-skill")
        self.is_test = False
        self.ci_fu_ling_li = 48
        self.status_value = 0
        self.init_status(Status.Start)

        self.add_action(Status.Start, self.action_start)
        self.add_action(Status.WaitLingLi, self.action_wait_ling_li)
        self.add_action(Status.Normal, self.action_normal)
        self.add_action(Status.Explosive, self.action_explosive)
        self.add_action(Status.CiFu, self.action_ci_fu)

        self.add_transform([Status.Normal, Status.CiFu,Status.WaitLingLi], Status.Explosive, self.transform_any_2_explosive)
        self.add_transform(Status.Normal, Status.CiFu, self.transform_normal_2_ci_fu)

    def skill(self) -> SmSkill:
        return self.__skills

    def ling_li(self) -> SmLingLi:
        return self.__ling_li

    def fu_wen(self) -> SmFuWen:
        return self.__fu_wen

    def dot(self) -> SmDot:
        return self.__dot

    def ka_dao(self):
        self.wait(0.2)

    def action_start(self):
        while self.fu_wen().is_ok():
            self.skill().gun_si.freed()
            self.wait(0.1)
            self.update()
        self.become(Status.Normal)

    def action_wait_ling_li(self):
        n = self.status_value
        if self.ling_li().score() < n:
            self.skill().q.auto()
            self.freed_default_skill()
        else:
            self.status_value = 0
            self.logger().info("wait ling li " + str(n))
            self.un_become()

    def action_normal(self):
        skill = self.skill()
        skill.q.auto()
        self.freed_default_skill()
        self.freed_hong_guang()

        if skill.hong_guang_mei_lan.is_ok():
            self.status_value = 25
            self.become(Status.WaitLingLi)
        elif skill.ci_fu.is_ok():
            if self.ling_li().score() > self.ci_fu_ling_li:
                self.become(Status.CiFu)
            else:
                self.status_value = self.ci_fu_ling_li
                self.become(Status.WaitLingLi)
        elif self.ling_li().score() <= 25 and millisecond() - self.before_time > 1500:
            skill.e.freed()
            self.update_time()
        elif self.ling_li().score() > 25 and millisecond() - self.before_time > 1000:
            skill.e.freed()
            self.update_time()
        else:
            pass

    def action_explosive(self):
        if self.exist_buffer(SmVal.buff_qjwh):
            if self.ling_li().score() < 15:
                self.skill().e.free_auto()
                self.skill().q.freed()
            else:
                self.skill().e.auto()
        else:
            self.skill().e.free_auto()
            self.become(Status.Normal)

    def freed_hong_guang(self):
        skill = self.skill()
        fu_wen = self.fu_wen()
        dot = self.dot()

        if skill.hong_guang_ci_fu.is_ok():
            skill.hong_guang_ci_fu.freed()
        elif skill.hong_guang_free.is_ok():
            if dot.exist_ben_huai(1):
                skill.hong_guang_free.freed()
            if skill.hong_guang_free.wait_time() > 3:
                skill.hong_guang_free.freed()
            if not fu_wen.exist(SmVal.img_fu_wen_gun_si):
                skill.hong_guang_free.freed()
        elif skill.hong_guang.is_ok():
            if dot.exist_ben_huai(1):
                skill.hong_guang_free.freed()
            if not fu_wen.exist(SmVal.img_fu_wen_gun_si):
                skill.hong_guang_free.freed()

    def action_ci_fu(self):
        skill = self.skill()
        if self.exist_buffer(SmVal.buff_qjwh):
            self.become(Status.Explosive)
        elif skill.hong_guang_ci_fu.is_ok():
            skill.hong_guang_ci_fu.freed()
        elif skill.hong_guang_free.is_ok():
            skill.hong_guang_free.freed()
            self.wait(0.3)
        else:
            skill.q.auto()
            self.un_become()

    def transform_normal_2_ci_fu(self):
        skill = self.skill()
        skill.q.free_auto()
        skill.ci_fu.freed()
        self.wait(0.6)

    def transform_any_2_explosive(self):
        skill = self.skill()
        skill.q.free_auto()
        self.windows.key_up("shift")
        skill.e.auto()

    def freed_default_skill(self):
        skill = self.skill()
        fu_wen = self.fu_wen()
        dot = self.dot()
        if fu_wen.is_wait() and skill.yu_hong.is_ok():
            skill.yu_hong.freed()
            skill.gun_si.freed()

        if skill.gun_si.is_ok() or fu_wen.is_ok():
            skill.gun_si.freed()
            self.wait()

        if skill.min_si.is_ok() and self.exist_fu_wen(SmVal.img_fu_wen_gun_si):
            skill.min_si.freed()
            self.wait()

        if skill.hong_guang_free.is_ok() and dot.exist_ben_huai(1):
            skill.hong_guang_free.freed()

        if self.exist_buffer(SmVal.buff_qjwh):
            self.become(Status.Explosive)
            return

    def clear(self):
        super().clear()
        self.skill().q.free_auto()
        self.delay()
        self.windows.key_press("5")
        self.delay()
        self.skill().q.free_auto()
        self.delay()
        self.windows.key_press("5")


class SmSkillLoopFsmPvp(SmSkillLoopFsmPve):
    def action_start(self):
        self.skill().q.auto()
        if self.skill().jin_yu.is_ok():
            self.skill().jin_yu.freed()
            self.wait(0.15)
            self.update()
            if self.exist_fu_wen(SmVal.img_fu_wen_jin_yu):
                self.logger().info("金羽 释放成功")
                self.skill().hong_guang.freed()
                super().action_start()
            else:
                self.logger().info("金羽 释放失败")

    def freed_hong_guang(self):
        skill = self.skill()

        if skill.hong_guang_ci_fu.is_ok():
            skill.hong_guang_ci_fu.freed()
        elif skill.hong_guang_free.is_ok():
            skill.hong_guang_free.freed()
        elif skill.hong_guang.is_ok():
            skill.hong_guang_free.freed()
