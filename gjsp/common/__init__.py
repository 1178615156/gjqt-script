from .windows import Windows
from .windows_dm import WindowsDm
from .find_pic import FindPic


class WindowsBuild:
    def build(self):
        return WindowsDm()


def get_gjqt_hwnd(w: Windows):
    gjqt_hwnd = list(w.find_hwnd("古剑").keys())
    if len(gjqt_hwnd) != 1:
        print("gj online have not start or you start gj online multiple instances")
        exit(-1)
    return gjqt_hwnd[0]
