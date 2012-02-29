import unittest

from diffcalc.gdasupport.scannable.parameter import \
    DiffractionCalculatorParameter
from tests.diffcalc.gdasupport.scannable.mockdiffcalc import MockDiffcalc,\
    MockParametarManger


class TestDiffractionCalculatorParameter(unittest.TestCase):

    def setUp(self):
        self.dcp = DiffractionCalculatorParameter('dcp', 'betain',
                                                  MockParametarManger())

    def testAsynchronousMoveToAndGetPosition(self):
        self.dcp.asynchronousMoveTo(12.3)
        self.assertEqual(self.dcp.getPosition(), 12.3)

    def testIsBusy(self):
        self.assertEqual(self.dcp.isBusy(), False)
