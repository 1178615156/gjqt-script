import os
import time
from ctypes import windll
from typing import List

import win32com.client
from PIL import Image

from gjsp.common import Windows
from gjsp.common.utensil import user_dir


def get_reg_code() -> List[List[str]]:
    return list(
        filter(lambda l: len(l) == 2,
               map(lambda s: s.replace(" ", "").replace("\t", "").replace("\r", "").replace("\n", "").split("--"),
                   list(open(user_dir + "dm_reg_code.txt").readlines()))))


class WindowsDm(Windows):

    def __init__(self):
        super().__init__()
        self.dll = None
        self.is_free = None

    def get_last_error(self):
        return self.dll.getLastError()

    def check(self, dm_ret, error_msg=None):
        if dm_ret is None:
            assert dm_ret == 1, "dm_ret:%s,code:%s" % (dm_ret, self.get_last_error())
        else:
            assert dm_ret == 1, "msg:%s,dm_ret:%s,code:%s" % (error_msg, dm_ret, self.get_last_error())

    def screen_shot(self) -> Image.Image:
        dm_ret = self.dll.Capture(0, 0, self.width, self.height, self.screen_file_name)
        self.check(dm_ret)
        return Image.open(self.screen_file_name)

    def init(self, hwnd: int):
        print("start init ; the windows hwnd is :%s" % (hwnd))
        if len(get_reg_code()) == 0:
            print("not find reg code , use free dm")
            windll[user_dir + "dm-7.dll"].DllUnregisterServer()
            windll[user_dir + "dm-3.dll"].DllRegisterServer()
            self.dll = win32com.client.Dispatch('dm.dmsoft')
            self.is_free = True
            print("start bind window")
            # dm_ret = self.dll.BindWindow(hwnd, "normal", "normal", "normal", 0)
            dm_ret = self.dll.BindWindow(hwnd, "gdi", "windows", "windows", 0)
            self.check(dm_ret, "bind is failure")
            print("bind window success")

        else:
            print("find reg code , try to reg")
            windll[user_dir + "dm-3.dll"].DllUnregisterServer()
            windll[user_dir + "dm-7.dll"].DllRegisterServer()
            a, b = get_reg_code()[0]
            self.dll = win32com.client.Dispatch('dm.dmsoft')
            dm_ret = self.dll.Reg(a, b)
            self.check(dm_ret, "reg code is failure")
            self.is_free = False
            print("reg success")

            print("start bind window")
            dm_ret = self.dll.BindWindow(hwnd, "gdi", "windows", "windows", 0)
            self.check(dm_ret, "bind is failure")
            print("bind window success")

        super().init(hwnd)
        self.hwnd = hwnd
        self.width = 1680
        self.height = 1050

        self.user_dir = user_dir
        self.tmp_dir = user_dir + "image_tmp\\"
        self.screen_file_name = self.tmp_dir + "screen.bmp"

        if not os.path.exists(self.tmp_dir):
            print("%s is not exist , try to create it " % (self.tmp_dir))
            os.makedirs(self.tmp_dir)

    def key_down(self, key: str):
        dm_ret = self.dll.KeyDownChar(key)
        self.check(dm_ret)

    def key_up(self, key):
        dm_ret = self.dll.KeyUpChar(key)
        self.check(dm_ret)

    def key_press(self, key: str):
        if "+" in key:
            keys = key.split("+")
            for x in keys:
                self.wait()
                self.key_down(x)
            for x in reversed(keys):
                self.wait()
                self.key_up(x)
        else:
            dm_ret = self.dll.KeyPressChar(key)
            self.check(dm_ret)

    def mouse_left_click(self):
        dm_ret = self.dll.LeftClick()
        self.check(dm_ret)

    def mouse_right_click(self):
        dm_ret = self.dll.RightClick()
        self.check(dm_ret)

    def move_to(self, x: int, y: int):
        dm_ret = self.dll.MoveTo(x, y)
        self.check(dm_ret)


if __name__ == '__main__':
    windows = WindowsDm()
    hwnd = list(windows.find_hwnd("古剑").keys())[0]
    windows.init(hwnd)
    print((hwnd, windows.width, windows.height, windows.screen_file_name))

    time.sleep(2)
    # windows.key_press("enter")
    windows.key_press("enter")
    # windows.key_press("enter")
    # windows.key_press("enter")
    # windows.key_press("enter")
    # windows.key_press("enter")
    # for i in range(1, 10):
    #     start_time = int(time.time() * 1000.0)
    #     windows.screen_shot()
    #     end_time = int(time.time() * 1000.0)
    #     print(end_time - start_time)
    #     time.sleep(0.1)
