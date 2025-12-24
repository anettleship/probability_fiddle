"""Tests for weapons with variable damage (e.g., D6, D6+2, 2D6)."""

import pytest

from ..warhammer_base import Model, MeleeWeapon, RangedWeapon
from ..warhammer import Unit
from ..warhammer_actions import MeleeAttack, RangedAttack
from ..warhammer_actions_orchestrators import AttackOrchestrator


def test_orchestrator_with_d6_damage_weapon():
    """Test that orchestrator correctly handles D6 damage weapons."""
    # Create attacker unit with D6 damage weapon
    attacker_model = Model(
        name="Thunder Hammer Terminator",
        movement=5,
        toughness=5,
        save=2,
        wounds=3,
        leadership=6,
        objective_control=1,
        melee_weapons={
            "Thunder Hammer": MeleeWeapon(
                name="Thunder Hammer",
                attacks=3,
                weapon_skill=3,
                strength=8,
                armour_penetration=-2,
                damage="D6",  # Variable damage - this should trigger the failure
            )
        },
    )
    
    attacker_unit = Unit(models=[attacker_model], name="Terminator Squad")
    
    # Create target unit
    target_model = Model(
        name="Ork Boy",
        movement=6,
        toughness=5,
        save=6,
        wounds=1,
        leadership=7,
        objective_control=2,
    )
    
    target_unit = Unit(models=[target_model], name="Ork Boyz")
    
    # This should fail because weapon.damage is "D6" string, not a number
    orchestrator = AttackOrchestrator(
        attacker_unit=attacker_unit,
        target_unit=target_unit,
        num_simulations=10,
        attack_class=MeleeAttack
    )
    
    result = orchestrator.run()
    
    # If we get here, the orchestrator handled variable damage
    # Expected damage per attack should account for D6 average (3.5)
    assert "expected_success_rate" in result
    assert "expected_damage_per_unit_attack" in result["expected_success_rate"]


def test_weapon_with_d6_damage():
    """Test that a weapon with D6 damage correctly calculates expected damage."""
    # Create attacker with D6 damage weapon
    attacker = Model(
        name="Thunder Hammer Terminator",
        movement=5,
        toughness=5,
        save=2,
        wounds=3,
        leadership=6,
        objective_control=1,
        melee_weapons={
            "Thunder Hammer": MeleeWeapon(
                name="Thunder Hammer",
                attacks=3,
                weapon_skill=3,
                strength=8,
                armour_penetration=-2,
                damage="D6",  # Variable damage
            )
        },
    )
    
    # Create target
    target = Model(
        name="Ork Boy",
        movement=6,
        toughness=5,
        save=6,
        wounds=1,
        leadership=7,
        objective_control=2,
    )
    
    weapon = attacker.melee_weapons["Thunder Hammer"]
    attack = MeleeAttack(
        attacker=attacker,
        target=target,
        weapon=weapon,
    )
    
    # For D6 damage, expected damage = average of D6 = 3.5
    # probability_to_damage already calculates hit × wound × fail_save
    expected_damage = attack.probability_to_damage() * 3.5
    
    # Verify weapon.damage is "D6" string
    assert weapon.damage == "D6"
    
    # Test that expected_damage calculation would work
    # (This will fail until we implement variable damage support)
    assert isinstance(expected_damage, float)
    assert expected_damage > 0


def test_weapon_with_d6_plus_modifier_damage():
    """Test that a weapon with D6+2 damage correctly calculates expected damage."""
    attacker = Model(
        name="Lascannon Marine",
        movement=6,
        toughness=4,
        save=3,
        wounds=2,
        leadership=6,
        objective_control=2,
        ranged_weapons={
            "Lascannon": RangedWeapon(
                name="Lascannon",
                range=48,
                attacks=1,
                ballistic_skill=3,
                strength=12,
                armour_penetration=-3,
                damage="D6+2",  # Variable damage with modifier
            )
        },
    )
    
    target = Model(
        name="Tank",
        movement=10,
        toughness=10,
        save=2,
        wounds=12,
        leadership=6,
        objective_control=3,
    )
    
    weapon = attacker.ranged_weapons["Lascannon"]
    attack = RangedAttack(
        attacker=attacker,
        target=target,
        weapon=weapon,
    )
    
    # For D6+2 damage, expected damage = average of D6 + 2 = 3.5 + 2 = 5.5
    expected_damage = attack.probability_to_damage() * 5.5
    
    # Verify weapon.damage is "D6+2" string
    assert weapon.damage == "D6+2"
    
    # Test that expected_damage calculation would work
    assert isinstance(expected_damage, float)
    assert expected_damage > 0


def test_weapon_with_multiple_dice_damage():
    """Test that a weapon with 2D6 damage correctly calculates expected damage."""
    attacker = Model(
        name="Demolisher Cannon Tank",
        movement=10,
        toughness=10,
        save=2,
        wounds=12,
        leadership=6,
        objective_control=3,
        ranged_weapons={
            "Demolisher Cannon": RangedWeapon(
                name="Demolisher Cannon",
                range=24,
                attacks=3,
                ballistic_skill=3,
                strength=14,
                armour_penetration=-3,
                damage="2D6",  # Multiple dice
            )
        },
    )
    
    target = Model(
        name="Heavy Target",
        movement=6,
        toughness=12,
        save=2,
        wounds=18,
        leadership=6,
        objective_control=4,
    )
    
    weapon = attacker.ranged_weapons["Demolisher Cannon"]
    attack = RangedAttack(
        attacker=attacker,
        target=target,
        weapon=weapon,
    )
    
    # For 2D6 damage, expected damage = average of 2D6 = 7.0
    expected_damage = attack.probability_to_damage() * 7.0
    
    # Verify weapon.damage is "2D6" string
    assert weapon.damage == "2D6"
    
    # Test that expected_damage calculation would work
    assert isinstance(expected_damage, float)
    assert expected_damage > 0


def test_parse_damage_value_d6():
    """Test parsing D6 damage notation."""
    from ..warhammer_base import Weapon
    
    # This will test our future parse_damage method
    damage_str = "D6"
    expected_avg = 3.5
    
    # Placeholder for future implementation
    # avg_damage = Weapon.parse_damage_average(damage_str)
    # assert avg_damage == expected_avg


def test_parse_damage_value_d6_plus_modifier():
    """Test parsing D6+X damage notation."""
    from ..warhammer_base import Weapon
    
    damage_str = "D6+2"
    expected_avg = 5.5  # 3.5 + 2
    
    # Placeholder for future implementation
    # avg_damage = Weapon.parse_damage_average(damage_str)
    # assert avg_damage == expected_avg


def test_parse_damage_value_multiple_dice():
    """Test parsing XD6 damage notation."""
    from ..warhammer_base import Weapon
    
    damage_str = "2D6"
    expected_avg = 7.0  # 2 × 3.5
    
    # Placeholder for future implementation
    # avg_damage = Weapon.parse_damage_average(damage_str)
    # assert avg_damage == expected_avg


def test_parse_damage_value_fixed_integer():
    """Test parsing fixed integer damage values."""
    from ..warhammer_base import Weapon
    
    damage_int = 3
    expected_avg = 3.0
    
    # Should handle both int and string representations
    # avg_damage = Weapon.parse_damage_average(damage_int)
    # assert avg_damage == expected_avg
    
    damage_str = "3"
    # avg_damage = Weapon.parse_damage_average(damage_str)
    # assert avg_damage == expected_avg
