from __future__ import annotations

from .warhammer import Unit
from .warhammer_actions import MeleeAttack
from .probability_objects import ProbabilityConverter


class AttackOrchestrator:
    def __init__(
        self,
        attacker_unit: Unit,
        target_unit: Unit,
        num_simulations: int = 1
    ):
        self.attacker_unit = attacker_unit
        self.target_unit = target_unit
        self.num_simulations = num_simulations
    
    def run(self) -> dict:
        """Run simulations and return structured results with summary, expected rates, and detail."""
        # Aggregate results across all simulations
        all_hit_rolls = []
        all_successful_hits = []
        all_wound_rolls = []
        all_successful_wounds = []
        all_save_rolls = []
        all_successful_damage = []
        all_damage_to_unit = []
        
        for _ in range(self.num_simulations):
            sim_result = self.attacker_unit.melee_attack_simulation(self.target_unit)
            all_hit_rolls.extend(sim_result["hit_rolls"])
            all_successful_hits.extend(sim_result["successful_hits"])
            all_wound_rolls.extend(sim_result["wound_rolls"])
            all_successful_wounds.extend(sim_result["successful_wounds"])
            all_save_rolls.extend(sim_result["save_rolls"])
            all_successful_damage.extend(sim_result["successful_damage"])
            all_damage_to_unit.extend(sim_result["damage_to_unit"])
        
        # Calculate summary statistics
        total_attacks = len(all_hit_rolls)
        total_hits = len(all_successful_hits)
        total_wounds = len(all_successful_wounds)
        total_damage = sum(all_damage_to_unit)
        
        avg_hit_rate = total_hits / total_attacks if total_attacks > 0 else 0
        avg_wound_rate = total_wounds / total_hits if total_hits > 0 else 0
        avg_damage_per_simulation = total_damage / self.num_simulations
        
        # Calculate expected probabilities using first model as representative
        attacker_model = self.attacker_unit.all_models()[0]
        defender_model = self.target_unit.all_models()[0]
        weapon = attacker_model.melee_weapons[list(attacker_model.melee_weapons.keys())[0]]
        
        attack = MeleeAttack(
            attacker=attacker_model,
            target=defender_model,
            weapon=weapon,
        )
        
        expected_hit_probability = attack.probability_to_hit()
        expected_wound_probability = attack.probability_to_wound()
        expected_damage_probability = attack.probability_to_damage()
        
        # Convert probabilities to fractions
        hit_fraction = ProbabilityConverter.float_to_fraction(expected_hit_probability)
        wound_fraction = ProbabilityConverter.float_to_fraction(expected_wound_probability)
        damage_fraction = ProbabilityConverter.float_to_fraction(expected_damage_probability)
        
        return {
            "summary": {
                "total_attacks": total_attacks,
                "total_hits": total_hits,
                "total_wounds": total_wounds,
                "total_damage": total_damage,
                "avg_hit_rate": avg_hit_rate,
                "avg_wound_rate": avg_wound_rate,
                "avg_damage_per_simulation": avg_damage_per_simulation,
            },
            "expected_success_rate": {
                "hit_probability": hit_fraction,
                "wound_probability": wound_fraction,
                "damage_probability": damage_fraction,
            },
            "detail": {
                "hit_rolls": all_hit_rolls,
                "successful_hits": all_successful_hits,
                "wound_rolls": all_wound_rolls,
                "successful_wounds": all_successful_wounds,
                "save_rolls": all_save_rolls,
                "successful_damage": all_successful_damage,
                "damage_to_unit": all_damage_to_unit,
            },
        }
