from .fixed4 import Fixed4


class Money(Fixed4):
    def __repr__(self):
        return f"Money(intval={self.intval})"

    def __str__(self):
        return f"${round(self, 2):.2f}"

    def __add__(self, other):
        if isinstance(other, (int, float)) and other == 0:
            return self
        if isinstance(other, Money):
            return self._add_fixed4(other)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Money):
            raise TypeError("Cannot multiply two Money instances.")
        return super().__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, Money):
            return self._truediv_fixed4(other)
        return super().__truediv__(other)

    __radd__ = __add__

    def __rtruediv__(self, other):
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, (int, float)) and other == 0:
            return self.intval < 0
        if not isinstance(other, Money):
            raise TypeError('Cannot compare Money to non-Money')
        return self.intval < other.intval

    def __gt__(self, other):
        if isinstance(other, (int, float)) and other == 0:
            return self.intval > 0
        if not isinstance(other, Money):
            raise TypeError('Cannot compare Money to non-Money')
        return self.intval > other.intval
