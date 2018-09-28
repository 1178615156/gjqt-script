from unittest import TestCase
from ctypes import windll
from gjsp.common.utensil import user_dir
import win32com.client


class TestRegCode(TestCase):
    def test_reg_code(self):
        print("")
        dll = windll[user_dir + "dm-7.dll"].DllUnregisterServer()
        dll = windll[user_dir + "dm-3.dll"].DllRegisterServer()
        #
        dm = win32com.client.Dispatch('dm.dmsoft')
        assert (dm.DmGuard(1, "np") == 0)

    def test_reg_code2(self):
        print("")
        dll = windll[user_dir + "dm-3.dll"].DllUnregisterServer()
        dll = windll[user_dir + "dm-7.dll"].DllRegisterServer()
        #
        dm = win32com.client.Dispatch('dm.dmsoft')
        assert (dm.DmGuard(1, "np") == 1)
