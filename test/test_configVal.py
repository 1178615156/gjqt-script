from unittest import TestCase
from gjsp.common.const_value import ConfigVal

class TestConfigVal(TestCase):
    def test_value(self):
        assert (ConfigVal.dm_add_code == "")