import random
import time
import win32gui
from ctypes import windll
from typing import Dict

from PIL import Image


class Windows:

    def __init__(self):
        self.hwnd: int = None
        self.width: int = None
        self.height: int = None

    def screen_shot(self) -> Image.Image:
        pass

    def key_down(self, key: str):
        pass

    def key_up(self, key):
        pass

    def mouse_left_down(self):
        pass

    def mouse_left_up(self):
        pass

    def mouse_right_down(self):
        pass

    def mouse_right_up(self):
        pass

    def key_press(self, key: str):
        keys = key.split("+")
        for x in keys:
            self.key_down(x)
            time.sleep(random.randint(40, 60) * 0.001)
        for x in reversed(keys):
            self.key_up(x)
            time.sleep(random.randint(40, 60) * 0.001)

    def mouse_left_click(self):
        self.mouse_left_up()
        self.random_wait()
        self.mouse_left_down()
        self.random_wait()
        self.mouse_left_up()

    def mouse_right_click(self):
        self.mouse_right_up()
        self.random_wait()
        self.mouse_right_down()
        self.random_wait()
        self.mouse_right_up()

    def random_wait(self):
        time.sleep(random.randint(40, 60) * 0.001)

    def init(self, hwnd):
        user32 = windll.user32
        user32.SetProcessDPIAware()
        Image.MAX_IMAGE_PIXELS = 15883307070

    @staticmethod
    def find_hwnd(name: str) -> Dict[int, str]:
        result = {}

        def find(hwnd, nouse):
            title = win32gui.GetWindowText(hwnd)
            if name in title and \
                    win32gui.IsWindow(hwnd) and \
                    win32gui.IsWindowEnabled(hwnd) and \
                    win32gui.IsWindowVisible(hwnd):
                result[hwnd] = title

        win32gui.EnumWindows(find, 0)
        return result

    @staticmethod
    def get_window_size(hwnd: int) -> (int, int):
        rect = win32gui.GetClientRect(hwnd)
        x = rect[0]
        y = rect[1]
        w = rect[2] - x
        h = rect[3] - y
        return (w, h)
