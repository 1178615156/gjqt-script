import logging
import time

from gjsp.common.utensil import millisecond, goal_image
from gjsp.common import Windows,FindPic
from gjsp.skill import SkillStatus, Skill, SkillLoop
from gjsp.skill.ling_li import LingLiSiMing

_logger = logging.getLogger("skill")


class SkillSiMing:
    skills = goal_image("skills.bmp")

    @staticmethod
    def split_skills(shills_img, x_start, x_end=None):
        if not x_end:
            x_end = x_start + 40
        return shills_img.crop((x_start, 0, x_end, shills_img.height))

    def __init__(self, screen):
        def split_skills(x_start): return SkillSiMing.split_skills(SkillSiMing.skills, x_start)

        n = 44
        self.q = Skill(split_skills(n * 0), "q", screen=screen)
        self.e = Skill(split_skills(n * 1), "6", screen=screen)
        self.hong_guang: Skill = Skill(split_skills(n * 2 + 2), "-", screen=screen)
        self.hong_guang_ci_fu: Skill = Skill(goal_image("si_ming_skill_hong_guang_ci_fu.bmp"), "-", screen=screen)
        self.gun_si = Skill(split_skills(n * 3), "x", screen=screen)
        self.min_si = Skill(split_skills(n * 4 + 2), "7", screen=screen)
        self.ci_fu = Skill(split_skills(n * 5 + 2), "8", screen=screen)
        self.yu_hong = Skill(split_skills(n * 6 + 2), "9", screen=screen)
        self.jin_yu = Skill(split_skills(n * 7 + 2), "0", screen=screen)


class SkillLoopSiMing(SkillLoop):
    img_fu_wen_empty = goal_image("si_ming_fu_wen_empty.bmp")
    img_fu_wen_empty_plus = goal_image("si_ming_fu_wen_empty_plus.bmp")

    img_fu_wen_some = goal_image("si_ming_fu_wen_some.bmp")
    img_fu_wen_wait = goal_image("si_ming_fu_wen_wait.bmp")
    img_fu_wen_jin_yu = goal_image("si_ming_fu_wen_jin_yu.bmp")

    img_buff_qjwh = goal_image("si_ming_buff_qjwh.bmp")
    img_buff_zu_fu = goal_image("si_ming_buff_ci_fu.bmp")
    img_buff_liu_guang = goal_image("si_ming_buff_liu_guang.bmp")

    img_skill_hg_liu_guang = goal_image("si_ming_skill_hong_guang_liu_guang.bmp")
    img_skill_hg_ci_fu = goal_image("si_ming_skill_hong_guang_ci_fu.bmp")

    def __init__(self, windows: Windows):
        super().__init__(windows)
        self.ling_li = LingLiSiMing()
        self.__skills: SkillSiMing = None

    def skill(self):
        return self.__skills

    def update_after_screen(self):
        self.__skills = SkillSiMing(self.screen().crop(self.area_skill))

    ### skill status
    def fu_wen_is_ok(self) -> bool:
        x1 = FindPic(original=self.screen().crop(self.area_fu_wen), goal=self.img_fu_wen_empty).isFind()
        x2 = FindPic(original=self.screen().crop(self.area_fu_wen), goal=self.img_fu_wen_empty_plus).isFind()
        return x1 or x2

    def fu_wen_is_wait(self) -> bool:
        return FindPic(original=self.screen().crop(self.area_fu_wen), goal=self.img_fu_wen_wait).isFind()

    ### use skill
    def use_gun_si(self, skill: SkillSiMing):
        _logger.info("滚石")
        self.windows.key_press(skill.gun_si.key)
        self.wait(0.15)

    def use_e(self, skill: SkillSiMing):
        self.windows.key_press(skill.e.key)
        self.update_time()
        _logger.info("e")

    ### status logic loop
    def start(self, skill: SkillSiMing):
        for i in range(5):
            self.use_gun_si(skill)
        self.windows.key_press(skill.min_si.key)

    def normal(self, skill: SkillSiMing):

        if self.exist_buffer(self.img_buff_zu_fu):
            self.wait(0.4)

        if self.fu_wen_is_wait():
            _logger.info("玉虹")
            self.wait(0.1)
            self.windows.key_press(skill.yu_hong.key)
            self.wait(0.1)

        if self.ling_li.score(self.screen()) < 15 and skill.ci_fu.is_ok():
            _logger.info("赐福")
            self.windows.key_press(skill.ci_fu.key)
            self.wait(0.3)
            return

        if self.fu_wen_is_ok():
            self.use_gun_si(skill)

        if skill.hong_guang.is_ok() \
                or skill.hong_guang_ci_fu.is_ok() \
                or self.exist_buffer(self.img_buff_liu_guang):
            if not (self.exist_skill(self.img_skill_hg_ci_fu)):
                self.wait()
                _logger.info("虹光")
                self.windows.key_press(skill.hong_guang.key)
                self.wait()
            else:
                print("exist ci fu hong guan")

        if skill.min_si.is_ok() and self.exist_fu_wen(self.img_fu_wen_some):
            _logger.info("明视")
            self.windows.key_press(skill.min_si.key)
            self.wait()

        if (not self.exist_buffer(self.img_buff_zu_fu)) and millisecond() - self.before_time > 1500:
            self.use_e(skill)
        if self.exist_buffer(self.img_buff_qjwh):
            self.become(SkillStatus.Explosive)

    def explosive(self, skill: SkillSiMing):
        if self.exist_buffer(self.img_buff_qjwh):
            _logger.info("explosive [q]")
            self.use_e(skill)
        else:
            self.become(SkillStatus.Normal)

    def clear(self):
        if self.status is not None:
            self.status = None
            time.sleep(0.1)
            self.windows.key_press("q")
            print("clear")

    def pve(self):
        if self.status is None:
            self.windows.key_down("q")
            time.sleep(2.2)
            self.windows.key_up("q")
        self.update_screen()
        self.run()

    def pvp(self):
        self.update_screen()
        if self.status is not None:
            self.run()
            return
        if self.skill().jin_yu.is_ok():
            self.windows.key_press(self.skill().jin_yu.key)
            self.wait(0.3)
            self.update_screen()
            if self.exist_fu_wen(self.img_fu_wen_jin_yu):
                _logger.info("金羽 释放成功")
                self.windows.key_press(self.skill().hong_guang.key)
                self.run()
            else:
                _logger.info("金羽 释放失败")

    def run(self):
        skill = self.skill()
        if self.mouse_tap_if_need():
            logging.info("mouse tap")
            return

        elif self.status is None:
            self.become(SkillStatus.Start)

        elif self.status is SkillStatus.Start:
            self.start(skill)
            self.become(SkillStatus.Normal)

        elif self.status is SkillStatus.Normal:
            self.normal(skill)

        elif self.status is SkillStatus.Explosive:
            self.explosive(skill)
