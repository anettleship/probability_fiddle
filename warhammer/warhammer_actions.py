from ..warhammer.warhammer import Model, RangedWeapon, MeleeWeapon

class Attack:
    def __init__(self, attacker: Model, target:Model):
        self.attacker = attacker
        self.target = target
        self.weapon = None  # To be defined in subclasses

    def probability_to_wound(self):
        if self.weapon is None:
            raise NotImplementedError("Weapon must be defined in subclass to calculate wound probability.")

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

class RangedAttack(Attack):
    def __init__(self, attacker: Model, target:Model, weapon: RangedWeapon):
        super().__init__(attacker, target)
        self.weapon = weapon 

    def probability_to_hit(self):
        required_roll = self.weapon.ballistic_skill
        successful_outcomes = 7 - required_roll  # e.g., for 4+, successful outcomes are 4,5,6 => 3 outcomes
        return successful_outcomes / 6

class MeleeAttack(Attack):
    def __init__(self, attacker: Model, target:Model, weapon: MeleeWeapon):
        super().__init__(attacker, target)
        self.weapon = weapon

    def probability_to_hit(self):
        required_roll = self.weapon.weapon_skill
        successful_outcomes = 7 - required_roll  # e.g., for 3+, successful outcomes are 3,4,5,6 => 4 outcomes
        return successful_outcomes / 6