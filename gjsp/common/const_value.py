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
    fu_wen = (800, 800, 1000, 1080)
    buff = (400, 800, 850, 900)
    skill = (0, 600, 400, 710)
    mouse_tap = (1000, 400, 1300, 600)


class Global:
    img_war_npc = goal_image("war_npc.bmp")
    img_mouse_left = goal_image("mouse_left.bmp")
    img_mouse_right = goal_image("mouse_right.bmp")


class SmVal:
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


class ConfigVal:
    config = ConfigFactory.parse_file(user_dir + "application.conf")
    dm_reg_code = config.get("dm.reg_code", "")
    dm_add_code = config.get("dm.add_code", "")
