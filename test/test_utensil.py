import os
from unittest import TestCase
from gjsp.common.utensil import *

from os.path import dirname, abspath

class TestUtensil(TestCase):
    def test_user_dir(self):

        assert (str(user_dir) == "D:\\gjqt\\gjqt-script\\")
