from __future__ import annotations

from typing import Callable

from .warhammer import Unit
from .warhammer_actions import MeleeAttack, RangedAttack
from .probability_objects import ProbabilityConverter


class AttackOrchestrator:
    def __init__(
        self,
        attacker_unit: Unit,
        target_unit: Unit,
        num_simulations: int = 1,
        attack_class: type = MeleeAttack
    ):
        self.attacker_unit = attacker_unit
        self.target_unit = target_unit
        self.num_simulations = num_simulations
        self.attack_class = attack_class  # MeleeAttack or RangedAttack class
        
        # Get simulation method and weapon type from the attack class itself
        simulation_method_name = attack_class.get_simulation_method_name()
        self.simulation_method = getattr(attacker_unit, simulation_method_name)
        self.weapon_type = attack_class.get_weapon_type_attribute()
    
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
        
        # Track damage per simulation for variance calculation
        damage_per_simulation = []
        
        for _ in range(self.num_simulations):
            sim_result = self.simulation_method(self.target_unit)
            all_hit_rolls.extend(sim_result["hit_rolls"])
            all_successful_hits.extend(sim_result["successful_hits"])
            all_wound_rolls.extend(sim_result["wound_rolls"])
            all_successful_wounds.extend(sim_result["successful_wounds"])
            all_save_rolls.extend(sim_result["save_rolls"])
            all_successful_damage.extend(sim_result["successful_damage"])
            all_damage_to_unit.extend(sim_result["damage_to_unit"])
            
            # Track damage for this simulation
            sim_damage = sum(sim_result["damage_to_unit"])
            damage_per_simulation.append(sim_damage)
        
        # Calculate summary statistics
        total_attacks = len(all_hit_rolls)
        total_hits = len(all_successful_hits)
        total_wounds = len(all_successful_wounds)
        total_damage = sum(all_damage_to_unit)
        
        avg_hit_rate = total_hits / total_attacks if total_attacks > 0 else 0
        avg_wound_rate = total_wounds / total_hits if total_hits > 0 else 0
        avg_damage_per_simulation = total_damage / self.num_simulations
        
        # Calculate damage variance
        max_damage = max(damage_per_simulation) if damage_per_simulation else 0
        min_damage = min(damage_per_simulation) if damage_per_simulation else 0
        
        # Variance = average of squared differences from mean
        if damage_per_simulation:
            mean_damage = sum(damage_per_simulation) / len(damage_per_simulation)
            variance = sum((d - mean_damage) ** 2 for d in damage_per_simulation) / len(damage_per_simulation)
        else:
            variance = 0
        
        # Calculate expected probabilities using first model as representative
        attacker_model = self.attacker_unit.all_models()[0]
        defender_model = self.target_unit.all_models()[0]
        
        # Get weapon dictionary and first weapon
        weapons_dict = getattr(attacker_model, self.weapon_type)
        weapon = weapons_dict[list(weapons_dict.keys())[0]]
        
        # Create attack instance using the attack class
        attack = self.attack_class(
            attacker=attacker_model,
            target=defender_model,
            weapon=weapon,
        )
        
        expected_hit_probability = attack.probability_to_hit()
        expected_wound_probability = attack.probability_to_wound()
        expected_damage_probability = attack.probability_to_damage()
        
        # Get average damage (handles variable damage like D6)
        average_damage = weapon.get_average_damage()
        expected_damage_per_unit_attack = expected_damage_probability * average_damage * len(self.attacker_unit.all_models())
        
        # Convert probabilities to fractions
        hit_fraction = ProbabilityConverter.float_to_fraction(expected_hit_probability)
        wound_fraction = ProbabilityConverter.float_to_fraction(expected_wound_probability)
        damage_fraction = ProbabilityConverter.float_to_fraction(expected_damage_probability)
        expected_unit_damage_fraction = ProbabilityConverter.float_to_fraction(expected_damage_per_unit_attack)
        
        return {
            "summary": {
                "num_simulations": self.num_simulations,
                "total_attacks": total_attacks,
                "total_hits": total_hits,
                "total_wounds": total_wounds,
                "total_damage": total_damage,
                "avg_hit_rate": avg_hit_rate,
                "avg_wound_rate": avg_wound_rate,
                "avg_damage_per_simulation": avg_damage_per_simulation,
                "max_damage_in_single_simulation": max_damage,
                "min_damage_in_single_simulation": min_damage,
                "damage_variance": variance,
            },
            "expected_success_rate": {
                "hit_probability": hit_fraction,
                "wound_probability": wound_fraction,
                "damage_probability": damage_fraction,
                "expected_damage_per_unit_attack": expected_unit_damage_fraction,
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
