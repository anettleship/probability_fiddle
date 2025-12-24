"""Constants used across the Warhammer combat simulation system."""

from enum import Enum


class SimulationMethod(Enum):
    """Names of Unit simulation methods for different attack types."""
    MELEE = "melee_attack_simulation"
    RANGED = "shoot_at_simulation"


class WeaponAttribute(Enum):
    """Names of Model attributes that store weapons for different attack types."""
    MELEE = "melee_weapons"
    RANGED = "ranged_weapons"
