import random


class DiceRoll:
    def __init__(self, sides: int = 6) -> None:
        self.sides = sides

    def roll(self) -> int:
        return random.randint(1, self.sides)