import ctypes
import os
import time
from ctypes import windll
from ctypes import wintypes

import win32com.client

from gjsp.common import Windows
from gjsp.common.utensil import user_dir

rPM = ctypes.WinDLL('kernel32',use_last_error=True).ReadProcessMemory
rPM.argtypes = [wintypes.HANDLE,wintypes.LPCVOID,wintypes.LPVOID,ctypes.c_size_t,ctypes.POINTER(ctypes.c_size_t)]
rPM.restype = wintypes.BOOL
pid = os.getpid()

dm_dll = windll[user_dir + "dm-5.dll"]
dm_dll.DllRegisterServer()

ADDRESS1 = 0x00E97074
ADDRESS2 = ctypes.create_string_buffer(64)
bytes_read = ctypes.c_size_t()
print(rPM(pid,ADDRESS1,ADDRESS2,64,ctypes.byref(bytes_read)))



# hwnd = list(Windows().find_hwnd("古剑").keys())[0]
# print(hwnd)
# dll_path = "D:\\gjqt\\gjqt-script\\dm.dll"
# dll = win32com.client.Dispatch('dm.dmsoft')
#
#
# print("a")
# print(dll.BindWindow(hwnd, "normal", "normal", "normal", 0))
# time.sleep(2)
