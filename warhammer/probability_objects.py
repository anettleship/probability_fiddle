import random
from fractions import Fraction


class DiceRoll:
    def __init__(self, sides: int = 6) -> None:
        self.sides = sides

    def roll(self) -> int:
        return random.randint(1, self.sides)


class ProbabilityConverter:
    @classmethod
    def float_to_fraction(cls, probability: float) -> tuple[int, int]:
        """Convert a float probability to fraction components (numerator, denominator)."""
        frac = Fraction(probability).limit_denominator(1000)
        return (frac.numerator, frac.denominator)