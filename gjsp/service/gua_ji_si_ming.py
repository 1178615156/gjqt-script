import logging
from gjsp.common import WindowsBuild
from gjsp.service.gua_ji import GjDps, GjZiLiao
from gjsp.service.hot_key import HotKey
from gjsp.skill.sm import SmSkillLoopFsmPve, SmSkillLoopFsmPvp

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    windows = WindowsBuild().build()
    gjqt_hwnd = list(windows.find_hwnd("古剑").keys())[0]
    windows.init(gjqt_hwnd)

    print("start %s" % gjqt_hwnd)

    hot_key = HotKey()
    hot_key.add_handler(GjDps(name="gj-dps-pve", key="F5", windows=windows, skill_loop=SmSkillLoopFsmPve(windows)))
    hot_key.add_handler(GjDps(name="gj-dps-pvp", key="F6", windows=windows, skill_loop=SmSkillLoopFsmPvp(windows)))
    hot_key.add_handler(GjZiLiao(name="gj-zi-liao", key="F7", windows=windows))
    hot_key.start_hook()
    hot_key.run_even_loop()
