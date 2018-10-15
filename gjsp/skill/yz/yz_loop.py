import time
from enum import Enum

from gjsp import Screen
from gjsp.skill import Skill
from gjsp.skill import SkillLoop


class YzSkill(Screen):
    def __init__(self, windows):
        super().__init__()
        self.q = Skill("q", "q", windows, None)
        self.e = Skill("e", "e", windows, None)
        self.j = Skill("j", "8", windows, None)
        self.cdd = Skill("cdd", "9", windows, None)


class Status(Enum):
    Q1 = 1
    Q2 = 2
    Q3 = 3
    CDD = 10


class YzSkillLoop(SkillLoop):
    def __init__(self, windows):
        super().__init__(windows)
        self.__skill = YzSkill(windows)
        self.status = Status.Q1
        self.number = 0

    def skill(self):
        return self.__skill

    def ka_dao(self):
        time.sleep(0.2)

    def clear(self):
        self.become(Status.Q1)

    def run(self):
        def wait_skill():
            time.sleep(0.6)

        if self.status is Status.Q1:
            self.skill().q.freed()
            self.ka_dao()
            self.skill().e.freed()
            wait_skill()
            self.become(Status.Q3)

        # if self.status is Status.Q2:
        #     self.skill().q.freed()
        #     self.ka_dao()
        #     self.skill().q.freed()
        #     time.sleep(0.5)
        #     self.become(Status.Q3)

        if self.status is Status.Q3:
            self.skill().q.freed()
            self.ka_dao()
            self.skill().e.freed()
            wait_skill()
            self.become(Status.CDD)

        if self.status is Status.CDD:
            self.skill().q.freed()
            self.ka_dao()
            self.skill().cdd.freed()
            self.become(Status.Q1)
            time.sleep(1.1)
            self.number += 1
            # self.skill().q.freed()
            # self.become(None)
