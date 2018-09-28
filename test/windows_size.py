from gjsp.common import WindowsDm
import win32gui
from ctypes import windll

user32 = windll.user32
user32.SetProcessDPIAware()

windows = WindowsDm()
gjqt_hwnd = list(windows.find_hwnd("古剑").keys())[0]
rect = win32gui.GetClientRect(gjqt_hwnd)

x = rect[0]
y = rect[1]
w = rect[2] - x
h = rect[3] - y
print("\tLocation: (%d, %d)" % (x, y))
print("\t    Size: (%d, %d)" % (w, h))
