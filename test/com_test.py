
import ctypes
import comtypes
import win32com.client
from comtypes.client import CreateObject
from comtypes import GUID


dm = win32com.client.Dispatch('dm.dmsoft')

# OTAClientDLL = comtypes.client.CreateObject("D:\\gjqt\\gjqt-script\\Danbl_L.dll")
# OTAClientDLL.GetModuleAdd()

# OTAClientDLL = comtypes.client.CreateObject("comtypes.gen.dm")
# dll = CreateObject("dm.dmsoft")
# print(OTAClientDLL.BindWindow())

# dll = ctypes.CDLL("D:\\gjqt\\gjqt-script\\Danbo_L.dll")
# dll = win32com.client.Dispatch("D:\\gjqt\\gjqt-script\\Danbo_L.dll")
# dll = comtypes.client.CreateObject("D:\\gjqt\\gjqt-script\\Danbo_L.dll")
dll = comtypes.client.GetModule("D:\\Danbo_L.dll")
import comtypes.gen._B743E134_19B3_416D_91EE_2A3B5AF49314_0_1_0
dll = comtypes.client.CreateObject(dll.ArleneZ._reg_clsid_.as_progid())
print(dll.PjdmMax())


# dm = comtypes.client.GetModule("D:\\gjqt\\gjqt-script\\dm-2.dll")
# dm = comtypes.client.CreateObject(dm.dmsoft._reg_clsid_.as_progid())

print(dm.DmGuard(1,"np"))