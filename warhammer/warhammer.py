from .warhammer_actions import RangedAttack, MeleeAttack
from .warhammer_base import Model


class WeaponResult:
    def __init__(
        self,
        weapon_name,
        attacks,
        expected_hits,
        expected_wounds,
        expected_damage,
    ):
        self.weapon_name = weapon_name
        self.attacks = attacks
        self.expected_hits = expected_hits
        self.expected_wounds = expected_wounds
        self.expected_damage = expected_damage


class ShootingResult:
    def __init__(self, weapon_results):
        self.weapon_results = weapon_results
        self.total_expected_damage = sum(wr.expected_damage for wr in weapon_results)


class Unit:
    def __init__(self, models: list[Model], name: str):
        # Group models by their name (type)
        self.models = {}
        for model in models:
            if model.name not in self.models:
                self.models[model.name] = []
            self.models[model.name].append(model)
        self.name = name

    def model_types(self):
        """Return the set of model type names in this unit."""
        return set(self.models.keys())

    def all_models(self):
        """Return a flat list of all models in the unit."""
        result = []
        for model_list in self.models.values():
            result.extend(model_list)
        return result

    def _calculate_weapon_expected_damage(
        self, weapon, total_attacks, target_model, attacker_model
    ):
        """Calculate expected hits, wounds, and damage for a weapon."""
        attack = RangedAttack(
            attacker=attacker_model,
            target=target_model,
            weapon=weapon,
        )

        hit_probability = attack.probability_to_hit()
        wound_probability = attack.probability_to_wound()
        expected_damage_per_attack = attack.probability_to_damage() * weapon.damage

        expected_hits = total_attacks * hit_probability
        expected_wounds = total_attacks * hit_probability * wound_probability
        expected_damage = total_attacks * expected_damage_per_attack

        return expected_hits, expected_wounds, expected_damage

    def shoot_at_return_probability(self, target_unit):
        """Calculate expected damage from all ranged weapons firing at target unit."""

        # Aggregate weapons across all models
        weapons_by_name = {}
        for model in self.all_models():
            for weapon_name, weapon in model.ranged_weapons.items():
                if weapon_name not in weapons_by_name:
                    weapons_by_name[weapon_name] = {
                        "weapon": weapon,
                        "total_attacks": 0,
                    }
                weapons_by_name[weapon_name]["total_attacks"] += weapon.attacks

        # Sort weapons by power (strength desc, AP desc, damage desc)
        sorted_weapons = sorted(
            weapons_by_name.items(),
            key=lambda item: (
                -item[1]["weapon"].strength,
                item[1]["weapon"].armour_penetration,
                -item[1]["weapon"].damage,
            ),
        )

        # Calculate expected damage for each weapon
        weapon_results = []
        target_model = target_unit.all_models()[0]
        attacker_model = self.all_models()[0]

        for weapon_name, weapon_data in sorted_weapons:
            weapon = weapon_data["weapon"]
            total_attacks = weapon_data["total_attacks"]

            expected_hits, expected_wounds, expected_damage = (
                self._calculate_weapon_expected_damage(
                    weapon, total_attacks, target_model, attacker_model
                )
            )

            weapon_result = WeaponResult(
                weapon_name=weapon_name,
                attacks=total_attacks,
                expected_hits=expected_hits,
                expected_wounds=expected_wounds,
                expected_damage=expected_damage,
            )
            weapon_results.append(weapon_result)

        return ShootingResult(weapon_results)

    def shoot_at_simulation(self, target_unit):
        """Simulate shooting by rolling dice for each attack."""
        from .probability_objects import DiceRoll
        
        dice = DiceRoll(sides=6)
        
        # Initialize result dictionary
        result = {
            "hit_rolls": [],
            "successful_hits": [],
            "wound_rolls": [],
            "successful_wounds": [],
            "save_rolls": [],
            "successful_damage": [],
            "damage_to_unit": []
        }
        
        # Aggregate weapons across all models
        target_model = target_unit.all_models()[0]
        attacker_model = self.all_models()[0]
        
        for model in self.all_models():
            for weapon_name, weapon in model.ranged_weapons.items():
                # Create attack for this weapon
                attack = RangedAttack(
                    attacker=attacker_model,
                    target=target_model,
                    weapon=weapon,
                )
                
                # Get successful outcome sets
                hit_outcomes = attack.probability_to_hit_successful_outcomes()
                wound_outcomes = attack.probability_to_wound_successful_outcomes()
                fail_save_outcomes = attack.probability_to_fail_save_outcomes()
                
                # Roll to hit for each attack
                for _ in range(weapon.attacks):
                    hit_roll = dice.roll()
                    result["hit_rolls"].append(hit_roll)
                    
                    # Check if hit was successful
                    if hit_roll in hit_outcomes:
                        result["successful_hits"].append(hit_roll)
                        
                        # Roll to wound
                        wound_roll = dice.roll()
                        result["wound_rolls"].append(wound_roll)
                        
                        # Check if wound was successful
                        if wound_roll in wound_outcomes:
                            result["successful_wounds"].append(wound_roll)
                            
                            # Roll save
                            save_roll = dice.roll()
                            result["save_rolls"].append(save_roll)
                            
                            # Check if save failed (damage dealt)
                            if save_roll in fail_save_outcomes:
                                result["successful_damage"].append(save_roll)
                                result["damage_to_unit"].append(weapon.damage)
        
        return result

    def melee_attack_simulation(self, target_unit):
        """Simulate melee attacks by rolling dice for each attack."""
        from .probability_objects import DiceRoll
        
        dice = DiceRoll(sides=6)
        
        # Initialize result dictionary
        result = {
            "hit_rolls": [],
            "successful_hits": [],
            "wound_rolls": [],
            "successful_wounds": [],
            "save_rolls": [],
            "successful_damage": [],
            "damage_to_unit": []
        }
        
        # Aggregate weapons across all models
        target_model = target_unit.all_models()[0]
        attacker_model = self.all_models()[0]
        
        for model in self.all_models():
            for weapon_name, weapon in model.melee_weapons.items():
                # Create attack for this weapon
                attack = MeleeAttack(
                    attacker=attacker_model,
                    target=target_model,
                    weapon=weapon,
                )
                
                # Get successful outcome sets
                hit_outcomes = attack.probability_to_hit_successful_outcomes()
                wound_outcomes = attack.probability_to_wound_successful_outcomes()
                fail_save_outcomes = attack.probability_to_fail_save_outcomes()
                
                # Roll to hit for each attack
                for _ in range(weapon.attacks):
                    hit_roll = dice.roll()
                    result["hit_rolls"].append(hit_roll)
                    
                    # Check if hit was successful
                    if hit_roll in hit_outcomes:
                        result["successful_hits"].append(hit_roll)
                        
                        # Roll to wound
                        wound_roll = dice.roll()
                        result["wound_rolls"].append(wound_roll)
                        
                        # Check if wound was successful
                        if wound_roll in wound_outcomes:
                            result["successful_wounds"].append(wound_roll)
                            
                            # Roll save
                            save_roll = dice.roll()
                            result["save_rolls"].append(save_roll)
                            
                            # Check if save failed (damage dealt)
                            if save_roll in fail_save_outcomes:
                                result["successful_damage"].append(save_roll)
                                result["damage_to_unit"].append(weapon.damage)
        
        return result
