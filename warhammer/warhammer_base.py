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
        invulnerable_save=None,
        feel_no_pain=None,
        ranged_weapons=None,
        melee_weapons=None,
    ):
        self.name = name
        self.movement = movement
        self.toughness = toughness
        self.save = save
        self.wounds = wounds
        self.health = wounds
        self.leadership = leadership
        self.objective_control = objective_control
        self.invulnerable_save = invulnerable_save
        self.feel_no_pain = feel_no_pain
        self.ranged_weapons = ranged_weapons if ranged_weapons is not None else {}
        self.melee_weapons = melee_weapons if melee_weapons is not None else {}

    def is_alive(self):
        return self.health > 0

    def health(self):
        return self.health


class Weapon:
    def __init__(
        self, name, attacks, strength, armour_penetration, damage, keywords=None
    ):
        self.name = name
        self.attacks = attacks
        self.strength = strength
        self.armour_penetration = armour_penetration
        self.damage = damage
        self.keywords = keywords if keywords is not None else []


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
        keywords=None,
    ):
        super().__init__(name, attacks, strength, armour_penetration, damage, keywords)
        self.range = range
        self.ballistic_skill = ballistic_skill


class MeleeWeapon(Weapon):
    def __init__(
        self,
        name,
        attacks,
        weapon_skill,
        strength,
        armour_penetration,
        damage,
        keywords=None,
    ):
        super().__init__(name, attacks, strength, armour_penetration, damage, keywords)
        self.weapon_skill = weapon_skill
