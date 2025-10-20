
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