import ctypes
import sys
import time

from functional import seq

from gjsp.common import Windows
from gjsp.common.const_value import ConfigVal, AreaVal
from gjsp.common.windows_dm import WindowsDm
from gjsp.service.fish import Fish
from gjsp.service.gua_ji import GjDps
from gjsp.service.hot_key import HotKey
from gjsp.skill.sm import SmSkillLoopFsmPve

if not ctypes.windll.shell32.IsUserAnAdmin():
    print("not admin , can not run")
    exit(-1)


def get_gjqt_hwnd(w:Windows):
    gjqt_hwnd = list(w.find_hwnd("古剑").keys())
    if len(gjqt_hwnd) != 1:
        print("gj online have not start or you start gj online multiple instances")
        exit(-1)
    return gjqt_hwnd[0]


windows = WindowsDm()
hwnd = get_gjqt_hwnd(windows)
windows.init(hwnd)
resolution = Windows.get_window_size(hwnd)
opt = lambda: sys.argv[1]
windows.mk_dir()

print(seq({
    "args      ":str(sys.argv),
    "resolution":str(resolution),
    "hwnd      ":str(hwnd),
    "reg_code  ":str(ConfigVal.dm_reg_list),
    "dm_is_free":str(windows.is_free)
}.items()).map(lambda x:x[0]+":"+x[1]).make_string("\n"))

if not resolution == (1680, 1050):
    print("当前分辨率 %s ,只支持 (1680, 1050)" % (str(resolution)))
    exit()

if len(sys.argv) <= 1 or opt() == "test":
    print("just test")
    time.sleep(2)
    screen = windows.screen_shot()
    screen.crop(AreaVal.skill).save("test_skill_area.bmp")
    screen.crop(AreaVal.buff).save("test_buff_area.bmp")
    screen.crop(AreaVal.fu_wen).save("test_fu_wen_area.bmp")
    screen.crop(AreaVal.dot).save("test_dot_area.bmp")
    windows.key_press("1")

elif opt() == "fish":
    if len(sys.argv) > 2:
        size = int(sys.argv[2])
    else:
        size = ConfigVal.fish_size
    print("""
        即将开始钓鱼,请将窗口切换至[古剑奇谭ol]
        请勿遮挡,或最小化,
        记得在游戏中使用钓鱼竿进入钓鱼状态,并上好鱼饵
    """)
    for i in range(5):
        print('will start after %s' % (str(5 - i)))
        time.sleep(1)
    for i in range(size):
        Fish(hwnd, windows).run()
        print("finish fish :%s" % (i))
elif opt() == "si-ming-gua-ji":
    print("""
        开始 司命挂机输出
        请将窗口切换至[古剑奇谭ol]
        请勿遮挡,或最小化,
        【F5】键启动,再次按【F5】退出
    """)
    hot_key = HotKey()
    hot_key.add_handler(GjDps(name="gj-dps-pve", key="F5", windows=windows, skill_loop=SmSkillLoopFsmPve(windows)))
    hot_key.start_hook()
    hot_key.run_even_loop()
else:
    print("unknown cmd")
