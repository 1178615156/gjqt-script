from gjsp.common import Windows
from PIL import ImageGrab
import win32gui
import pywinio
import time
import atexit


class WindowsWinIo(Windows):

    def init(self, hwnd):
        super().init(hwnd)
        init()

    def screen_shot(self):
        game_rect = win32gui.GetWindowRect(self.hwnd)
        src_image = ImageGrab.grab(game_rect)
        return src_image

    def key_press(self, key: str):
        key = key.lower()
        key_code = {
            "q"    : 0x10,
            "enter": 0x1c
        }
        key_press(key_code[key])

# KeyBoard Commands
# Command port
KBC_KEY_CMD = 0x64
# Data port
KBC_KEY_DATA = 0x60

__winio = None


def __get_winio():
    global __winio

    if __winio is None:
        __winio = pywinio.WinIO()

        def __clear_winio():
            global __winio
            __winio = None

        atexit.register(__clear_winio)

    return __winio


def wait_for_buffer_empty():
    '''
    Wait keyboard buffer empty
    '''

    winio = __get_winio()

    dwRegVal = 0x02
    while (dwRegVal & 0x02):
        dwRegVal = winio.get_port_byte(KBC_KEY_CMD)


def key_down(scancode):
    winio = __get_winio()

    wait_for_buffer_empty()
    winio.set_port_byte(KBC_KEY_CMD, 0xd2)
    wait_for_buffer_empty()
    winio.set_port_byte(KBC_KEY_DATA, scancode)


def key_up(scancode):
    winio = __get_winio()

    wait_for_buffer_empty()
    winio.set_port_byte(KBC_KEY_CMD, 0xd2)
    wait_for_buffer_empty()
    winio.set_port_byte(KBC_KEY_DATA, scancode | 0x80)


def key_press(scancode, press_time=0.01):
    key_down(scancode)
    time.sleep(press_time)
    key_up(scancode)


def init():
    winio = __get_winio()


# Scancodes references : https://www.win.tue.nl/~aeb/linux/kbd/scancodes-1.html
if __name__ == '__main__':
    time.sleep(1)
    key_press(0x10)
    time.sleep(1)
    key_press(0x1E)
    time.sleep(1)
    key_press(0x10)
    time.sleep(1)
    key_press(0x1E)
