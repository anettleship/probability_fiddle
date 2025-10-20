from probability_objects import DiceRoll

def test_dice_roll_returns_number_within_range():

    dice = DiceRoll(sides=6)
    roll_result = dice.roll()
    assert 1 <= roll_result <= 6, "Dice roll should be between 1 and 6"