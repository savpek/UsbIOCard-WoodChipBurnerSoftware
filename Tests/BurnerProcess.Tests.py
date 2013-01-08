# coding=utf-8
import unittest
from mock import call, Mock
from Burner import Burner
from BurnerController import BurnerController

class BurnerTests(unittest.TestCase):
    _burnerController = None
    _burner = None

    def setUp(self):
        self._burner = Mock(spec=Burner)
        self._burnerController = BurnerController(self._burner)

    def test_adc_value_calculates_average_from_list_correctly(self):
        pass
