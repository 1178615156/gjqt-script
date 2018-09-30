import logging
import time

from gjsp.common.windows_dm import WindowsDm
from gjsp.service.hot_key import HotKey
from gjsp.common.utensil import millisecond
from gjsp.service.even_loop import EvenLoop
from gjsp.service.gua_ji import GjDps, GjDpsPve, GjDpsPvp
from gjsp.skill.sm.sm_loop import SmSkillLoop


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


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    windows = WindowsDm()
    gjqt_hwnd = list(windows.find_hwnd("古剑").keys())[0]
    windows.init(gjqt_hwnd)

    print("start %s" % gjqt_hwnd)

    hot_key = HotKey()
    hot_key.add_handler(GjDps(name="gj-dps", key="F8", windows=windows, skill_loop=SmSkillLoop(windows)))
    hot_key.add_handler(GjDpsPve(name="gj-dps-pve", key="F5", windows=windows, skill_loop=SmSkillLoop(windows)))
    hot_key.add_handler(GjDpsPvp(name="gj-dps-pvp", key="F6", windows=windows, skill_loop=SmSkillLoop(windows)))
    hot_key.add_handler(GjZiLiao(name="gj-zi-liao", key="F7", windows=windows))
    hot_key.start_hook()
    hot_key.run_even_loop()
