import logging
import time

from functional import seq

from gjsp.common import Windows
from gjsp.common.const_value import SmVal
from gjsp.common.utensil import millisecond
from gjsp.skill import SkillLoop
from gjsp.skill.sm import SmLingLi, SmFuWen, SmSkill, SmDot

_logger = logging.getLogger("skill")


class SmSkillLoop(SkillLoop):

    def __init__(self, windows: Windows):
        super().__init__(windows)
        self.__ling_li = SmLingLi()
        self.__skills = SmSkill(windows)
        self.__fu_wen = SmFuWen()
        self.__dot = SmDot()
        self._logger = _logger
        self.is_test = False
        self.ci_fu_ling_li = 48

    def test(self):
        self.update()

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

    def freed_hong_guang(self):
        skill = self.skill()
        fu_wen = self.fu_wen()
        dot = self.dot()
        condition = lambda: seq(
            dot.exist_ben_huai(1),
            skill.hong_guang_free.wait_time() > 3,
            (not fu_wen.exist(SmVal.img_fu_wen_gun_si)))

        def hong_guang_after():
            self.wait(1.1)
            self.update()

        if skill.hong_guang_ci_fu.is_ok():
            skill.hong_guang_ci_fu.freed()
            hong_guang_after()

        if skill.hong_guang_free.is_ok():
            if condition().exists(lambda x: x):
                skill.hong_guang_free.freed()
                hong_guang_after()

        if self.skill().hong_guang_mei_lan.is_ok():
            _logger.info("hong guan mei lan wait to 25")
            self.wait_ling_li_to(25)
            self.freed_hong_guang()
            return

        if skill.hong_guang.is_ok():
            if condition().exists(lambda x: x):
                skill.hong_guang.freed()
                hong_guang_after()

    def freed_e(self):
        skill = self.skill()

        if millisecond() - self.before_time > 1300:
            skill.e.freed()
            self.update_time()
            return

    def freed_ci_fu(self):
        skill = self.skill()
        skill.q.free_auto()
        self.random_wait()
        skill.ci_fu.freed()
        self.wait(0.6)
        while True:
            self.update()
            if self.skill().hong_guang_ci_fu.is_ok():
                self.skill().hong_guang_ci_fu.freed()
                self.wait(0.2)
            elif self.skill().hong_guang_free.is_ok():
                self.skill().hong_guang_free.freed()
                self.wait(0.2)
            elif self.exist_buffer(SmVal.buff_zu_fu):
                self.skill().q.auto()
                self.wait(0.2)
            else:
                skill.q.auto()
                self._logger.info("freed ci fu - end ")
                return

    def wait_ling_li_to(self, n):
        while self.ling_li().score() < n and self.exec_func == self.normal:
            self.skill().q.auto()
            self.freed_default_skill()
            self.update()
            self.wait()
        _logger.info("wait ling li to %s" % (n))

    def start(self):
        while self.fu_wen().is_ok():
            self.skill().gun_si.freed()
            self.wait(0.1)
            self.update()
        self.become(self.normal)

    def freed_default_skill(self):
        skill = self.skill()
        fu_wen = self.fu_wen()

        if fu_wen.is_wait() and skill.yu_hong.is_ok():
            self.wait()
            skill.yu_hong.freed()
            self.wait()
            skill.gun_si.freed()
            return

        if skill.gun_si.is_ok() or fu_wen.is_ok():
            skill.gun_si.freed()
            self.wait()

        if skill.min_si.is_ok() and self.exist_fu_wen(SmVal.img_fu_wen_gun_si):
            skill.min_si.freed()
            self.wait()

        if self.exist_buffer(SmVal.buff_qjwh):
            self.become(self.explosive)
            skill.q.free_auto()
            self.windows.key_up("shift")
            skill.e.auto()
            return

    def normal(self):
        skill = self.skill()
        fu_wen = self.fu_wen()
        skill.q.auto()

        self.freed_default_skill()

        if skill.ci_fu.is_ok():
            self.wait_ling_li_to(self.ci_fu_ling_li)
            if self.exec_func == self.explosive:
                return
            self.freed_ci_fu()

        self.freed_hong_guang()
        self.freed_e()

    def explosive(self):
        if self.exist_buffer(SmVal.buff_qjwh):
            if self.ling_li().score() < 15:
                self.skill().q.freed()
            else:
                self.skill().e.auto()
                time.sleep(0.2)
        else:
            self.skill().e.just_up()
            self.become(self.normal)

    def clear(self):
        if self.exec_func is not None:
            self.exec_func = None
            time.sleep(0.1)
            self.skill().q.free_auto()
            print("clear")

    def run(self):
        if self.is_test:
            self.test()
            return
        if self.exec_func is None:
            self.start_time = millisecond()
            self.become(self.start)
        else:
            self.update()
            self.exec_func()
        time.sleep(0.2)
