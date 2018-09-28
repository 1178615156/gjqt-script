import logging
from gjsp.common import WindowsDm
import time
import ctypes

logging.basicConfig(level=logging.INFO)
windows = WindowsDm()
gjqt_hwnd = list(windows.find_hwnd("古剑").keys())[0]
windows.init(gjqt_hwnd)


time.sleep(2)

x_ptr = ctypes.c_int(0)
y_ptr = ctypes.c_int(0)

print(windows.dll.GetCursorPos(ctypes.pointer(x_ptr),ctypes.pointer(y_ptr)))
print(x_ptr,y_ptr)

print(windows.dll.MoveTo(1500,100))

print(windows.dll.GetCursorPos(ctypes.pointer(x_ptr),ctypes.pointer(y_ptr)))
print(x_ptr,y_ptr)

# print(windows.dll.GetCursorSpot())
# print(windows.dll.MoveR(1500,100))
# print(windows.dll.GetCursorSpot())
#
time.sleep(0.1)
print(windows.dll.LeftClick())
time.sleep(0.1)
print(windows.dll.LeftClick())



# list_file = os.listdir("D:\\gjqt\\gjqt-script\\tmp-goal")
# list_img = list(map(lambda s: Image.open("D:\\gjqt\\gjqt-script\\tmp-goal\\" + s), list_file))
#
# print(list(zip(
#     map(lambda s: FindPic(s, SkillLoop.img_mouse_left).isFind(), list_img),
#     map(lambda s: FindPic(s, SkillLoop.img_mouse_right).isFind(), list_img),
# )))
# time.sleep(2)
# screen = Image.open("D:\\gjqt\\GuJian_Online\\screenshots\\2018-9-21-18-52-47.jpg")
# skill_loop = SkillLoop(windows)
# skill_loop.update_screen(screen)

# print(skill_loop.mouse_tap_if_need())