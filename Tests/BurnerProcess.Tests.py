# coding=utf-8
import unittest
from Burner import Burner
from mock import call, MagicMock, Mock
from BurnerProcess import BurnerProcess
from UsbCard import IoCardException


class BurnerTests(unittest.TestCase):
    _burnerProcess = None
    _burner = None

    def setUp(self):
        self._burner = Mock(spec=Burner)
        self._burnerProcess = BurnerProcess(self._burner)

    def test_abc(self):
        pass