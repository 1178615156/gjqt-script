import time

import numpy as np
from PIL import Image, ImageDraw
from gjsp.common.utensil import user_dir, goal_image
from gjsp.common.find_pic import FindPic
from gjsp.common import WindowsDm


class Fish:
    mark_cache = {}

    class Reward:
        area = (429, 258, 632, 462)
        default_color = np.array([90, 163, 192], dtype="uint8")
        goal_color = np.array([33, 78, 158])

    def __init__(self, hwnd, wind):
        at_fish = goal_image("at_fish.bmp")
        doing_fish = goal_image("四海生金.bmp")
        reward_fish = goal_image("fish_flag.bmp")

        self.hwnd = hwnd
        self.wind = wind

        self.find_at_fish = FindPic().goal(at_fish)
        self.find_doing_fish = FindPic().goal(doing_fish)
        self.find_reward_fish = FindPic().goal(reward_fish)

    @staticmethod
    def normal(img):
        return np.abs(np.array(img).astype(int) - Fish.Reward.default_color)

    @staticmethod
    def to_gray(img):
        y = np.array(img).astype(int) - Fish.Reward.goal_color
        y = np.mean(y, axis=2)
        y = ((y - np.mean(y)) / (np.max(y) - np.min(y)))
        y = y > 0.1
        return y * 255

    @staticmethod
    def circle_mark(size):
        img = Image.new(size=size, mode="L", color=(0))
        draw = ImageDraw.Draw(img)
        draw.ellipse((0, 0, img.width, img.height), fill=(1))
        return np.array(img)

    @staticmethod
    def pretreatment(img):
        size = img.size
        if size not in Fish.mark_cache:
            Fish.mark_cache[size] = Fish.circle_mark(size)

        return Fish.mark_cache[size] * Fish.to_gray(Fish.normal(img))

    @staticmethod
    def score(img):
        return np.count_nonzero(img) / np.size(img)

    def just_screen_shot(self):
        while True:
            img = self.wind.screen_shot()
            reward_img = img.crop(self.Reward.area)
            if self.find_reward_fish.original(reward_img).isFind():
                score = Fish.score(Fish.pretreatment(reward_img))
                reward_img.save(user_dir + "image_tmp\\%s-%s.jpg" % (int(time.time() * 1000.0), score))

    def run(self):
        before_score = 0
        score = 0
        is_end = False
        while not is_end:
            img = self.wind.screen_shot()
            reward_img = img.crop(self.Reward.area)

            if self.find_reward_fish.original(reward_img).isFind():
                score = Fish.score(Fish.pretreatment(reward_img))
                print("try get fish reward :" + str(before_score))
                if before_score - score > 0.004:
                    self.wind.key_press("q")
                    print("到达指定位置:%s,%s" % (score, before_score))
                    is_end = True
                    reward_img.save(user_dir + "image_tmp\\%s-%s.jpg" % (int(time.time() * 1000.0), score))
                    time.sleep(1)
                before_score = np.max([before_score, score])
                time.sleep(0.01)
            elif self.find_doing_fish.original(img).isFind():
                print("doing fish ")
                time.sleep(0.01)
            elif self.find_at_fish.original(img).isFind():
                self.wind.key_press("q")
                time.sleep(1)
                print("at fish , do fish")
            else:
                print("no at fish")
                time.sleep(1)


if __name__ == '__main__':
    print("start fish")
    windows = WindowsDm()
    gjqt_hwnd = list(windows.find_hwnd("古剑").keys())[0]
    print(gjqt_hwnd)
    windows.init(gjqt_hwnd)

    for i in range(20):
        print(i)
        Fish(gjqt_hwnd, windows).run()
#
