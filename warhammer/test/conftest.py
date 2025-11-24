import sys
from pathlib import Path

import pytest

# Add parent directory to path to import warhammer module
sys.path.insert(0, str(Path(__file__).parent.parent))

from warhammer import MeleeWeapon, Model, RangedWeapon


@pytest.fixture
def bolter():
    return RangedWeapon(
        name="Bolter",
        range=24,
        attacks=1,
        ballistic_skill=4,
        strength=4,
        armour_penetration=-1,
        damage=1,
    )


@pytest.fixture
def bolt_pistol():
    return RangedWeapon(
        name="Bolt Pistol",
        range=12,
        attacks=1,
        ballistic_skill=4,
        strength=4,
        armour_penetration=-1,
        damage=1,
    )


@pytest.fixture
def chainsword():
    return MeleeWeapon(
        name="Chainsword",
        attacks=2,
        weapon_skill=3,
        strength=4,
        armour_penetration=-1,
        damage=1,
    )


@pytest.fixture
def space_marine(bolter, bolt_pistol, chainsword):
    return Model(
        name="Space Marine",
        movement=6,
        toughness=4,
        save=3,
        wounds=2,
        leadership=8,
        objective_control=1,
        ranged_weapons={"Bolter": bolter, "Bolt Pistol": bolt_pistol},
        melee_weapons={"Chainsword": chainsword},
    )


@pytest.fixture
def necron_warrior():
    return Model(
        name="Necron Warrior",
        movement=5,
        toughness=4,
        save=4,
        wounds=1,
        leadership=7,
        objective_control=2,
    )
