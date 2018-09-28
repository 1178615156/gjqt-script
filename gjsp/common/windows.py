import win32gui
from ctypes import windll
import time
from PIL import Image
from typing import Dict


class Windows:
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

    def __init__(self):
        self.hwnd: int = None
        self.width: int = None
        self.height: int = None

    def screen_shot(self) -> Image.Image: pass

    def key_press(self, key: str): pass

    def key_down(self, key: str): pass

    def key_up(self, key): pass

    def mouse_left_click(self): pass

    def mouse_right_click(self): pass

    def wait(self, t=0.1):
        time.sleep(t)

    def init(self, hwnd):
        user32 = windll.user32
        user32.SetProcessDPIAware()
        Image.MAX_IMAGE_PIXELS = 15883307070
