import os
from unittest import TestCase
from gjsp.common.utensil import *


class TestRegCode(TestCase):
    def test_reg_code(self):
        s = list(open(user_dir + "dm_reg_code.txt").readlines())[0]
        [a, b] = (s.split("--"))
        print(a, b)
