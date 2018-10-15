from gjsp.common.const_value import SmVal
from gjsp.skill.sm.sm_loop import SmSkillLoop, _logger


class SmSkillLoopPvp(SmSkillLoop):
    def start(self):
        self.skill().q.auto()
        if self.skill().jin_yu.is_ok():
            self.skill().jin_yu.freed()
            self.wait(0.15)
            self.update()
            if self.exist_fu_wen(SmVal.img_fu_wen_jin_yu):
                _logger.info("金羽 释放成功")
                self.skill().hong_guang.freed()
                super().start()
            else:
                _logger.info("金羽 释放失败")

    def freed_ci_fu(self):
        self.skill().ci_fu.freed()

    def freed_hong_guang(self):
        skill = self.skill()
        if skill.hong_guang.is_ok() or skill.hong_guang_free.is_ok() or skill.hong_guang_ci_fu.is_ok():
            skill.hong_guang.freed()
            self.wait(0.5)
