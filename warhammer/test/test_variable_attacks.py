"""Tests for weapons with variable attacks (e.g., D6, 2D6, D3)."""

import pytest

from ..warhammer_base import RangedWeapon
from ..warhammer import Unit
from ..warhammer_base import Model


def test_heavy_flamer_has_d6_attacks():
    """Regression test: Heavy Flamer should have 'D6' attacks, not averaged to 3."""
    heavy_flamer = RangedWeapon(
        name="Heavy Flamer",
        range=12,
        attacks="D6",
        ballistic_skill=0,  # Auto-hit
        strength=5,
        armour_penetration=-1,
        damage=1,
    )
    
    # Should preserve the string, not convert to average
    assert heavy_flamer.attacks == "D6", "Heavy Flamer should have 'D6' attacks"
    
    # Average should be 3.5
    assert heavy_flamer.get_average_attacks() == 3.5, "D6 average should be 3.5"


def test_weapon_with_d6_damage_in_probability_calculation():
    """Regression test: Probability calculations should use average damage for D6."""
    attacker = Model(
        name="Heavy Weapon Marine",
        movement=6,
        toughness=4,
        save=3,
        wounds=2,
        leadership=8,
        objective_control=1,
        ranged_weapons={
            "Lascannon": RangedWeapon(
                name="Lascannon",
                range=48,
                attacks=1,
                ballistic_skill=3,
                strength=9,
                armour_penetration=-3,
                damage="D6",
            )
        },
    )
    
    target = Model(
        name="Tank",
        movement=10,
        toughness=9,
        save=3,
        wounds=10,
        leadership=7,
        objective_control=1,
    )
    
    attacker_unit = Unit(models=[attacker], name="Marine Squad")
    target_unit = Unit(models=[target], name="Tank Squadron")
    
    # This should not crash with TypeError when multiplying "D6" string
    result = attacker_unit.shoot_at_return_probability(target_unit)
    
    # Should successfully calculate expected damage
    assert len(result.weapon_results) == 1
    assert result.weapon_results[0].expected_damage > 0
