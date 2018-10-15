from gjsp.common.const_value import SmVal
from gjsp.skill.sm.sm_loop import SmSkillLoop


class SmSkillLoopPve(SmSkillLoop):

    def start(self):
        super().start()
        if self.skill().ci_fu.is_ok():
            self.freed_ci_fu()
