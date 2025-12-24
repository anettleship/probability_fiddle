import pytest

from ..warhammer import Model, Unit
from ..warhammer_base import MeleeWeapon, RangedWeapon


@pytest.fixture
def bolter():
    return RangedWeapon(
        name="Bolter",
        range=24,
        attacks=1,
        ballistic_skill=3,
        strength=4,
        armour_penetration=-1,
        damage=1,
    )


@pytest.fixture
def gauss_flayer():
    return RangedWeapon(
        name="Gauss Flayer",
        range=24,
        attacks=1,
        ballistic_skill=4,
        strength=4,
        armour_penetration=0,
        damage=1,
    )


@pytest.fixture
def lascannon():
    return RangedWeapon(
        name="Lascannon",
        range=48,
        attacks=1,
        ballistic_skill=3,
        strength=9,
        armour_penetration=-3,
        damage=6,
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
def close_combat_weapon():
    return MeleeWeapon(
        name="Close combat weapon",
        attacks=1,
        weapon_skill=4,
        strength=4,
        armour_penetration=0,
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
def necron_warrior(gauss_flayer, close_combat_weapon):
    return Model(
        name="Necron Warrior",
        movement=5,
        toughness=4,
        save=4,
        wounds=1,
        leadership=7,
        objective_control=2,
        ranged_weapons={"Gauss Flayer": gauss_flayer},
        melee_weapons={"Close combat weapon": close_combat_weapon},
    )


@pytest.fixture
def tough_target():
    return Model(
        name="Tough Target",
        movement=5,
        toughness=8,  # High toughness for testing Lethal Hits
        save=3,
        wounds=5,
        leadership=7,
        objective_control=1,
    )


@pytest.fixture
def storm_bolter():
    return RangedWeapon(
        name="Storm Bolter",
        range=24,
        attacks=2,
        ballistic_skill=3,
        strength=4,
        armour_penetration=0,
        damage=1,
    )


@pytest.fixture
def heavy_flamer():
    return RangedWeapon(
        name="Heavy Flamer",
        range=12,
        attacks=6,  # D6 attacks
        ballistic_skill=0,  # Auto-hit weapon
        strength=5,
        armour_penetration=-1,
        damage=1,
        keywords=["Ignores Cover", "Torrent"],
    )


@pytest.fixture
def lethal_hits_weapon():
    return RangedWeapon(
        name="Precision Rifle",
        range=24,
        attacks=1,
        ballistic_skill=3,  # 3+ to hit
        strength=4,
        armour_penetration=-1,
        damage=1,
        keywords=["Lethal Hits"],
    )


@pytest.fixture
def power_fist():
    return MeleeWeapon(
        name="Power Fist",
        attacks=3,
        weapon_skill=3,
        strength=8,
        armour_penetration=-2,
        damage=2,
    )


@pytest.fixture
def terminator_sergeant(storm_bolter, power_fist):
    return Model(
        name="Terminator Sergeant",
        movement=5,
        toughness=5,
        save=2,
        wounds=3,
        leadership=6,
        objective_control=1,
        invulnerable_save=4,
        ranged_weapons={"Storm Bolter": storm_bolter},
        melee_weapons={"Power Fist": power_fist},
    )


@pytest.fixture
def terminator_with_storm_bolter(storm_bolter, power_fist):
    return Model(
        name="Terminator w/ Storm Bolter",
        movement=5,
        toughness=5,
        save=2,
        wounds=3,
        leadership=6,
        objective_control=1,
        invulnerable_save=4,
        ranged_weapons={"Storm Bolter": storm_bolter},
        melee_weapons={"Power Fist": power_fist},
    )


@pytest.fixture
def terminator_with_heavy_flamer(heavy_flamer, power_fist):
    return Model(
        name="Terminator w/ Heavy Flamer",
        movement=5,
        toughness=5,
        save=2,
        wounds=3,
        leadership=6,
        objective_control=1,
        invulnerable_save=4,
        ranged_weapons={"Heavy Flamer": heavy_flamer},
        melee_weapons={"Power Fist": power_fist},
    )


@pytest.fixture
def terminator_unit(
    terminator_sergeant, terminator_with_storm_bolter, terminator_with_heavy_flamer
):
    """5-man Terminator squad: 1 Sergeant, 3 with storm bolters, 1 with heavy flamer"""
    models = [
        terminator_sergeant,
        terminator_with_storm_bolter,
        terminator_with_storm_bolter,
        terminator_with_storm_bolter,
        terminator_with_heavy_flamer,
    ]
    return Unit(models=models, name="Terminator Squad")


@pytest.fixture
def necron_warrior_unit(necron_warrior):
    """Unit with a single Necron Warrior model."""
    models = [necron_warrior] * 10
    return Unit(models=models, name="Necron Warrior Unit")
