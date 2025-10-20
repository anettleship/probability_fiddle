
class Unit:
    def __init__(self, name, movement, toughness, save, wounds, leadership, objective_control):
        self.name = name
        self.movement = movement
        self.toughness = toughness
        self.save = save
        self.wounds = wounds
        self.health = wounds
        self.leadership = leadership
        self.objective_control = objective_control

    def is_alive(self):
        return self.health > 0
    
    def health(self):
        return self.health
    
class Weapon:
    def __init__(self, bearer: Unit, name, attacks, strength, armour_penetration, damage):
        self.name = name
        self.attacks = attacks
        self.strength = strength
        self.armour_penetration = armour_penetration
        self.damage = damage
        self.bearer = bearer 

class RangedWeapon(Weapon):
    def __init__(self, bearer: Unit, name, range, attacks, ballistic_skill, strength, armour_penetration, damage):
        super().__init__(bearer, name, attacks, strength, armour_penetration, damage)
        self.range = range
        self.ballistic_skill = ballistic_skill

class MeleeWeapon(Weapon):
    def __init__(self, bearer: Unit, name, attacks, weapon_skill, strength, armour_penetration, damage):
        super().__init__(bearer, name, attacks, strength, armour_penetration, damage)
        self.weapon_skill = weapon_skill
