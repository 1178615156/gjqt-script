from gjsp.common.utensil import user_dir
from gjsp.service.fish import Fish
from gjsp.common import WindowsDm, Windows
from gjsp.common.windows_dm import get_reg_code
import sys
import time
import ctypes

start_msg = """
    welcome to use gjqt script
        args:%s
        user_dir:%s
        reg_code:%s
""" % (str(sys.argv), user_dir, get_reg_code())
print(start_msg)
time.sleep(0.5)

windows = WindowsDm()

gjqt_hwnd = list(windows.find_hwnd("古剑").keys())
resolution = lambda: Windows.get_window_size(gjqt_hwnd[0])
opt = lambda: sys.argv[1]

if not ctypes.windll.shell32.IsUserAnAdmin():
    print("not admin , can not run")
    exit()
if len(gjqt_hwnd) == 0:
    print("gj online have not start")
    exit()
if len(gjqt_hwnd) > 1:
    print("you start gj online multiple instances")
    exit()
if not resolution() == (1680, 1050):
    print("当前分辨率 %s ,只支持 (1680, 1050)")
    exit()

gjqt_hwnd = gjqt_hwnd[0]
windows.init(gjqt_hwnd)


if len(sys.argv) <= 1:
    print("just test")
    time.sleep(2)
    windows.key_press("1")

elif opt() == "fish":
    size = int(sys.argv[2])
    print("""
        即将开始钓鱼,请将窗口切换至[古剑奇谭ol]
        请勿遮挡,或最小化,
        请检查分辨率是否为 `1050*1680`,只支持该分辨率,
        记得在游戏中使用钓鱼竿进入钓鱼状态,并上好鱼饵
    """)
    for i in range(5):
        print('will start after %s' % (str(5 - i)))
        time.sleep(1)
    for i in range(size):
        print("finish fish :%s" % (i))
        Fish(gjqt_hwnd, windows).run()
else:
    print("unknown cmd")

