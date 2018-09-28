import time

from gjsp.service.even_loop import EvenLoop
from gjsp.skill import SkillLoop


class GjDps(EvenLoop):
    def __init__(self, name, key, windows, skill_loop: SkillLoop):
        super().__init__(name, key)
        self.windows = windows
        self.skill_loop: SkillLoop = skill_loop

    def clear(self):
        self.skill_loop.clear()

    def delay(self):
        time.sleep(0.2)

    def run(self):
        self.skill_loop.update_screen()
        self.skill_loop.run()


class GjDpsPve(GjDps):
    def run(self):
        self.skill_loop.pve()


class GjDpsPvp(GjDps):
    def run(self):
        self.skill_loop.pvp()
