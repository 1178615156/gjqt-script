from .windows import Windows
from .windows_dm import WindowsDm
from .find_pic import FindPic


class WindowsBuild:
    def build(self):
        return WindowsDm()
