from pyapp.utils.math import round_half_away


class Fixed4:
    DIGITS = 4
    INTSCALAR = 10**DIGITS
    __slots__ = ('__intval',)

    def __init__(self, value: 'float | int | str | Fixed4 | None' = None,
                 intval: int | None = None):
        if value is not None and intval is not None:
            raise TypeError("Cannot specify both 'value' and 'intval'")

        if value:
            intval = (value.__intval if isinstance(value, Fixed4)
                      else round_half_away(float(value)*self.INTSCALAR))

        self.__intval = intval or 0

    @property
    def intval(self):
        return self.__intval

    def __repr__(self):
        return f"Fixed4(intval={self.__intval})"

    def __str__(self):
        return f"{float(self):.4f}"

    def __bool__(self):
        return bool(self.__intval)

    def __round__(self, n: int = 0):
        """
        Round the Fixed4 value to a given number of decimal places.

        This does NOT apply banker's rounding; returns half-away rounding.
        """
        intval = self.__intval
        expo = self.DIGITS - (n or 0)
        out = round_half_away(intval, -expo)/self.INTSCALAR
        if n <= 0:
            return int(out)
        elif n > self.DIGITS:
            raise ValueError("Cannot round to more than 4 decimal places")
        return out

    def __float__(self):
        return self.__intval/self.INTSCALAR

    def __int__(self):
        return round(self)

    def __pos__(self):
        return self.__class__(self)

    def __neg__(self):
        return self.__class__(intval=-self.__intval)

    def _add_fixed4(self, other: 'Fixed4'):
        return self.__class__(intval=self.__intval + other.__intval)

    def __add__(self, other):
        """
        If you want to get a float value, you need to call float() on the
        Fixed4 instance first and then operate on the floats.  Otherwise, we
        assume you want to continue working in fixed precision.
        """
        if other == 0:
            return self
        if not isinstance(other, Fixed4):
            return self + self.__class__(other)
        if not type(other) is Fixed4:
            return NotImplemented
        return self._add_fixed4(other)

    def __sub__(self, other):
        return self + -other

    def _mul_fixed4(self, other: 'Fixed4'):
        # M1 * M2 = M1x/1e4 * M2x/1e4 = M1x*M2x/1e8 = (M1x*M2x/1e4) / 1e4
        x = self.__intval*other.__intval/self.INTSCALAR
        return self.__class__(intval=round_half_away(x))

    def __mul__(self, other):
        """
        If you want to get a float value, you need to call float() on the
        Fixed4 instance first and then operate on the floats.  Otherwise, we
        assume you want to continue working in fixed precision.
        """
        if other == 0:
            return self.__class__()
        if other == 1:
            return self
        if not isinstance(other, Fixed4):
            return self.__class__(intval=round_half_away(self.__intval*other))
        if not type(other) is Fixed4:
            return NotImplemented
        return self._mul_fixed4(other)

    def _truediv_fixed4(self, other: 'Fixed4'):
        # M1 / M2 = M1x/10000 / M2x/10000
        # return self.__class__(self.__intval/other.__intval)
        return self.__intval/other.__intval

    def __truediv__(self, other):
        """
        If you want to get a float value, you need to call float() on the
        Fixed4 instance first and then operate on the floats.  Otherwise, we
        assume you want to continue working in fixed precision.

        The exception is if you divide two Fixed4 instances, which will return
        a float.
        """
        if other == 1:
            return self
        if not isinstance(other, Fixed4):
            return self.__class__(intval=round_half_away(self.__intval/other))
        if not type(other) is Fixed4:
            return NotImplemented
        return self._truediv_fixed4(other)

    __radd__ = __add__

    def __rsub__(self, other):
        return other + -self

    __rmul__ = __mul__

    def __rtruediv__(self, other):
        return self.__class__(other*self.INTSCALAR/self.__intval)

    def __abs__(self):
        return self.__class__(intval=abs(self.__intval))

    def __eq__(self, other):
        if isinstance(other, Fixed4):
            return self.__intval == other.__intval
        return other == 0 and not self.__intval

    def __lt__(self, other):
        if other == 0:
            return self.__intval < 0
        if not isinstance(other, Fixed4):
            raise TypeError('Cannot compare Fixed4 to non-Fixed4')
        return self.__intval < other.__intval

    def __gt__(self, other):
        if other == 0:
            return self.__intval > 0
        if not isinstance(other, Fixed4):
            raise TypeError('Cannot compare Fixed4 to non-Fixed4')
        return self.__intval > other.__intval

    def __le__(self, other):
        return self == other or self < other

    def __ge__(self, other):
        return self == other or self > other

    def __floordiv__(self, other):
        return int(float(self) // other)

    def __mod__(self, other):
        denom = (other.__intval if isinstance(other, Fixed4)
                 else other*self.INTSCALAR)
        return self.__class__(intval=round_half_away(self.__intval % denom))

    def __divmod__(self, other):
        return self // other, self % other

    def __rfloordiv__(self, other):
        return int(other // float(self))

    def __rmod__(self, other):
        return other % float(self)  # i'm lazy

    def __rdivmod__(self, other):
        return other // self, other % self

    def __trunc__(self):
        # x = floor(self)
        # return x + (x < 0)
        scl = self.INTSCALAR
        flr = self.__intval // scl
        return self.__class__(intval=(flr + (flr < 0))*scl)

    def __floor__(self):
        # return self.__intval // self.INTSCALAR
        scl = self.INTSCALAR
        return self.__class__(intval=(self.__intval // scl)*scl)

    def __ceil__(self):
        # quo, rem = divmod(self.__intval, self.INTSCALAR)
        # return quo + (rem > 0)
        intval = self.__intval
        scl = self.INTSCALAR
        quo, rem = divmod(intval, scl)
        return self.__class__(intval=(quo + (rem > 0))*scl)

    # these should really be handled as floats to reduce complexity here since
    # they will likely be rarely used

    # def __pow__(self, other, modulo=None):
    #     return self.__class__(pow(float(self), other, modulo))

    # def __rpow__(self, other, modulo=None):
    #     return NotImplemented
