from ..warhammer.warhammer import Unit, RangedWeapon, MeleeWeapon

class Attack:
    def __init__(self, attacker: Unit, target:Unit):
        self.attacker = attacker
        self.target = target

class RangedAttack(Attack):
    def __init__(self, attacker: Unit, target:Unit, weapon: RangedWeapon):
        super().__init__(attacker, target)
        self.weapon = weapon 

    def probability_to_hit(self):
        required_roll = self.weapon.ballistic_skill
        successful_outcomes = 7 - required_roll  # e.g., for 4+, successful outcomes are 4,5,6 => 3 outcomes
        return successful_outcomes / 6

class MeleeAttack(Attack):
    def __init__(self, attacker: Unit, target:Unit, weapon: MeleeWeapon):
        super().__init__(attacker, target)
        self.weapon = weapon

    def probability_to_hit(self):
        required_roll = self.weapon.weapon_skill
        successful_outcomes = 7 - required_roll  # e.g., for 3+, successful outcomes are 3,4,5,6 => 4 outcomes
        return successful_outcomes / 6