class Model:
    def __init__(
        self,
        name,
        movement,
        toughness,
        save,
        wounds,
        leadership,
        objective_control,
        ranged_weapons=list(),
        melee_weapons=list(),
    ):
        self.name = name
        self.movement = movement
        self.toughness = toughness
        self.save = save
        self.wounds = wounds
        self.health = wounds
        self.leadership = leadership
        self.objective_control = objective_control
        self.ranged_weapons = ranged_weapons
        self.melee_weapons = melee_weapons

    def is_alive(self):
        return self.health > 0

    def health(self):
        return self.health


class Unit:
    def __init__(self, models: list[Model], name: str):
        self.models = models
        self.name = name


class Weapon:
    def __init__(self, name, attacks, strength, armour_penetration, damage):
        self.name = name
        self.attacks = attacks
        self.strength = strength
        self.armour_penetration = armour_penetration
        self.damage = damage


class RangedWeapon(Weapon):
    def __init__(
        self,
        name,
        range,
        attacks,
        ballistic_skill,
        strength,
        armour_penetration,
        damage,
    ):
        super().__init__(name, attacks, strength, armour_penetration, damage)
        self.range = range
        self.ballistic_skill = ballistic_skill


class MeleeWeapon(Weapon):
    def __init__(
        self, name, attacks, weapon_skill, strength, armour_penetration, damage
    ):
        super().__init__(name, attacks, strength, armour_penetration, damage)
        self.weapon_skill = weapon_skill
