import pytest

from ..probability_objects import DiceRoll, ProbabilityConverter

def test_dice_roll_returns_number_within_range():

    dice = DiceRoll(sides=6)
    roll_result = dice.roll()
    assert 1 <= roll_result <= 6, "Dice roll should be between 1 and 6"


@pytest.mark.parametrize(
    "probability, expected_numerator, expected_denominator",
    [
        (0.5, 1, 2),      # Simple half
        (0.25, 1, 4),     # Quarter
        (0.75, 3, 4),     # Three quarters
        (0.333333, 1, 3), # Approximately one third
        (0.666667, 2, 3), # Approximately two thirds
        (0.2, 1, 5),      # One fifth
        (0.125, 1, 8),    # One eighth
        (0.166667, 1, 6), # Approximately one sixth (Warhammer relevant!)
        (0.135371179, 31, 229), # A more complex probability with prime numerator/denominator
    ],
)
def test_probability_converter_converts_float_to_fraction(
    probability, expected_numerator, expected_denominator
):
    """Test that various probabilities convert to correct fraction components."""
    numerator, denominator = ProbabilityConverter.float_to_fraction(probability)
    
    assert numerator == expected_numerator
    assert denominator == expected_denominator