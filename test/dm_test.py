import time
import win32com.client
from gjsp.common import Windows

hwnd = list(Windows().find_hwnd("古剑").keys())[0]
print(hwnd)
dll_path = "D:\\gjqt\\gjqt-script\\dm.dll"
dll = win32com.client.Dispatch('dm.dmsoft')


# dll = comtypes.client.GetModule("D:\\gjqt\\gjqt-script\\dm-2.dll")
# dll = comtypes.client.CreateObject(dll.dmsoft._reg_clsid_.as_progid())


print("a")
# time.sleep(1)
# print(dll.keyPressChar("1"))
# print(dll.keyPressChar("2"))
# print(dll.keyPressChar("3"))
# print(dll.DmGuard(1,"np"))
print(dll.BindWindow(hwnd, "normal", "normal", "normal", 0))
time.sleep(2)
