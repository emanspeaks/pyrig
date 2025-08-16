from unittest import TestCase, main as utmain, TextTestRunner, mock
import sys
from os import environ
from pathlib import Path

HERE = Path(__file__).expanduser().resolve().parent
REPOROOT = HERE.parent
if __name__ == '__main__':
    sys.path.append(str(REPOROOT))

    # so we can get testing constants without importing pyrig
    sys.path.insert(0, str(REPOROOT/'pyrig/_testing'))

from _pyrig_testing import (  # noqa: E402
    ENV_PYRIG_UNITTEST_ACTIVE,
)


@mock.patch.dict(environ, {ENV_PYRIG_UNITTEST_ACTIVE: '1'})
class TestPyRig(TestCase):
    def test_import(self):
        import pyrig  # noqa: F401

    def test_rounding(self):
        self.assertEqual(round(1300 / 8), 162)
        self.assertEqual(round(325 / 2), 162)
        self.assertEqual(round(235 / 2), 118)
        self.assertEqual(round(5, -1), 0)

        from pyapp.utils.math import round_half_up
        self.assertEqual(round_half_up(1300 / 8), 163)
        self.assertEqual(round_half_up(325 / 2), 163)
        self.assertEqual(round_half_up(235 / 2), 118)
        self.assertEqual(round_half_up(5, -1), 10)

    def test_money(self):
        from pyrig.models.acctng.money import Money
        with self.assertRaises(TypeError):
            Money(1, 1000000)

        mval1 = 123.456789
        mval2 = 987.654321

        m = Money(mval1)
        mdup = Money(mval1)
        mneg = Money(-mval2)

        self.assertEqual(m.intval, 1234568)
        self.assertEqual(str(m), '$123.46')
        self.assertEqual(f'{m}', '$123.46')
        self.assertEqual(repr(m), "Money(intval=1234568)")
        self.assertEqual(f'{m!r}', "Money(intval=1234568)")
        self.assertEqual(float(m), 123.4568)
        self.assertEqual(int(m), 123)
        self.assertEqual(round(m, -2), 100)
        self.assertEqual(round(m, -1), 120)
        self.assertEqual(round(m, 1), 123.5)
        self.assertEqual(round(m, 2), 123.46)
        self.assertEqual(round(m, 3), 123.457)
        self.assertEqual(round(m, 4), 123.4568)
        with self.assertRaises(ValueError):
            round(m, 5)

        self.assertTrue(bool(m))
        self.assertFalse(bool(Money(0)))
        self.assertFalse(bool(Money()))

        self.assertEqual(+m, m)
        self.assertEqual(+mneg, mneg)

        self.assertEqual(-m, Money(-mval1))
        self.assertEqual(-mneg, Money(mval2))

        self.assertEqual(m + mdup, Money(mval1 + mval1))
        self.assertEqual(m + mneg, Money(mval1 - mval2))
        self.assertEqual(m + 0, m)
        with self.assertRaises(TypeError):
            m + 1

        self.assertEqual(m - mdup, Money(0))
        self.assertEqual(m - mdup, Money())
        self.assertEqual(m - mneg, Money(mval1 + mval2))
        self.assertEqual(m - 0, m)
        with self.assertRaises(TypeError):
            m - 1

        self.assertEqual(m*2, Money(mval1*2))
        with self.assertRaises(TypeError):
            m*m

        self.assertEqual(m/2, Money(mval1/2))
        self.assertEqual(m/mdup, 1.0)
        self.assertAlmostEqual(m/mneg, -mval1/mval2)
        from pyapp.utils.math import round_half_up
        self.assertEqual(m/mneg,
                         -round_half_up(mval1, 4)/round_half_up(mval2, 4))

        self.assertEqual(0 + m, m)
        with self.assertRaises(TypeError):
            1 + m

        self.assertEqual(0 - m, -m)
        self.assertEqual(0 - mneg, Money(mval2))
        with self.assertRaises(TypeError):
            1 - m

        self.assertEqual(2*m, Money(mval1*2))

        with self.assertRaises(TypeError):
            1/m

        self.assertEqual(abs(m), m)
        self.assertEqual(abs(mneg), Money(mval2))

        self.assertTrue(m == mdup)
        self.assertFalse(m == mneg)
        self.assertTrue(Money() == 0)
        self.assertTrue(0 == Money())
        self.assertFalse(m == mval1)
        self.assertFalse(mval1 == m)

        self.assertFalse(m != mdup)
        self.assertTrue(m != mneg)
        self.assertFalse(Money() != 0)
        self.assertFalse(0 != Money())
        self.assertTrue(m != mval1)
        self.assertTrue(mval1 != m)

        self.assertTrue(m > 0)
        self.assertTrue(0 > mneg)
        self.assertTrue(m > mneg)
        self.assertFalse(mdup > m)
        self.assertFalse(0 > m)
        self.assertFalse(mneg > 0)
        self.assertFalse(mneg > m)
        with self.assertRaises(TypeError):
            m > 1

        with self.assertRaises(TypeError):
            1 > m

        self.assertTrue(m >= 0)
        self.assertTrue(0 >= mneg)
        self.assertTrue(m >= mneg)
        self.assertTrue(mdup >= m)
        self.assertFalse(0 >= m)
        self.assertFalse(mneg >= 0)
        self.assertFalse(mneg >= m)
        with self.assertRaises(TypeError):
            m >= 1

        with self.assertRaises(TypeError):
            1 >= m

        self.assertFalse(m < 0)
        self.assertFalse(0 < mneg)
        self.assertFalse(m < mneg)
        self.assertFalse(mdup < m)
        self.assertTrue(0 < m)
        self.assertTrue(mneg < 0)
        self.assertTrue(mneg < m)
        with self.assertRaises(TypeError):
            m < 1

        with self.assertRaises(TypeError):
            1 < m

        self.assertFalse(m <= 0)
        self.assertFalse(0 <= mneg)
        self.assertFalse(m <= mneg)
        self.assertTrue(mdup <= m)
        self.assertTrue(0 <= m)
        self.assertTrue(mneg <= 0)
        self.assertTrue(mneg <= m)
        with self.assertRaises(TypeError):
            m <= 1

        with self.assertRaises(TypeError):
            1 <= m


if __name__ == '__main__':
    ttr = TextTestRunner(stream=sys.stdout,
                         verbosity=9,
                         failfast=True)
    try:
        utmain(testRunner=ttr)
    except SystemExit:
        pass
