from gjsp.common.windows import Windows
import ctypes
import comtypes
import win32com.client
from comtypes.client import CreateObject
from comtypes import GUID
import time

hwnd = list(Windows.find_hwnd("古剑").keys())[0]
print(hwnd)
dll = ctypes.windll["D:\\Bkgnd.dll"]
dll.DllRegisterServer()

dll.KeyPress(hwnd,65)