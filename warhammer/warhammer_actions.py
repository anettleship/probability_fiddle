from ..warhammer.warhammer import MeleeWeapon, Model, RangedWeapon


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

    def probability_to_wound(self):
        if self.weapon is None:
            raise NotImplementedError(
                "Weapon must be defined in subclass to calculate wound probability."
            )

        strength = self.weapon.strength
        toughness = self.target.toughness

        # Determine required roll based on Strength vs Toughness
        if strength >= 2 * toughness:
            required_roll = 2  # 2+ to wound
        elif strength > toughness:
            required_roll = 3  # 3+ to wound
        elif strength == toughness:
            required_roll = 4  # 4+ to wound
        elif strength * 2 <= toughness:
            required_roll = 6  # 6+ to wound
        else:  # strength < toughness (but not half or less)
            required_roll = 5  # 5+ to wound

        successful_outcomes = 7 - required_roll
        return successful_outcomes / 6

    def probability_to_fail_save(self) -> float:
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

        probable_fail_outcomes = (
            modified_save - 1
        )  # e.g. a 5+ save fails on 1,2,3,4 => 4 outcomes
        return probable_fail_outcomes / 6

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

    def probability_to_hit(self):
        required_roll = self.weapon.ballistic_skill
        successful_outcomes = (
            7 - required_roll
        )  # e.g., for 4+, successful outcomes are 4,5,6 => 3 outcomes
        return successful_outcomes / 6

    def apply_benefit_of_cover(self, modified_save: int) -> int:
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

    def probability_to_hit(self):
        required_roll = self.weapon.weapon_skill
        successful_outcomes = (
            7 - required_roll
        )  # e.g., for 3+, successful outcomes are 3,4,5,6 => 4 outcomes
        return successful_outcomes / 6
