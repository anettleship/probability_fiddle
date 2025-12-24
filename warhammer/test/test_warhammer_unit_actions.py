from pathlib import Path

import pytest

from ..load_unit_data_from_roster import LoadUnitDataFromRoster
from ..warhammer import Unit
from ..warhammer_actions import MeleeAttack
from ..warhammer_actions_orchestrators import AttackOrchestrator
from .conftest import SIMULATION_HIT_WOUND_TOLERANCE, SIMULATION_DAMAGE_TOLERANCE


def test_unit_can_shoot_single_weapon_type_at_target(
    terminator_with_storm_bolter, necron_warrior_unit
):
    # Single terminator model wrapped in unit shoots at necron warrior unit
    # Storm Bolter: 2 attacks, BS 3+, S4, AP0, D1
    # Expected: attacks × P(hit) × P(wound) × P(fail_save) × damage
    # = 2 × (2/3) × (1/2) × (1/2) × 1 = 1/3

    single_terminator_unit = Unit(
        models=[terminator_with_storm_bolter], name="Single Terminator"
    )

    results = single_terminator_unit.shoot_at_return_probability(necron_warrior_unit)

    assert len(results.weapon_results) == 1
    assert results.weapon_results[0].weapon_name == "Storm Bolter"
    assert abs(results.total_expected_damage - (1 / 3)) < 0.001


def test_unit_ranged_attacked_probabilities_match_expected(
    necron_warrior_unit, terminator_unit
):
    # TODO NEXT STEP Check that this test is actually True!

    # Terminator unit composition:
    # - 1 Sergeant with Storm Bolter (2 attacks, S4, AP0, D1)
    # - 3 Terminators with Storm Bolters (2 attacks each = 6 total, S4, AP0, D1)
    # - 1 Terminator with Heavy Flamer (D6 attacks = 6 in fixture, S5, AP-1, D1, Auto-hit, Ignores Cover)
    #
    # Expected shooting order (most powerful first):
    # 1. Heavy Flamer: 6 attacks (D6), S5, AP-1, D1
    # 2. Storm Bolters: 8 attacks total (4 models × 2), S4, AP0, D1
    #
    # Expected damage calculation per weapon accounts for number of attacks:
    # expected_damage = attacks × P(hit) × P(wound) × P(fail_save) × damage

    # Execute unit ranged attack
    results = terminator_unit.shoot_at_return_probability(necron_warrior_unit)

    # Verify results structure
    assert hasattr(results, "weapon_results"), "Results should have weapon_results"
    assert len(results.weapon_results) == 2, "Should have 2 weapon types fired"

    # Heavy Flamer should be first (higher strength, better AP)
    heavy_flamer_result = results.weapon_results[0]
    assert heavy_flamer_result.weapon_name == "Heavy Flamer"
    assert heavy_flamer_result.attacks == 6
    assert heavy_flamer_result.expected_hits > 0
    assert heavy_flamer_result.expected_wounds > 0
    assert heavy_flamer_result.expected_damage > 0

    # Storm Bolters should be second
    storm_bolter_result = results.weapon_results[1]
    assert storm_bolter_result.weapon_name == "Storm Bolter"
    assert storm_bolter_result.attacks == 8  # 4 models with 2 attacks each
    assert storm_bolter_result.expected_hits > 0
    assert storm_bolter_result.expected_wounds > 0
    assert storm_bolter_result.expected_damage > 0

    # Verify total expected damage
    total_expected_damage = sum(wr.expected_damage for wr in results.weapon_results)
    assert total_expected_damage > 0
    assert hasattr(results, "total_expected_damage")
    assert results.total_expected_damage == total_expected_damage


@pytest.mark.parametrize(
    "simulation_method",
    [
        "shoot_at_simulation",
        "melee_attack_simulation",
    ],
)
def test_unit_simulation_returns_dict_with_simulation_results(
    space_marine, necron_warrior, simulation_method
):
    """Test that simulation methods return a dictionary with dice roll outcomes."""
    attacker_models = [space_marine for _ in range(5)]
    attacker_unit = Unit(models=attacker_models, name="Tactical Squad")
    
    defender_models = [necron_warrior for _ in range(10)]
    defender_unit = Unit(models=defender_models, name="Necron Warriors")
    
    # Call the appropriate simulation method
    result = getattr(attacker_unit, simulation_method)(defender_unit)
    
    # Verify result is a dictionary
    assert isinstance(result, dict), f"{simulation_method} should return a dictionary"
    
    # Verify required keys exist
    required_keys = {
        "hit_rolls",
        "successful_hits", 
        "wound_rolls",
        "successful_wounds",
        "save_rolls",
        "successful_damage",
        "damage_to_unit"
    }
    assert set(result.keys()) == required_keys, (
        f"Result should contain keys: {required_keys}"
    )
    
    # Verify all values are lists
    for key, value in result.items():
        assert isinstance(value, list), f"{key} should be a list"
    
    # Verify all hit_rolls are integers (die roll results)
    assert all(isinstance(roll, int) for roll in result["hit_rolls"]), (
        "All hit_rolls should be integers"
    )
    
    # Verify successful_hits is a subset of hit_rolls (by index or tracking)
    assert len(result["successful_hits"]) <= len(result["hit_rolls"]), (
        "successful_hits cannot exceed total hit_rolls"
    )
    
    # Verify wound_rolls length matches successful_hits length
    assert len(result["wound_rolls"]) == len(result["successful_hits"]), (
        "wound_rolls should only be made for successful hits"
    )
    
    # Verify save_rolls length matches successful_wounds length  
    assert len(result["save_rolls"]) == len(result["successful_wounds"]), (
        "save_rolls should only be made for successful wounds"
    )
    
    # Verify damage_to_unit contains integers
    assert all(isinstance(dmg, int) for dmg in result["damage_to_unit"]), (
        "All damage_to_unit values should be integers"
    )
    
    # Verify successful_damage length matches damage_to_unit length
    assert len(result["successful_damage"]) == len(result["damage_to_unit"]), (
        "successful_damage should match damage_to_unit length"
    )


@pytest.mark.parametrize(
    "simulation_method",
    [
        "melee_attack_simulation",
    ],
)
def test_unit_simulation_converges_to_probability(
    necron_warrior, terminator_unit, simulation_method
):
    """Test that simulation averages converge to expected probabilities over many repetitions."""
    # Create attacking unit: 10 Necron Warriors
    attacker_models = [necron_warrior for _ in range(10)]
    attacker_unit = Unit(models=attacker_models, name="Necron Warriors")
    
    # Defender unit: 5 Terminators (from fixture)
    defender_unit = terminator_unit
    
    # Run simulation 1000 times
    num_simulations = 1000
    total_hits = 0
    total_wounds = 0
    total_damage = 0
    total_attacks = 0
    
    for _ in range(num_simulations):
        result = getattr(attacker_unit, simulation_method)(defender_unit)
        total_attacks += len(result["hit_rolls"])
        total_hits += len(result["successful_hits"])
        total_wounds += len(result["successful_wounds"])
        total_damage += sum(result["damage_to_unit"])
    
    # Calculate simulation averages
    avg_hit_rate = total_hits / total_attacks if total_attacks > 0 else 0
    avg_wound_rate = total_wounds / total_hits if total_hits > 0 else 0
    avg_damage_per_simulation = total_damage / num_simulations
    
    # Use first model from each unit as representative
    attacker_model = attacker_unit.all_models()[0]
    defender_model = defender_unit.all_models()[0]
    
    # Get the close combat weapon from necron warrior
    weapon = attacker_model.melee_weapons["Close combat weapon"]
    
    attack = MeleeAttack(
        attacker=attacker_model,
        target=defender_model,
        weapon=weapon,
    )
    
    expected_hit_probability = attack.probability_to_hit()
    expected_wound_probability = attack.probability_to_wound()
    expected_damage_probability = attack.probability_to_damage()
    expected_damage_per_attack = expected_damage_probability * weapon.damage
    
    # Calculate expected damage per simulation
    # 10 warriors × 1 attack each = 10 attacks per simulation
    attacks_per_simulation = 10 * weapon.attacks
    expected_damage_per_simulation = attacks_per_simulation * expected_damage_per_attack
    
    # Assert simulation converges to expected probabilities (within reasonable tolerance)
    # Hit/wound rates should be very close (5.5% tolerance)
    # Damage has more variance due to cascading probabilities (16.5% tolerance)
    
    assert abs(avg_hit_rate - expected_hit_probability) < SIMULATION_HIT_WOUND_TOLERANCE, (
        f"Hit rate {avg_hit_rate:.3f} should be close to expected {expected_hit_probability:.3f}"
    )
    
    assert abs(avg_wound_rate - expected_wound_probability) < SIMULATION_HIT_WOUND_TOLERANCE, (
        f"Wound rate {avg_wound_rate:.3f} should be close to expected {expected_wound_probability:.3f}"
    )
    
    assert abs(avg_damage_per_simulation - expected_damage_per_simulation) / expected_damage_per_simulation < SIMULATION_DAMAGE_TOLERANCE, (
        f"Average damage {avg_damage_per_simulation:.3f} should be close to expected {expected_damage_per_simulation:.3f}"
    )


def test_attack_orchestrator_runs_melee_simulation_and_returns_summary_with_fractions(
    necron_warrior, terminator_unit
):
    """Test that AttackOrchestrator runs simulation and returns structured results with fraction conversion."""
    # Load units from roster JSON files
    necron_roster_path = (
        Path(__file__).parent.parent / "test_data" / "Single_Necron_Warrior_Unit.json"
    )
    terminator_roster_path = (
        Path(__file__).parent.parent / "test_data" / "Single_Terminator_Squad_Roster.json"
    )
    
    necron_loader = LoadUnitDataFromRoster(datasource=necron_roster_path)
    terminator_loader = LoadUnitDataFromRoster(datasource=terminator_roster_path)
    
    # Get units from loaders
    attacker_unit = necron_loader.get_unit("Necron Warriors")
    defender_unit = terminator_loader.get_unit("Terminator Squad")
    
    # Create orchestrator with 1000 simulations
    orchestrator = AttackOrchestrator(
        attacker_unit=attacker_unit,
        target_unit=defender_unit,
        num_simulations=1000
    )
    
    # Run the simulation
    result = orchestrator.run()
    
    # Verify result structure
    assert isinstance(result, dict), "Result should be a dictionary"
    assert "summary" in result, "Result should contain 'summary' key"
    assert "expected_success_rate" in result, "Result should contain 'expected_success_rate' key"
    assert "detail" in result, "Result should contain 'detail' key"
    
    # Verify summary contains simulation outcome
    summary = result["summary"]
    assert isinstance(summary, dict), "Summary should be a dictionary"
    assert "total_attacks" in summary
    assert "total_hits" in summary
    assert "total_wounds" in summary
    assert "total_damage" in summary
    assert "avg_hit_rate" in summary
    assert "avg_wound_rate" in summary
    assert "avg_damage_per_simulation" in summary
    
    # Verify expected_success_rate contains fractions
    expected_rate = result["expected_success_rate"]
    assert isinstance(expected_rate, dict), "Expected success rate should be a dictionary"
    assert "hit_probability" in expected_rate
    assert "wound_probability" in expected_rate
    assert "damage_probability" in expected_rate
    
    # Each probability should be a tuple (numerator, denominator)
    hit_prob = expected_rate["hit_probability"]
    assert isinstance(hit_prob, tuple), "Hit probability should be a tuple"
    assert len(hit_prob) == 2, "Hit probability tuple should have 2 elements"
    assert isinstance(hit_prob[0], int), "Numerator should be an int"
    assert isinstance(hit_prob[1], int), "Denominator should be an int"
    
    wound_prob = expected_rate["wound_probability"]
    assert isinstance(wound_prob, tuple), "Wound probability should be a tuple"
    assert len(wound_prob) == 2, "Wound probability tuple should have 2 elements"
    
    damage_prob = expected_rate["damage_probability"]
    assert isinstance(damage_prob, tuple), "Damage probability should be a tuple"
    assert len(damage_prob) == 2, "Damage probability tuple should have 2 elements"
    
    # Verify detail contains breakdown of all steps
    detail = result["detail"]
    assert isinstance(detail, dict), "Detail should be a dictionary"
    assert "hit_rolls" in detail
    assert "successful_hits" in detail
    assert "wound_rolls" in detail
    assert "successful_wounds" in detail
    assert "save_rolls" in detail
    assert "successful_damage" in detail
    assert "damage_to_unit" in detail
    
    # Verify detail contains lists (aggregated across all simulations)
    assert isinstance(detail["hit_rolls"], list), "hit_rolls should be a list"
    assert isinstance(detail["successful_hits"], list), "successful_hits should be a list"
    assert isinstance(detail["wound_rolls"], list), "wound_rolls should be a list"
    assert isinstance(detail["successful_wounds"], list), "successful_wounds should be a list"
    assert isinstance(detail["save_rolls"], list), "save_rolls should be a list"
    assert isinstance(detail["successful_damage"], list), "successful_damage should be a list"
    assert isinstance(detail["damage_to_unit"], list), "damage_to_unit should be a list"
    
    # Verify simulation ran correct number of times (1000 simulations × 10 attacks each = 10000 total attacks)
    assert len(detail["hit_rolls"]) == 10000, "Should have 10000 total hit rolls (1000 sims × 10 attacks)"

