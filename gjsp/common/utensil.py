import os
import time
from os.path import dirname, abspath

import numpy as np
from PIL import Image


def array2img(array):
    return Image.fromarray(np.abs(array).astype("uint8"))


def millisecond() -> int:
    return int(time.time() * 1000.0)


def pass_second() -> int:
    global start_time
    return int((millisecond() - start_time) / 1000)


def goal_image(file_name: str) -> Image.Image:
    return Image.open(user_dir + "image_goal\\" + file_name)


def get_user_dir() -> str:
    _user_dir = abspath(os.getcwd())
    i = 0
    while not os.path.exists(_user_dir + "\\image_goal"):
        _user_dir = dirname(_user_dir)
        i += 1
        assert i < 10, "can not find image_goal in %s" % (os.getcwd())
    return str(_user_dir) + "\\"


user_dir: str = get_user_dir()
start_time = millisecond()
