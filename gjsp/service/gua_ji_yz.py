import logging

from gjsp.common.windows_dm import WindowsDm
from gjsp.service.gua_ji import GjDps
from gjsp.service.hot_key import HotKey
from gjsp.skill.yz.yz_loop import YzSkillLoop

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    windows = WindowsDm()
    gjqt_hwnd = list(windows.find_hwnd("古剑").keys())[0]
    windows.init(gjqt_hwnd)

    print("start %s" % gjqt_hwnd)

    hot_key = HotKey()
    hot_key.add_handler(GjDps(name="gj-dps", key="F9", windows=windows, skill_loop=YzSkillLoop(windows)))
    hot_key.start_hook()
    hot_key.run_even_loop()
