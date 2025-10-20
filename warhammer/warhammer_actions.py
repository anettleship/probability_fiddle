from ..warhammer.warhammer import Unit, RangedWeapon, MeleeWeapon

class Attack:
    def __init__(self, attacker: Unit, target:Unit):
        self.attacker = attacker
        self.target = target

class RangedAttack(Attack):
    def __init__(self, attacker: Unit, target:Unit, weapon: RangedWeapon):
        super().__init__(attacker, target)
        self.weapon = weapon 

class MeleeAttack(Attack):
    def __init__(self, attacker: Unit, target:Unit, weapon: MeleeWeapon):
        super().__init__(attacker, target)
        self.weapon = weapon