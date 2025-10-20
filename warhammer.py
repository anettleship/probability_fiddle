
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
    def __init__(self, name, range, attacks, strength, armor_penetration, damage):
        self.name = name
        self.range = range
        self.attacks = attacks
        self.strength = strength
        self.armor_penetration = armor_penetration
        self.damage = damage