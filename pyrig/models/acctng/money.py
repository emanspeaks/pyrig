# from math import floor

from pyapp.utils.math import round_half_up


class Money:
    DIGITS = 4
    INTSCALAR = 10**DIGITS
    __slots__ = ('__intval',)

    def __init__(self, value: 'float | int | str | Money | None' = None,
                 intval: int | None = None):
        if value is not None and intval is not None:
            raise TypeError("Cannot specify both 'value' and 'intval'")

        if value:
            intval = (value.__intval if isinstance(value, Money)
                      else round_half_up(float(value)*self.INTSCALAR))

        self.__intval = intval or 0

    @property
    def intval(self):
        return self.__intval

    def __repr__(self):
        return f"Money(intval={self.__intval})"

    def __str__(self):
        return f"${round(self, 2):.2f}"

    def __bool__(self):
        return bool(self.__intval)

    def __round__(self, n: int = 0):
        """
        Round the Money value to a given number of decimal places.

        This does NOT apply banker's rounding; returns half-up rounding.
        """
        intval = self.__intval
        expo = self.DIGITS - (n or 0)
        out = round_half_up(intval, -expo)/self.INTSCALAR
        if n <= 0:
            return int(out)
        elif n > self.DIGITS:
            raise ValueError("Cannot round to more than 4 decimal places")
        return out

    def __float__(self):
        return self.__intval/self.INTSCALAR

    # note: note defining this defaults to calling __trunc__()
    # def __int__(self):
    #     return round(self)

    def __pos__(self):
        return Money(self)

    def __neg__(self):
        return Money(intval=-self.__intval)

    def __add__(self, other):
        if other == 0:
            return self
        if not isinstance(other, Money):
            return NotImplemented
        return Money(intval=self.__intval + other.__intval)

    def __sub__(self, other):
        return self + -other

    def __mul__(self, other):
        if isinstance(other, Money):
            raise TypeError("Cannot multiply two Money instances.")
        return Money(intval=self.__intval*other)

    def __truediv__(self, other):
        # M1 / M2 = M1x/10000 / M2x/10000
        if isinstance(other, Money):
            return self.__intval/other.__intval
        return Money(intval=self.__intval/other)

    __radd__ = __add__

    def __rsub__(self, other):
        return other + -self

    __rmul__ = __mul__

    def __rtruediv__(self, other: object):
        return NotImplemented

    def __abs__(self):
        return Money(intval=abs(self.__intval))

    def __eq__(self, other):
        if isinstance(other, Money):
            return self.__intval == other.__intval
        return other == 0 and not self.__intval

    def __lt__(self, other):
        if other == 0:
            return self.__intval < 0
        if not isinstance(other, Money):
            raise TypeError('Cannot compare Money to non-Money')
        return self.__intval < other.__intval

    def __gt__(self, other):
        if other == 0:
            return self.__intval > 0
        if not isinstance(other, Money):
            raise TypeError('Cannot compare Money to non-Money')
        return self.__intval > other.__intval

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self == other

    # object.__floordiv__(self, other)
    # object.__mod__(self, other)
    # object.__divmod__(self, other)
    # object.__pow__(self, other[, modulo])
    # object.__rfloordiv__(self, other)
    # object.__rmod__(self, other)
    # object.__rdivmod__(self, other)
    # object.__rpow__(self, other[, modulo])
    # object.__trunc__(self)
    # object.__floor__(self)
    # object.__ceil__(self)
