import ctypes
import win32process
import win32security
from ctypes import *
import ctypes, win32ui, win32process, win32api
from ctypes import wintypes as w
from gjsp.common import Windows

k32 = ctypes.WinDLL("kernel32", use_last_error=True)
OpenProcess = windll.kernel32.OpenProcess
GetWindowThreadProcessId = windll.user32.GetWindowThreadProcessId

ReadProcessMemory = k32.ReadProcessMemory
ReadProcessMemory.argtypes = [w.HANDLE, w.LPCVOID, w.LPVOID, c_size_t, POINTER(c_size_t)]
ReadProcessMemory.restype = w.BOOL

VirtualProtectEx = k32.VirtualProtectEx
VirtualProtectEx.argtypes = [w.HANDLE, w.LPCVOID, c_size_t, w.DWORD, w.PDWORD]

hwnd = list(Windows.find_hwnd("古剑").keys())[0]

# hwnd = list(Windows.find_hwnd("微信").keys())[0]
# address = 0x011D78BC
# windows = WindowsDm()
# windows.init(hwnd)

PID = win32process.GetWindowThreadProcessId(hwnd)[1]
PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)
PROCESS_VM_OPERATION = 0x0008
process = win32api.OpenProcess(PROCESS_ALL_ACCESS | PROCESS_VM_OPERATION, 0, PID)
processHandle = process.handle
print(str({
    "all access"   : PROCESS_ALL_ACCESS,
    "hwnd"         : hwnd,
    "processHandle": processHandle
}))

address = (0x1A5D8FBB9D8)

def AdjustPrivilege(priv):
    flags = win32security.TOKEN_ADJUST_PRIVILEGES | win32security.TOKEN_QUERY
    htoken = win32security.OpenProcessToken(processHandle, win32security.TOKEN_ALL_ACCESS)
    id = win32security.LookupPrivilegeValue(None, priv)
    newPrivileges = [(id, win32security.SE_PRIVILEGE_ENABLED)]
    win32security.AdjustTokenPrivileges(htoken, 0, newPrivileges)


def changeProtect():
    old_protection = w.DWORD(0)
    print({
        "VirtualProtectEx": k32.VirtualProtectEx(processHandle, w.LPVOID(address), 1, 0x40, w.PDWORD(old_protection)),
        "last_error"      : k32.GetLastError()
    })


def read_by_win():
    buff = create_string_buffer(4)
    bufferSize = (sizeof(buff))
    appBase = c_int32()
    numRead = c_int()
    bytesRead = c_ulong(0)
    print(str({
        "read_memory": ReadProcessMemory(processHandle, address, (byref(appBase)), bufferSize, byref(bytesRead)),
        "last_error" : k32.GetLastError(),
        "value"      : appBase
    }))


AdjustPrivilege("seDebugPrivilege")
changeProtect()
read_by_win()
