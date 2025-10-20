from warhammer import Unit

def test_warhammer_unit_is_alive():

    unit = Unit(name="Space Marine", movement=6, toughness=4, save=3, wounds=2, leadership=8, objective_control=1)
    assert unit.is_alive() == True, "Unit should be alive when health is greater than 0"

    unit.health = 0
    assert unit.is_alive() == False, "Unit should not be alive when health is 0"

def test_warhammer_unit_has_properties():

    unit = Unit(name="Space Marine", movement=6, toughness=4, save=3, wounds=2, leadership=8, objective_control=1)
    assert unit.name == "Space Marine", "Unit name should be 'Space Marine'"
    assert unit.movement == 6, "Unit movement should be 6"
    assert unit.toughness == 4, "Unit toughness should be 4"
    assert unit.save == 3, "Unit save should be 3"
    assert unit.wounds == 2, "Unit wounds should be 2"
    assert unit.leadership == 8, "Unit leadership should be 8"
    assert unit.objective_control == 1, "Unit objective control should be 1"
    assert unit.health == unit.wounds, "Unit health should equal wounds on creation"

def test_warhammer_weapon_properties():
    from warhammer import Weapon

    weapon = Weapon(name="Bolter", range=24, attacks=1, strength=4, armor_penetration=-1, damage=1)
    assert weapon.name == "Bolter", "Weapon name should be 'Bolter'"
    assert weapon.range == 24, "Weapon range should be 24"
    assert weapon.attacks == 1, "Weapon attacks should be 1"
    assert weapon.strength == 4, "Weapon strength should be 4"
    assert weapon.armor_penetration == -1, "Weapon armor penetration should be -1"
    assert weapon.damage == 1, "Weapon damage should be 1"