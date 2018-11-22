from gjsp import Screen
from gjsp.skill import Skill
from gjsp.common.const_value import *

from functional import seq


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
        self.windows = windows
        self.q = Skill("q", "[", windows, SmVal.SkillImg.q)
        self.e = Skill("e", "]", windows, SmVal.SkillImg.e)
        self.hong_guang = Skill("虹光", "6", windows, SmVal.SkillImg.hong_guang)
        self.hong_guang_ci_fu = Skill("虹光-赐福", "6", windows, SmVal.SkillImg.hong_guan_ci_fu)
        self.hong_guang_free = Skill("虹光-免费", "6", windows, SmVal.buff_liu_guang)
        self.hong_guang_mei_lan = Skill("虹光", "6", windows, SmVal.SkillImg.hong_guang_mei_lan)
        self.gun_si = Skill("滚石", "7", windows, SmVal.SkillImg.gun_si)
        self.min_si = Skill("季晴", "8", windows, SmVal.SkillImg.ji_qin)
        self.ci_fu = Skill("赐福", "9", windows, SmVal.SkillImg.ci_fu)
        self.yu_hong = Skill("玉虹", "0", windows, SmVal.SkillImg.yu_hong)
        self.jin_yu = Skill("金羽", "-", windows, SmVal.SkillImg.jin_yu)
        self.ling_li = Skill("灵狸", "=", windows, SmVal.SkillImg.ling_li)

        self.all_skills = seq(vars(self).items()).map(lambda x:x[1]).filter(lambda x: isinstance(x, Skill))

    def update(self, screen):
        screen_skill = screen.crop(AreaVal.skill)
        screen_buff = screen.crop(AreaVal.buff)
        self.all_skills.for_each(lambda skill: skill.update(screen_skill))
        self.hong_guang_free.update(screen_buff)
        # self.hong_guang.update(screen_skill)
        # self.hong_guang_ci_fu.update(screen_skill)
        # self.gun_si.update(screen_skill)
        # self.min_si.update(screen_skill)
        # self.ci_fu.update(screen_skill)
        # self.yu_hong.update(screen_skill)
        # self.jin_yu.update(screen_skill)
        # self.hong_guang_mei_lan.update(screen_skill)
