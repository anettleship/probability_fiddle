from ..warhammer import MeleeWeapon, Unit


def test_warhammer_model_is_alive(space_marine):
    unit = space_marine
    assert unit.is_alive(), "Unit should be alive when health is greater than 0"

    unit.health = 0
    assert not unit.is_alive(), "Unit should not be alive when health is 0"


def test_warhammer_model_has_properties(space_marine, bolter, bolt_pistol, chainsword):
    unit = space_marine
    assert unit.name == "Space Marine", "Unit name should be 'Space Marine'"
    assert unit.movement == 6, "Unit movement should be 6"
    assert unit.toughness == 4, "Unit toughness should be 4"
    assert unit.save == 3, "Unit save should be 3"
    assert unit.wounds == 2, "Unit wounds should be 2"
    assert unit.leadership == 8, "Unit leadership should be 8"
    assert unit.objective_control == 1, "Unit objective control should be 1"
    assert unit.health == unit.wounds, "Unit health should equal wounds on creation"
    assert unit.ranged_weapons == {"Bolter": bolter, "Bolt Pistol": bolt_pistol}, (
        "Unit should have correct ranged weapons"
    )
    assert unit.melee_weapons == {"Chainsword": chainsword}, (
        "Unit should have correct melee weapons"
    )


def test_warhammer_weapon_properties(space_marine):
    unit = space_marine
    weapon = unit.ranged_weapons["Bolter"]
    assert weapon.name == "Bolter", "Weapon name should be 'Bolter'"
    assert weapon.range == 24, "Weapon range should be 24"
    assert weapon.attacks == 1, "Weapon attacks should be 1"
    assert weapon.ballistic_skill == 4, "Weapon ballistic skill should be 4"
    assert weapon.strength == 4, "Weapon strength should be 4"
    assert weapon.armour_penetration == -1, "Weapon armor penetration should be -1"
    assert weapon.damage == 1, "Weapon damage should be 1"


def test_warhammer_melee_weapon_properties():
    weapon = MeleeWeapon(
        name="Chainsword",
        attacks=2,
        weapon_skill=3,
        strength=4,
        armour_penetration=-1,
        damage=1,
    )

    assert weapon.name == "Chainsword", "Weapon name should be 'Chainsword'"
    assert weapon.attacks == 2, "Weapon attacks should be 2"
    assert weapon.weapon_skill == 3, "Weapon skill should be 3"
    assert weapon.strength == 4, "Weapon strength should be 4"
    assert weapon.armour_penetration == -1, "Weapon armor penetration should be -1"
    assert weapon.damage == 1, "Weapon damage should be 1"


def test_warhammer_unit_properties_should_be_a_group_of_models_with_properties_and_weapons(
    space_marine,
):
    """Test that a Unit contains multiple Models and exposes unit-level properties."""
    # Create a unit with 5 models (1 sergeant + 4 marines, all using space_marine stats for simplicity)
    models = [space_marine for _ in range(5)]
    unit = Unit(models=models, name="Tactical Squad")

    # Verify unit has correct name and models
    assert unit.name == "Tactical Squad", "Unit should have correct name"
    assert len(unit.models) == 5, "Unit should contain 5 models"
    assert all(isinstance(model, type(space_marine)) for model in unit.models), (
        "All models should be Model instances"
    )

    # Verify we can access individual models
    first_model = unit.models[0]
    assert first_model.name == "Space Marine", (
        "Should be able to access individual model properties"
    )
    assert first_model.toughness == 4, (
        "Individual models should retain their characteristics"
    )

    # Verify all models in unit have expected characteristics
    for model in unit.models:
        assert model.movement == 6
        assert model.toughness == 4
        assert model.save == 3
        assert model.wounds == 2
        assert model.is_alive()
