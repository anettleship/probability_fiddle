from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable, Type

from .warhammer import Unit
from .warhammer_actions import Attack, MeleeAttack, RangedAttack
from .probability_objects import ProbabilityConverter


class AttackOrchestrator(ABC):
    """Base class for orchestrating attack simulations and probability calculations.
    
    This abstract class defines the common interface for running combat simulations
    and calculating expected probabilities for attacks from one unit against another.
    
    Attributes:
        attacker_unit: The attacking unit
        target_unit: The defending unit
        num_simulations: Number of simulation runs to perform
    """
    
    def __init__(
        self,
        attacker_unit: Unit,
        target_unit: Unit,
        num_simulations: int = 1,
    ):
        self.attacker_unit: Unit = attacker_unit
        self.target_unit: Unit = target_unit
        self.num_simulations: int = num_simulations
    
    @property
    @abstractmethod
    def attack_class(self) -> Type[Attack]:
        """The attack class type (MeleeAttack or RangedAttack)."""
        pass
    
    @property
    @abstractmethod
    def weapon_type(self) -> str:
        """The weapon attribute name ('ranged_weapons' or 'melee_weapons')."""
        pass
    
    @abstractmethod
    def simulate(self, target_unit: Unit) -> dict:
        """Run a single simulation against the target unit."""
        pass
    
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
            sim_result = self.simulate(self.target_unit)
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
        
        # Calculate weighted probabilities across all weapons in the unit
        weighted_probs = self.calculate_weighted_weapon_probabilities()
        
        expected_hit_probability = weighted_probs["weighted_hit_probability"]
        expected_wound_probability = weighted_probs["weighted_wound_probability"]
        expected_damage_probability = weighted_probs["weighted_damage_probability"]
        
        # Calculate expected damage per unit attack
        # This requires iterating through all models and weapons to get weighted average damage
        total_weighted_damage = 0.0
        
        defender_model = self.target_unit.all_models()[0]
        for model in self.attacker_unit.all_models():
            weapons_dict = getattr(model, self.weapon_type)
            for weapon_name, weapon in weapons_dict.items():
                attack = self.attack_class(
                    attacker=model,
                    target=defender_model,
                    weapon=weapon,
                )
                damage_prob = attack.probability_to_damage()
                avg_damage = weapon.get_average_damage()
                num_attacks = weapon.get_average_attacks()
                
                total_weighted_damage += num_attacks * damage_prob * avg_damage
        
        expected_damage_per_unit_attack = total_weighted_damage
        
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
    
    def calculate_weighted_weapon_probabilities(self) -> dict:
        """Calculate weighted average probabilities across all weapons in the unit.
        
        For units with multiple weapon types (e.g., Storm Bolters and Heavy Flamers),
        this calculates the weighted average of hit/wound/damage probabilities based
        on the number of attacks each weapon contributes.
        
        Returns:
            dict with keys:
                - weighted_hit_probability: float
                - weighted_wound_probability: float
                - weighted_damage_probability: float
                - total_attacks: int
        """
        defender_model = self.target_unit.all_models()[0]
        
        total_attacks = 0
        weighted_hits = 0.0
        weighted_wounds = 0.0
        weighted_damage = 0.0
        
        # Iterate through all models in the attacking unit
        for model in self.attacker_unit.all_models():
            weapons_dict = getattr(model, self.weapon_type)
            
            # Iterate through all weapons on this model
            for weapon_name, weapon in weapons_dict.items():
                # Get number of attacks for this weapon (use average for variable attacks)
                num_attacks = weapon.get_average_attacks()
                
                # Create attack instance to calculate probabilities
                attack = self.attack_class(
                    attacker=model,
                    target=defender_model,
                    weapon=weapon,
                )
                
                hit_prob = attack.probability_to_hit()
                wound_prob = attack.probability_to_wound()
                damage_prob = attack.probability_to_damage()
                
                # Weight by number of attacks
                weighted_hits += num_attacks * hit_prob
                weighted_wounds += num_attacks * wound_prob
                weighted_damage += num_attacks * damage_prob
                total_attacks += num_attacks
        
        # Calculate weighted averages
        if total_attacks > 0:
            weighted_hit_avg = weighted_hits / total_attacks
            weighted_wound_avg = weighted_wounds / total_attacks
            weighted_damage_avg = weighted_damage / total_attacks
        else:
            weighted_hit_avg = 0.0
            weighted_wound_avg = 0.0
            weighted_damage_avg = 0.0
        
        return {
            "weighted_hit_probability": weighted_hit_avg,
            "weighted_wound_probability": weighted_wound_avg,
            "weighted_damage_probability": weighted_damage_avg,
            "total_attacks": total_attacks,
        }


class RangedAttackOrchestrator(AttackOrchestrator):
    """Orchestrates ranged attack simulations and probability calculations."""
    
    @property
    def attack_class(self) -> Type[Attack]:
        return RangedAttack
    
    @property
    def weapon_type(self) -> str:
        return "ranged_weapons"
    
    def simulate(self, target_unit: Unit) -> dict:
        """Run a single ranged attack simulation."""
        return self.attacker_unit.shoot_at_simulation(target_unit)


class MeleeAttackOrchestrator(AttackOrchestrator):
    """Orchestrates melee attack simulations and probability calculations."""
    
    @property
    def attack_class(self) -> Type[Attack]:
        return MeleeAttack
    
    @property
    def weapon_type(self) -> str:
        return "melee_weapons"
    
    def simulate(self, target_unit: Unit) -> dict:
        """Run a single melee attack simulation."""
        return self.attacker_unit.melee_attack_simulation(target_unit)
