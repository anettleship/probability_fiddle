from __future__ import annotations

from .constants import WeaponAttribute


class Model:
    def __init__(
        self,
        name: str,
        movement: int,
        toughness: int,
        save: int,
        wounds: int,
        leadership: int,
        objective_control: int,
        invulnerable_save: int | None = None,
        feel_no_pain: int | None = None,
        ranged_weapons: dict | None = None,
        melee_weapons: dict | None = None,
    ) -> None:
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
        setattr(self, WeaponAttribute.RANGED.value, ranged_weapons if ranged_weapons is not None else {})
        setattr(self, WeaponAttribute.MELEE.value, melee_weapons if melee_weapons is not None else {})

    def is_alive(self) -> bool:
        return self.health > 0

    def health(self) -> int:
        return self.health


class Weapon:
    def __init__(
        self,
        name: str,
        attacks: int,
        strength: int,
        armour_penetration: int,
        damage: int,
        keywords: list[str] | None = None,
    ) -> None:
        self.name = name
        self.attacks = attacks
        self.strength = strength
        self.armour_penetration = armour_penetration
        self.damage = damage
        self.keywords = keywords if keywords is not None else []


class RangedWeapon(Weapon):
    def __init__(
        self,
        name: str,
        range: int,
        attacks: int,
        ballistic_skill: int,
        strength: int,
        armour_penetration: int,
        damage: int,
        keywords: list[str] | None = None,
    ) -> None:
        super().__init__(name, attacks, strength, armour_penetration, damage, keywords)
        self.range = range
        self.ballistic_skill = ballistic_skill


class MeleeWeapon(Weapon):
    def __init__(
        self,
        name: str,
        attacks: int,
        weapon_skill: int,
        strength: int,
        armour_penetration: int,
        damage: int,
        keywords: list[str] | None = None,
    ) -> None:
        super().__init__(name, attacks, strength, armour_penetration, damage, keywords)
        self.weapon_skill = weapon_skill
