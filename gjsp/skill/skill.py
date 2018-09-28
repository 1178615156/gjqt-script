from gjsp.common.find_pic import FindPic
from enum import Enum


class SkillStatus(Enum):
    Wait = 0
    Start = 1
    Normal = 2
    Explosive = 3


class Skill:
    def __init__(self, icon=None, key=None, screen=None):
        self.key = key
        self.__icon = icon
        self.__screen = screen
        self.__result = FindPic(original=self.__screen, goal=self.__icon, sim=0.99)

    def result(self):
        return self.__result

    def is_ok(self):
        return self.result().isFind()

    def press(self, windows):
        windows.key_press(self.key)


