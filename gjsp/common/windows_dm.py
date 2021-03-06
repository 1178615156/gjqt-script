import os
import time
from ctypes import windll

import win32com.client
from PIL import Image

from gjsp.common import Windows
from gjsp.common.utensil import millisecond
from gjsp.common.utensil import user_dir
from gjsp.common.const_value import ConfigVal
import random

import logging

_logger = logging.getLogger("dm")


# def get_reg_code() -> List[List[str]]:
#     return list(
#         filter(lambda l: len(l) == 2,
#                map(lambda s: s.replace(" ", "").replace("\t", "").replace("\r", "").replace("\n", "").split("--"),
#                    list(open(user_dir + "dm_reg_code.txt").readlines()))))


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
        start_time = millisecond()
        dm_ret = self.dll.Capture(0, 0, self.width, self.height, self.screen_file_name)
        end_time = millisecond()
        _logger.debug("shot screen time:%s " % (end_time - start_time))
        self.check(dm_ret)
        return Image.open(self.screen_file_name)

    def load_dll(self):
        if len(ConfigVal.dm_reg_list) == 0:
            print("not find reg code , use free dm")
            windll[user_dir + "dm-7.dll"].DllUnregisterServer()
            windll[user_dir + "dm-3.dll"].DllRegisterServer()
            self.dll = win32com.client.Dispatch('dm.dmsoft')
            self.is_free = True
        else:
            print("find dm reg code , try to reg")
            windll[user_dir + "dm-3.dll"].DllUnregisterServer()
            windll[user_dir + "dm-7.dll"].DllRegisterServer()
            self.dll = win32com.client.Dispatch('dm.dmsoft')
            for reg_code in ConfigVal.dm_reg_list:
                dm_ret = self.dll.Reg(reg_code.get("code"), reg_code.get("add"))
                if dm_ret != 1:
                    print("failure %s: %s" %(dm_ret,str(reg_code)))
                    continue
                else:
                    print("success : "+str(reg_code))
                    self.is_free = False
                    break

            if self.is_free is not False:
                raise Exception("all dm reg code is failure")

        return self.dll

    def init(self, hwnd: int):
        print("start init ; the windows hwnd is :%s" % (hwnd))
        self.load_dll()
        if self.is_free:
            print("start bind window")
            # dm_ret = self.dll.BindWindow(hwnd, "normal", "normal", "normal", 0)
            dm_ret = self.dll.BindWindow(hwnd, "gdi", "normal", "windows", 0)
            self.check(dm_ret, "bind is failure")
            print("bind window success")
        else:
            dm_ret = self.dll.DmGuard(1, "np")
            self.check(dm_ret)

            print("start bind window")
            dm_ret = self.dll.BindWindow(hwnd, "gdi", "normal", "windows", 0)
            self.check(dm_ret, "bind is failure")
            print("bind window success")

        super().init(hwnd)
        self.hwnd = hwnd
        self.width = 1680
        self.height = 1050
        self.mk_dir()

    def mk_dir(self):
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

    def mouse_left_down(self):
        dm_ret = self.dll.LeftDown()
        self.check(dm_ret)

    def mouse_left_up(self):
        dm_ret = self.dll.LeftUp()
        self.check(dm_ret)

    def mouse_right_down(self):
        dm_ret = self.dll.RightUp()
        self.check(dm_ret)

    def mouse_right_up(self):
        dm_ret = self.dll.RightDown()
        self.check(dm_ret)

    # def mouse_left_click(self):
    #     dm_ret = self.dll.LeftClick()
    #     self.check(dm_ret)
    #
    # def mouse_right_click(self):
    #     dm_ret = self.dll.RightClick()
    #     self.check(dm_ret)

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
