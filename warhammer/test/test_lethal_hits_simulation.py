"""Tests for Lethal Hits keyword implementation in simulation."""

import pytest
from ..warhammer import Model, Unit
from ..warhammer_base import RangedWeapon


def test_simulation_with_lethal_hits_auto_wounds_on_critical_hits():
    """Test that weapons with Lethal Hits auto-wound on unmodified 6s to hit."""
    # Create attacker with Lethal Hits weapon
    # Gauss flayer: BS 4+, S4, AP0, D1, Lethal Hits
    gauss_flayer = RangedWeapon(
        name="Gauss flayer",
        range=24,
        attacks=1,
        ballistic_skill=4,
        strength=4,
        armour_penetration=0,
        damage=1,
        keywords=["Lethal Hits", "Rapid Fire 1"]
    )
    
    attacker = Model(
        name="Necron Warrior",
        movement=5,
        toughness=4,
        save=4,
        wounds=1,
        leadership=7,
        objective_control=2,
        invulnerable_save=None,
        ranged_weapons={"Gauss flayer": gauss_flayer},
        melee_weapons={}
    )
    
    # Create defender - high toughness so normal wounds are rare
    # T5 means S4 needs 5+ to wound normally (only 1/3 chance)
    defender = Model(
        name="Terminator",
        movement=5,
        toughness=5,
        save=2,
        wounds=3,
        leadership=6,
        objective_control=1,
        invulnerable_save=4,
        ranged_weapons={},
        melee_weapons={}
    )
    
    attacker_unit = Unit(models=[attacker for _ in range(10)], name="Necron Warriors")
    defender_unit = Unit(models=[defender for _ in range(5)], name="Terminators")
    
    # Run simulation many times to get statistical results
    num_simulations = 10000
    total_hits = 0
    total_wounds = 0
    total_attacks = 0
    critical_hits = 0  # Count how many 6s were rolled
    
    for _ in range(num_simulations):
        result = attacker_unit.shoot_at_simulation(defender_unit)
        total_attacks += len(result["hit_rolls"])
        total_hits += len(result["successful_hits"])
        total_wounds += len(result["successful_wounds"])
        
        # Count critical hits (6s in hit_rolls)
        for i, roll in enumerate(result["hit_rolls"]):
            if roll == 6:
                critical_hits += 1
    
    # Calculate rates
    simulated_hit_rate = total_hits / total_attacks
    simulated_wound_rate = total_wounds / total_attacks  # wounds per attack, not per hit
    
    # Expected probabilities with Lethal Hits
    # BS 4+ means hit on 4, 5, 6 = 3/6 = 1/2
    expected_hit_rate = 1/2
    
    # With Lethal Hits:
    # - Critical hits (6s): 1/6 of attacks → auto-wound
    # - Normal hits (4s and 5s): 2/6 of attacks → wound on 5+ (2/6) = 4/36
    # Total wound rate: 1/6 + 4/36 = 6/36 + 4/36 = 10/36 = 5/18
    expected_wound_rate_per_attack = 5/18
    
    # Assertions with tolerance for simulation variance
    assert abs(simulated_hit_rate - expected_hit_rate) < 0.01, (
        f"Hit rate {simulated_hit_rate:.4f} should be close to {expected_hit_rate:.4f}"
    )
    
    assert abs(simulated_wound_rate - expected_wound_rate_per_attack) < 0.01, (
        f"Wound rate {simulated_wound_rate:.4f} should be close to {expected_wound_rate_per_attack:.4f} with Lethal Hits"
    )
    
    # Verify that approximately 1/6 of attacks were critical hits
    critical_hit_rate = critical_hits / total_attacks
    expected_critical_rate = 1/6
    assert abs(critical_hit_rate - expected_critical_rate) < 0.01, (
        f"Critical hit rate {critical_hit_rate:.4f} should be close to {expected_critical_rate:.4f}"
    )


def test_simulation_without_lethal_hits_uses_normal_wound_rolls():
    """Test that weapons without Lethal Hits use normal wound rolling mechanics."""
    # Create attacker without Lethal Hits
    bolter = RangedWeapon(
        name="Bolter",
        range=24,
        attacks=2,
        ballistic_skill=3,
        strength=4,
        armour_penetration=0,
        damage=1,
        keywords=["Rapid Fire 1"]
    )
    
    attacker = Model(
        name="Space Marine",
        movement=6,
        toughness=4,
        save=3,
        wounds=2,
        leadership=6,
        objective_control=2,
        invulnerable_save=None,
        ranged_weapons={"Bolter": bolter},
        melee_weapons={}
    )
    
    # Create defender with same toughness as attacker strength
    # T4 vs S4 = 4+ to wound = 1/2
    defender = Model(
        name="Necron Warrior",
        movement=5,
        toughness=4,
        save=4,
        wounds=1,
        leadership=7,
        objective_control=2,
        invulnerable_save=None,
        ranged_weapons={},
        melee_weapons={}
    )
    
    attacker_unit = Unit(models=[attacker for _ in range(5)], name="Tactical Squad")
    defender_unit = Unit(models=[defender for _ in range(10)], name="Necron Warriors")
    
    # Run simulation many times
    num_simulations = 10000
    total_hits = 0
    total_wounds = 0
    total_attacks = 0
    
    for _ in range(num_simulations):
        result = attacker_unit.shoot_at_simulation(defender_unit)
        total_attacks += len(result["hit_rolls"])
        total_hits += len(result["successful_hits"])
        total_wounds += len(result["successful_wounds"])
    
    # Calculate rates
    simulated_hit_rate = total_hits / total_attacks
    simulated_wound_rate = total_wounds / total_hits  # wounds per successful hit
    
    # Expected probabilities without Lethal Hits
    # BS 3+ means hit on 3, 4, 5, 6 = 4/6 = 2/3
    expected_hit_rate = 2/3
    
    # S4 vs T4 = 4+ to wound = 3/6 = 1/2
    expected_wound_rate_per_hit = 1/2
    
    # Assertions
    assert abs(simulated_hit_rate - expected_hit_rate) < 0.01, (
        f"Hit rate {simulated_hit_rate:.4f} should be close to {expected_hit_rate:.4f}"
    )
    
    assert abs(simulated_wound_rate - expected_wound_rate_per_hit) < 0.01, (
        f"Wound rate per hit {simulated_wound_rate:.4f} should be close to {expected_wound_rate_per_hit:.4f}"
    )


def test_simulation_lethal_hits_only_on_unmodified_6s():
    """Test that Lethal Hits only triggers on unmodified 6s, not modified hits."""
    # This test verifies the critical hit is specifically roll == 6
    # Not just any successful hit
    
    # Create attacker with Lethal Hits and good BS
    # BS 2+ means almost everything hits, but only 6s should auto-wound
    lethal_weapon = RangedWeapon(
        name="Lethal Weapon",
        range=24,
        attacks=1,
        ballistic_skill=2,
        strength=3,
        armour_penetration=0,
        damage=1,
        keywords=["Lethal Hits"]
    )
    
    attacker = Model(
        name="Elite Shooter",
        movement=6,
        toughness=4,
        save=3,
        wounds=2,
        leadership=6,
        objective_control=2,
        invulnerable_save=None,
        ranged_weapons={"Lethal Weapon": lethal_weapon},
        melee_weapons={}
    )
    
    # High toughness defender - S3 vs T6 needs 6+ to wound (only 1/6)
    # So without Lethal Hits, wounds would be very rare
    defender = Model(
        name="Tough Target",
        movement=5,
        toughness=6,
        save=2,
        wounds=5,
        leadership=6,
        objective_control=1,
        invulnerable_save=None,
        ranged_weapons={},
        melee_weapons={}
    )
    
    attacker_unit = Unit(models=[attacker for _ in range(10)], name="Elite Shooters")
    defender_unit = Unit(models=[defender for _ in range(5)], name="Tough Targets")
    
    # Run simulation
    num_simulations = 10000
    total_attacks = 0
    total_wounds = 0
    sixes_rolled = 0
    
    for _ in range(num_simulations):
        result = attacker_unit.shoot_at_simulation(defender_unit)
        total_attacks += len(result["hit_rolls"])
        total_wounds += len(result["successful_wounds"])
        
        # Count how many 6s were rolled
        sixes_rolled += sum(1 for roll in result["hit_rolls"] if roll == 6)
    
    # Expected: With Lethal Hits
    # - BS 2+ means hit on 2,3,4,5,6 = 5/6
    # - Critical hits (6s): 1/6 → auto-wound
    # - Normal hits (2,3,4,5): 4/6 → wound on 6+ (1/6) = 4/36
    # Total wound rate: 1/6 + 4/36 = 6/36 + 4/36 = 10/36 = 5/18
    expected_wound_rate = 5/18
    simulated_wound_rate = total_wounds / total_attacks
    
    assert abs(simulated_wound_rate - expected_wound_rate) < 0.01, (
        f"Wound rate {simulated_wound_rate:.4f} should match {expected_wound_rate:.4f}"
    )
    
    # Verify approximately 1/6 of attacks were 6s
    six_rate = sixes_rolled / total_attacks
    assert abs(six_rate - 1/6) < 0.01, (
        f"Rate of 6s rolled {six_rate:.4f} should be close to {1/6:.4f}"
    )
