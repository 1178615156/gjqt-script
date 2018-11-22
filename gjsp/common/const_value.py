from gjsp.common.utensil import goal_image, user_dir
from pyhocon import ConfigFactory, ConfigTree
from typing import List


class AreaVal:
    fu_wen = (750, 800, 1000, 1080)
    buff = (400, 800, 850, 900)
    skill = (0, 600, 400, 710)
    mouse_tap = (1000, 400, 1300, 600)
    dot = (300, 40, 600, 200)


class GlobalVal:
    img_war_npc = goal_image("war_npc.bmp")
    img_mouse_left = goal_image("mouse_left.bmp")
    img_mouse_right = goal_image("mouse_right.bmp")


class SmVal:

    img_fu_wen_empty = goal_image("sm_fu_wen_empty.bmp")
    img_fu_wen_empty_plus = goal_image("sm_fu_wen_empty_plus.bmp")

    img_fu_wen_gun_si = goal_image("sm_fu_wen_gun_si.bmp")
    img_fu_wen_wait = goal_image("si_ming_fu_wen_wait.bmp")
    img_fu_wen_jin_yu = goal_image("sm_fu_wen_jin_yu.bmp")

    fu_wen_icon = goal_image("sm_fu_wen_icon.jpg")
    fu_wen_ling_li = goal_image("sm_fu_wen_ling_li.bmp")

    buff_qjwh = goal_image("si_ming_buff_qjwh.bmp")
    buff_zu_fu = goal_image("si_ming_buff_ci_fu.bmp")
    buff_zu_fu_full = goal_image("si_ming_buff_ci_fu_full.bmp")
    buff_liu_guang = goal_image("si_ming_buff_liu_guang.bmp")

    class SkillImg:
        __img = staticmethod(lambda name: goal_image("sm_skill_%s.bmp" % (name))).__func__
        q = __img("q")
        e = __img("e")
        gun_si = __img("gun_si")
        ji_qin = __img("ji_qin")
        ci_fu = __img("ci_fu")
        yu_hong = __img("yu_hong")
        jin_yu = __img("jin_yu")
        ling_li = __img("ling_li")
        hong_guang = __img("hong_guang")
        hg_liu_guang = goal_image("sm_skill_hong_guang_liu_guang.bmp")
        hong_guan_ci_fu = goal_image("sm_skill_hong_guang_ci_fu.bmp")
        hong_guang_mei_lan = goal_image("sm_skill_hong_guang_mei_lan.bmp")

    dot_ben_huai_1 = goal_image("sm_dot_ben_huai_1.jpg")
    dot_ben_huai_2 = goal_image("sm_dot_ben_huai_2.jpg")
    dot_ben_huai_3 = goal_image("sm_dot_ben_huai_3.jpg")
    dot_ben_huai_4 = goal_image("sm_dot_ben_huai_4.jpg")
    dot_ling_li = goal_image("sm_dot_ling_li.bmp")

    ling_li_word = goal_image("si_ming_ling_li_word.jpg")


class ConfigVal:
    config = ConfigFactory.parse_file(user_dir + "application.conf")
    dm_reg_list: List[ConfigTree] = config.get("dm_reg_list")
    fish_size = config.get("fish.size", 1)
