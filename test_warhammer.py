from warhammer import Unit

def test_warhammer_unit_is_alive():

    unit = Unit(name="Space Marine", movement=6, toughness=4, save=3, wounds=2, leadership=8, objective_control=1)
    assert unit.is_alive() == True, "Unit should be alive when health is greater than 0"

    unit.health = 0
    assert unit.is_alive() == False, "Unit should not be alive when health is 0"

def test_warhammer_unit_properties():

    unit = Unit(name="Space Marine", movement=6, toughness=4, save=3, wounds=2, leadership=8, objective_control=1)
    assert unit.name == "Space Marine", "Unit name should be 'Space Marine'"
    assert unit.movement == 6, "Unit movement should be 6"
    assert unit.toughness == 4, "Unit toughness should be 4"
    assert unit.save == 3, "Unit save should be 3"
    assert unit.wounds == 2, "Unit wounds should be 2"
    assert unit.leadership == 8, "Unit leadership should be 8"
    assert unit.objective_control == 1, "Unit objective control should be 1"
    assert unit.health == unit.wounds, "Unit health should equal wounds on creation"