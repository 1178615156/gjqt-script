# import win32api
# import win32con
# import time
#
# time.sleep(2)
# win32api.keybd_event(win32con.VK_NUMPAD7,
#                      win32api.MapVirtualKey(win32con.VK_NUMPAD7,3),
#                      win32con.KEYEVENTF_EXTENDEDKEY,
#                      0)  # press
# win32api.Sleep(50)
# win32api.keybd_event(win32con.VK_NUMPAD7,
#                      win32api.MapVirtualKey(win32con.VK_NUMPAD7,3),
#                      win32con.KEYEVENTF_EXTENDEDKEY | win32con.KEYEVENTF_KEYUP,
#                      0)  # r
# import random
#
# print(random.randint(40,60))
#
# from functional import seq
# print(seq(0).find(lambda x:x==1))
# print(seq(None,None))
from functional import seq
class A:
    def __init__(self):
        self.a = 1
        self.b = 2
        self.c = "c"

a = A()
# for k,v in (vars(a).items()):
#     print(k,v)
l=seq(vars(a).items()).filter(lambda k:type(k[1]) is int )
print(l)