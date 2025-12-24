from __future__ import annotations

from .warhammer_base import MeleeWeapon, Model, RangedWeapon
from .constants import SimulationMethod, WeaponAttribute


class Attack:
    def __init__(self, attacker: Model, target: Model, benefit_of_cover: bool = False):
        self.attacker = attacker
        self.target = target
        self.benefit_of_cover = benefit_of_cover
        self.weapon = None  # To be defined in subclasses

    def probability_to_damage(self) -> float:
        return (
            self.probability_to_hit()
            * self.probability_to_wound()
            * self.probability_to_fail_save()
        )

    def probability_to_hit(self) -> float:
        raise NotImplementedError(
            "Subclasses must implement probability_to_hit method."
        )

    def _calculate_wound_roll_required(self) -> int:
        """Calculate the required wound roll based on weapon strength vs target toughness."""
        strength = self.weapon.strength
        toughness = self.target.toughness

        if strength >= 2 * toughness:
            return 2
        elif strength > toughness:
            return 3
        elif strength == toughness:
            return 4
        elif strength * 2 <= toughness:
            return 6
        else:
            return 5

    def _calculate_wound_probability_with_lethal_hits(self) -> float:
        """Calculate wound probability when weapon has Lethal Hits keyword."""
        # Get hit skill to determine critical vs normal hits
        if hasattr(self.weapon, "ballistic_skill"):
            required_hit_roll = self.weapon.ballistic_skill
        elif hasattr(self.weapon, "weapon_skill"):
            required_hit_roll = self.weapon.weapon_skill
        else:
            required_hit_roll = 0

        # Critical hits: unmodified 6s always auto-wound
        critical_hit_probability = 1 / 6

        # Normal hits: successful hits that aren't 6s (must roll to wound)
        if required_hit_roll == 0:
            # Auto-hit weapon: conceptually still has critical 6s
            normal_hit_probability = 5 / 6
        elif required_hit_roll <= 6:
            # Normal hits = all successful hit rolls except 6
            # e.g., 3+ to hit gives 3,4,5,6 but 6 is critical, so normal = 3,4,5
            total_successful_hits = 7 - required_hit_roll
            normal_hit_probability = (total_successful_hits - 1) / 6
        else:
            normal_hit_probability = 0

        # Calculate wound probability for normal hits
        wound_roll = self._calculate_wound_roll_required()
        normal_wound_probability = (7 - wound_roll) / 6

        # Total wounds = critical hits (auto-wound) + normal hits × wound probability
        return critical_hit_probability + (
            normal_hit_probability * normal_wound_probability
        )

    def probability_to_wound_successful_outcomes(self) -> set[int]:
        if self.weapon is None:
            raise NotImplementedError(
                "Weapon must be defined in subclass to calculate wound probability."
            )

        required_roll = self._calculate_wound_roll_required()
        return set(range(required_roll, 7))  # e.g., for 4+, returns {4, 5, 6}

    def probability_to_wound(self) -> float:
        if self.weapon is None:
            raise NotImplementedError(
                "Weapon must be defined in subclass to calculate wound probability."
            )

        # Check for Lethal Hits keyword
        if hasattr(self.weapon, "keywords") and "Lethal Hits" in self.weapon.keywords:
            return self._calculate_wound_probability_with_lethal_hits()

        # Standard wound calculation (no Lethal Hits)
        successful_outcomes = self.probability_to_wound_successful_outcomes()
        return len(successful_outcomes) / 6

    def _calculate_modified_save(self) -> int:
        """Calculate the modified save value after AP, cover, and invuln."""
        if self.weapon is None:
            raise NotImplementedError(
                "Weapon must be defined in subclass to calculate save probability."
            )

        modified_save = self.target.save - self.weapon.armour_penetration
        if modified_save < 2:
            modified_save = 2  # Minimum save is 2+
        elif modified_save > 6:
            modified_save = 7  # Impossible save

        if self.benefit_of_cover:
            modified_save = self.apply_benefit_of_cover(modified_save)

        if (
            self.target.invulnerable_save is not None
            and self.target.invulnerable_save < modified_save
        ):
            modified_save = self.target.invulnerable_save

        return modified_save

    def probability_to_fail_save_outcomes(self) -> set[int]:
        modified_save = self._calculate_modified_save()
        # Failed save outcomes: e.g., 5+ save fails on 1,2,3,4 => {1, 2, 3, 4}
        if modified_save > 6:
            return {1, 2, 3, 4, 5, 6}  # Impossible save, all rolls fail
        return set(range(1, modified_save))

    def probability_to_fail_save(self) -> float:
        successful_outcomes = self.probability_to_fail_save_outcomes()
        return len(successful_outcomes) / 6

    def apply_benefit_of_cover(self, modified_save: int) -> int:
        return modified_save


class RangedAttack(Attack):
    def __init__(
        self,
        attacker: Model,
        target: Model,
        weapon: RangedWeapon,
        benefit_of_cover: bool = False,
    ):
        super().__init__(attacker, target, benefit_of_cover)
        self.weapon = weapon
    
    @classmethod
    def get_simulation_method_name(cls) -> str:
        """Return the name of the Unit simulation method for this attack type."""
        return SimulationMethod.RANGED.value
    
    @classmethod
    def get_weapon_type_attribute(cls) -> str:
        """Return the name of the Model attribute that stores weapons for this attack type."""
        return WeaponAttribute.RANGED.value

    def probability_to_hit_successful_outcomes(self) -> set[int]:
        required_roll = self.weapon.ballistic_skill
        if required_roll == 0:
            return {1, 2, 3, 4, 5, 6}  # Auto-hit weapon hits on all rolls
        return set(range(required_roll, 7))  # e.g., for 4+, returns {4, 5, 6}

    def probability_to_hit(self) -> float:
        successful_outcomes = self.probability_to_hit_successful_outcomes()
        return len(successful_outcomes) / 6

    def apply_benefit_of_cover(self, modified_save: int) -> int:
        # Check if weapon has "Ignores Cover" keyword
        if hasattr(self.weapon, "keywords") and "Ignores Cover" in self.weapon.keywords:
            return modified_save  # No benefit of cover applied

        if modified_save > 3:
            modified_save -= 1  # Cover lowers save requirement by 1 with a floor of 3+
        return modified_save


class MeleeAttack(Attack):
    def __init__(
        self,
        attacker: Model,
        target: Model,
        weapon: MeleeWeapon,
        benefit_of_cover: bool = False,
    ):
        super().__init__(attacker, target, benefit_of_cover)
        self.weapon = weapon
    
    @classmethod
    def get_simulation_method_name(cls) -> str:
        """Return the name of the Unit simulation method for this attack type."""
        return SimulationMethod.MELEE.value
    
    @classmethod
    def get_weapon_type_attribute(cls) -> str:
        """Return the name of the Model attribute that stores weapons for this attack type."""
        return WeaponAttribute.MELEE.value

    def probability_to_hit_successful_outcomes(self) -> set[int]:
        required_roll = self.weapon.weapon_skill
        return set(range(required_roll, 7))  # e.g., for 3+, returns {3, 4, 5, 6}

    def probability_to_hit(self) -> float:
        successful_outcomes = self.probability_to_hit_successful_outcomes()
        return len(successful_outcomes) / 6

    def apply_benefit_of_cover(self, modified_save: int) -> int:
        # Melee attacks don't benefit from cover
        return modified_save
