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

        from pyapp.utils.math import round_half_away
        self.assertEqual(round_half_away(1300 / 8), 163)
        self.assertEqual(round_half_away(325 / 2), 163)
        self.assertEqual(round_half_away(235 / 2), 118)
        self.assertEqual(round_half_away(5, -1), 10)

    def test_fixed4(self):
        from pyrig.models.acctng.fixed4 import Fixed4
        with self.assertRaises(TypeError):
            Fixed4(1, 1000000)

        fval1 = 123.456789
        fval2 = 987.654321

        f = Fixed4(fval1)
        fdup = Fixed4(fval1)
        fneg = Fixed4(-fval2)

        self.assertEqual(f.intval, 1234568)
        self.assertEqual(str(f), '123.4568')
        self.assertEqual(f'{f}', '123.4568')
        self.assertEqual(repr(f), "Fixed4(intval=1234568)")
        self.assertEqual(f'{f!r}', "Fixed4(intval=1234568)")
        self.assertEqual(float(f), 123.4568)
        self.assertEqual(int(f), 123)
        self.assertEqual(int(fneg), -988)
        self.assertEqual(round(f, -2), 100)
        self.assertEqual(round(f, -1), 120)
        self.assertEqual(round(f, 1), 123.5)
        self.assertEqual(round(f, 2), 123.46)
        self.assertEqual(round(f, 3), 123.457)
        self.assertEqual(round(f, 4), 123.4568)
        with self.assertRaises(ValueError):
            round(f, 5)

        self.assertTrue(bool(f))
        self.assertFalse(bool(Fixed4(0)))
        self.assertFalse(bool(Fixed4()))

        self.assertEqual(+f, f)
        self.assertEqual(+fneg, fneg)

        self.assertEqual(-f, Fixed4(-fval1))
        self.assertEqual(-fneg, Fixed4(fval2))

        self.assertEqual(f + fdup, Fixed4(fval1 + fval1))
        self.assertEqual(f + fneg, Fixed4(fval1 - fval2))
        self.assertEqual(f + 0, f)
        self.assertEqual(f + 1, Fixed4(fval1 + 1))

        self.assertEqual(f - fdup, Fixed4(0))
        self.assertEqual(f - fdup, Fixed4())
        self.assertEqual(f - fneg, Fixed4(fval1 + fval2))
        self.assertEqual(f - 0, f)
        self.assertEqual(f - 1, Fixed4(fval1 - 1))

        self.assertEqual(f*2, Fixed4(fval1*2))
        self.assertEqual(f*f, Fixed4(123.4568*123.4568))

        self.assertEqual(f/2, Fixed4(fval1/2))
        # self.assertEqual(f/fdup, Fixed4(1))
        self.assertEqual(f/fdup, 1.0)
        # self.assertAlmostEqual(float(f/fneg), -fval1/fval2)
        self.assertAlmostEqual(f/fneg, -fval1/fval2)
        # self.assertEqual(f/fneg, Fixed4(-fval1/fval2))
        from pyapp.utils.math import round_half_away
        self.assertEqual(f/fneg,
                         -round_half_away(fval1, 4)/round_half_away(fval2, 4))

        self.assertEqual(0 + f, f)
        self.assertEqual(1 + f, Fixed4(fval1 + 1))

        self.assertEqual(0 - f, -f)
        self.assertEqual(0 - fneg, Fixed4(fval2))
        self.assertEqual(1 - f, Fixed4(1 - fval1))

        self.assertEqual(2*f, Fixed4(fval1*2))

        self.assertEqual(1/f, Fixed4(1/fval1))

        self.assertEqual(abs(f), f)
        self.assertEqual(abs(fneg), Fixed4(fval2))

        self.assertTrue(f == fdup)
        self.assertFalse(f == fneg)
        self.assertTrue(Fixed4() == 0)
        self.assertTrue(0 == Fixed4())
        self.assertFalse(f == fval1)
        self.assertFalse(fval1 == f)

        self.assertFalse(f != fdup)
        self.assertTrue(f != fneg)
        self.assertFalse(Fixed4() != 0)
        self.assertFalse(0 != Fixed4())
        self.assertTrue(f != fval1)
        self.assertTrue(fval1 != f)

        self.assertTrue(f > 0)
        self.assertTrue(0 > fneg)
        self.assertTrue(f > fneg)
        self.assertFalse(fdup > f)
        self.assertFalse(0 > f)
        self.assertFalse(fneg > 0)
        self.assertFalse(fneg > f)
        with self.assertRaises(TypeError):
            f > 1

        with self.assertRaises(TypeError):
            1 > f

        self.assertTrue(f >= 0)
        self.assertTrue(0 >= fneg)
        self.assertTrue(f >= fneg)
        self.assertTrue(fdup >= f)
        self.assertFalse(0 >= f)
        self.assertFalse(fneg >= 0)
        self.assertFalse(fneg >= f)
        with self.assertRaises(TypeError):
            f >= 1

        with self.assertRaises(TypeError):
            1 >= f

        self.assertFalse(f < 0)
        self.assertFalse(0 < fneg)
        self.assertFalse(f < fneg)
        self.assertFalse(fdup < f)
        self.assertTrue(0 < f)
        self.assertTrue(fneg < 0)
        self.assertTrue(fneg < f)
        with self.assertRaises(TypeError):
            f < 1

        with self.assertRaises(TypeError):
            1 < f

        self.assertFalse(f <= 0)
        self.assertFalse(0 <= fneg)
        self.assertFalse(f <= fneg)
        self.assertTrue(fdup <= f)
        self.assertTrue(0 <= f)
        self.assertTrue(fneg <= 0)
        self.assertTrue(fneg <= f)
        with self.assertRaises(TypeError):
            f <= 1

        with self.assertRaises(TypeError):
            1 <= f

        self.assertEqual(f // 100, 1)
        self.assertEqual(fneg // 100, -10)
        self.assertEqual(fneg // f, -8)

        self.assertEqual(f % 100, Fixed4(23.4568))
        self.assertEqual(fneg % 100, Fixed4(12.3457))
        self.assertEqual(fneg % f, Fixed4(0.0001))
        self.assertEqual(f % fneg, Fixed4(-864.1975))

        self.assertEqual(divmod(f, 100), (1, Fixed4(23.4568)))
        self.assertEqual(divmod(fneg, 100), (-10, Fixed4(12.3457)))
        self.assertEqual(divmod(fneg, f), (-8, Fixed4(0.0001)))

        self.assertEqual(1000 // f, 8)

        self.assertEqual(1000 % f, 1000 % float(f))

        self.assertEqual(divmod(1000, f), (8, 1000 % float(f)))

        from math import floor, ceil, trunc

        self.assertEqual(trunc(f), Fixed4(123))
        self.assertEqual(trunc(fneg), Fixed4(-987))

        self.assertEqual(floor(f), Fixed4(123))
        self.assertEqual(floor(fneg), Fixed4(-988))

        self.assertEqual(ceil(f), Fixed4(124))
        self.assertEqual(ceil(fneg), Fixed4(-987))

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
        from pyapp.utils.math import round_half_away
        self.assertEqual(m/mneg,
                         -round_half_away(mval1, 4)/round_half_away(mval2, 4))

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

        self.assertEqual(m // 100, 1)
        self.assertEqual(mneg // 100, -10)
        self.assertEqual(mneg // m, -8)

        self.assertEqual(m % 100, Money(23.4568))
        self.assertEqual(mneg % 100, Money(12.3457))
        self.assertEqual(mneg % m, Money(0.0001))
        self.assertEqual(m % mneg, Money(-864.1975))

        self.assertEqual(divmod(m, 100), (1, Money(23.4568)))
        self.assertEqual(divmod(mneg, 100), (-10, Money(12.3457)))
        self.assertEqual(divmod(mneg, m), (-8, Money(0.0001)))

        self.assertEqual(1000 // m, 8)

        self.assertEqual(1000 % m, 1000 % float(m))

        self.assertEqual(divmod(1000, m), (8, 1000 % float(m)))

        from math import floor, ceil, trunc

        self.assertEqual(trunc(m), Money(123))
        self.assertEqual(trunc(mneg), Money(-987))

        self.assertEqual(floor(m), Money(123))
        self.assertEqual(floor(mneg), Money(-988))

        self.assertEqual(ceil(m), Money(124))
        self.assertEqual(ceil(mneg), Money(-987))


if __name__ == '__main__':
    ttr = TextTestRunner(stream=sys.stdout,
                         verbosity=9,
                         failfast=True)
    try:
        utmain(testRunner=ttr)
    except SystemExit:
        pass
