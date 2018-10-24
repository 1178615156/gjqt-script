from gjsp.common.utensil import goal_image, user_dir
from pyhocon import ConfigFactory

# 废弃,
area_fu_wen = (800, 800, 1000, 1080)
area_buff = (400, 800, 850, 900)
area_skill = (0, 600, 400, 710)
area_mouse_tap = (1000, 400, 1300, 600)
# 废弃,
img_war_npc = goal_image("war_npc.bmp")
img_mouse_left = goal_image("mouse_left.bmp")
img_mouse_right = goal_image("mouse_right.bmp")


class Area:
    fu_wen = (750, 800, 1000, 1080)
    buff = (400, 800, 850, 900)
    skill = (0, 600, 400, 710)
    mouse_tap = (1000, 400, 1300, 600)
    dot = (300, 40, 600, 200)


class Global:
    img_war_npc = goal_image("war_npc.bmp")
    img_mouse_left = goal_image("mouse_left.bmp")
    img_mouse_right = goal_image("mouse_right.bmp")


class SmVal:
    img_fu_wen_empty = goal_image("si_ming_fu_wen_empty.bmp")
    img_fu_wen_empty_plus = goal_image("si_ming_fu_wen_empty_plus.bmp")

    img_fu_wen_gun_si = goal_image("si_ming_fu_wen_some.bmp")
    img_fu_wen_wait = goal_image("si_ming_fu_wen_wait.bmp")
    img_fu_wen_jin_yu = goal_image("si_ming_fu_wen_jin_yu.bmp")

    buff_qjwh = goal_image("si_ming_buff_qjwh.bmp")
    buff_zu_fu = goal_image("si_ming_buff_ci_fu.bmp")
    buff_zu_fu_full = goal_image("si_ming_buff_ci_fu_full.bmp")
    buff_liu_guang = goal_image("si_ming_buff_liu_guang.bmp")

    skill_hg_liu_guang = goal_image("si_ming_skill_hong_guang_liu_guang.bmp")
    skill_hg_ci_fu = goal_image("si_ming_skill_hong_guang_ci_fu.bmp")
    skill_hg_mei_lan = goal_image("si_ming_skill_hong_guang_mei_lan.bmp")

    dot_ben_huai_1 = goal_image("si_ming_dot_ben_huai_1.jpg")
    dot_ben_huai_2 = goal_image("si_ming_dot_ben_huai_2.jpg")
    dot_ben_huai_3 = goal_image("si_ming_dot_ben_huai_3.jpg")
    dot_ben_huai_4 = goal_image("si_ming_dot_ben_huai_4.jpg")

    ling_li_word = goal_image("si_ming_ling_li_word.jpg")


class ConfigVal:
    config = ConfigFactory.parse_file(user_dir + "application.conf")
    dm_reg_code = config.get("dm.reg_code", "")
    dm_add_code = config.get("dm.add_code", "")
    fish_size = config.get("fish.size", 1)
