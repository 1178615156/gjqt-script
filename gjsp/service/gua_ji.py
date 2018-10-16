import time

from gjsp.common.utensil import millisecond
from gjsp.service.even_loop import EvenLoop


class GjDps(EvenLoop):
    def __init__(self, name, key, windows, skill_loop):
        super().__init__(name, key)
        self.windows = windows
        self.skill_loop = skill_loop

    def clear(self):
        self.skill_loop.clear()

    def run(self):
        self.skill_loop.run()

    def delay(self): pass


class GjZiLiao(EvenLoop):
    def __init__(self, name, key, windows):
        super().__init__(name, key)
        self.windows = windows
        self.start_time = millisecond()

    def run(self):
        pass_second = int((millisecond() - self.start_time) / 1000)
        if pass_second % 9 == 0:
            self.windows.key_press("q")
            time.sleep(1)
        if pass_second % 13 == 0:
            self.windows.key_press("e")
            time.sleep(1)
