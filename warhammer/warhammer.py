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
        self.ranged_weapons = ranged_weapons if ranged_weapons is not None else {}
        self.melee_weapons = melee_weapons if melee_weapons is not None else {}

    def is_alive(self):
        return self.health > 0

    def health(self):
        return self.health


class Unit:
    def __init__(self, models: list[Model], name: str):
        # Group models by their name (type)
        self.models = {}
        for model in models:
            if model.name not in self.models:
                self.models[model.name] = []
            self.models[model.name].append(model)
        self.name = name

    def model_types(self):
        """Return the set of model type names in this unit."""
        return set(self.models.keys())

    def all_models(self):
        """Return a flat list of all models in the unit."""
        result = []
        for model_list in self.models.values():
            result.extend(model_list)
        return result


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
