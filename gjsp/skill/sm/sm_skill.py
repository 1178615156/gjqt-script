from gjsp import Screen
from gjsp.skill import Skill
from gjsp.common.const_value import *

class SmSkill(Screen):
    img_skills = goal_image("skills.bmp")

    @staticmethod
    def skill_img(x_start, x_end=None, shills_img=img_skills):
        if not x_end:
            x_end = x_start + 40
        return shills_img.crop((x_start, 0, x_end, shills_img.height))

    def __init__(self, windows):
        super().__init__()
        skill_img = self.skill_img
        n = 44
        self.q = Skill("q", "q", windows, None)
        self.e = Skill("e", "e", windows, None)
        self.hong_guang = Skill("虹光", "6", windows,
                                [skill_img(n * 2 + 2), goal_image("si_ming_skill_hong_guang_ci_fu.bmp")])
        self.gun_si = Skill("滚石", "7", windows, [skill_img(n * 3)])
        self.min_si = Skill("名视", "8", windows, skill_img(n * 4 + 2))
        self.ci_fu = Skill("赐福", "9", windows, skill_img(n * 5 + 2))
        self.yu_hong = Skill("玉虹", "0", windows, skill_img(n * 6 + 2))
        self.jin_yu = Skill("金羽", "-", windows, skill_img(n * 7 + 2))

    def update(self, screen):
        screen = screen.crop(area_skill)
        self.hong_guang.update(screen)
        self.gun_si.update(screen)
        self.min_si.update(screen)
        self.ci_fu.update(screen)
        self.yu_hong.update(screen)
        self.jin_yu.update(screen)
