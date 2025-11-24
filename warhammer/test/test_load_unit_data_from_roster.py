from pathlib import Path

import pytest

from ..load_unit_data_from_roster import LoadUnitDataFromRoster

single_squad_roster_path = (
    Path(__file__).parent.parent / "test_data" / "Single_Terminator_Squad_Roster.json"
)

army_datasource_path = (
    Path(__file__).parent.parent / "test_data" / "Test_Terminators_Roster.json"
)

# Expected data for units in Test_Terminators_Roster.json
chaplain_expected_data = {
    "name": "Chaplain in Terminator Armour",
    "model_count": 1,
    "stats": {
        "movement": 5,
        "toughness": 5,
        "save": 2,
        "wounds": 5,
        "leadership": 5,
        "objective_control": 1,
    },
}

librarian_expected_data = {
    "name": "Librarian in Terminator Armour",
    "model_count": 1,
    "stats": {
        "movement": 5,
        "toughness": 5,
        "save": 2,
        "wounds": 5,
        "leadership": 6,
        "objective_control": 1,
    },
}

assault_squad_expected_data = {
    "name": "Terminator Assault Squad",
    "model_count": 5,
    "model_types": {
        "Assault Terminator Sergeant": 1,
        "Assault Terminator w/ Twin Lightning Claws": 4,
    },
    "stats": {
        "movement": 5,
        "toughness": 5,
        "save": 2,
        "wounds": 3,
        "leadership": 6,
        "objective_control": 1,
    },
}


@pytest.fixture
def roster_loader(datasource_path=single_squad_roster_path):
    """Initialize the loader with the path to the test roster file."""
    return LoadUnitDataFromRoster(datasource=datasource_path)


def test_load_terminator_squad_unit_from_roster_shows_single_unit(roster_loader):
    assert len(roster_loader.units) == 1, "Roster should contain exactly one unit"
    assert roster_loader.get_unit("Terminator Squad") is not None, (
        "Roster should contain 'Terminator Squad' unit"
    )


def test_load_terminator_squad_unit_from_roster_models_have_correct_attributes(
    roster_loader,
):
    terminator_unit = roster_loader.get_unit("Terminator Squad")
    all_models = terminator_unit.all_models()
    assert len(all_models) == 5, "Terminator Squad should contain 5 models"
    for model in all_models:
        assert model.movement == 5, "Terminator movement should be 5"
        assert model.toughness == 5, "Terminator toughness should be 5"
        assert model.save == 2, "Terminator save should be 2+"
        assert model.wounds == 3, "Terminator wounds should be 3"
        assert model.leadership == 6, "Terminator leadership should be 6+"
        assert model.objective_control == 1, "Terminator objective control should be 1"
        assert model.is_alive(), "Terminator should be alive"


def test_load_terminator_squad_unit_from_roster_has_correct_model_types(roster_loader):
    terminator_unit = roster_loader.get_unit("Terminator Squad")
    assert "Terminator Sergeant" in terminator_unit.model_types(), (
        "Terminator Squad should contain 'Terminator Sergeant' model type"
    )
    assert "Terminator w/ Heavy Weapon" in terminator_unit.model_types(), (
        "Terminator Squad should contain 'Terminator w/Heavy Weapon' model type"
    )
    assert "Terminator w/ Power Fist" in terminator_unit.model_types(), (
        "Terminator Squad should contain 'Terminator w/Power Fist' model type"
    )


def test_load_terminator_squad_unit_from_roster_has_correct_model_counts(roster_loader):
    terminator_unit = roster_loader.get_unit("Terminator Squad")
    assert len(terminator_unit.models["Terminator Sergeant"]) == 1, (
        "Terminator Squad should contain 1 'Terminator Sergeant'"
    )
    assert len(terminator_unit.models["Terminator w/ Heavy Weapon"]) == 1, (
        "Terminator Squad should contain 1 'Terminator w/ Heavy Weapon'"
    )
    assert len(terminator_unit.models["Terminator w/ Power Fist"]) == 3, (
        "Terminator Squad should contain 3 'Terminator w/ Power Fist'"
    )


def test_load_army_from_roster_contains_multiple_units():
    roster_loader = LoadUnitDataFromRoster(datasource=army_datasource_path)
    assert len(roster_loader.units) == 4, (
        "Army roster should contain exactly four units"
    )
    assert roster_loader.get_unit("Terminator Squad") is not None, (
        "Army roster should contain 'Terminator Squad' unit"
    )
    assert roster_loader.get_unit("Terminator Assault Squad") is not None, (
        "Army roster should contain 'Terminator Assault Squad' unit"
    )
    assert roster_loader.get_unit("Chaplain in Terminator Armour") is not None, (
        "Army roster should contain 'Chaplain in Terminator Armour' unit"
    )
    assert roster_loader.get_unit("Librarian in Terminator Armour") is not None, (
        "Army roster should contain 'Librarian in Terminator Armour' unit"
    )


def test_chaplain_in_terminator_armour_properties():
    roster_loader = LoadUnitDataFromRoster(datasource=army_datasource_path)
    chaplain = roster_loader.get_unit(chaplain_expected_data["name"])

    all_models = chaplain.all_models()
    assert len(all_models) == chaplain_expected_data["model_count"]

    for model in all_models:
        assert model.movement == chaplain_expected_data["stats"]["movement"]
        assert model.toughness == chaplain_expected_data["stats"]["toughness"]
        assert model.save == chaplain_expected_data["stats"]["save"]
        assert model.wounds == chaplain_expected_data["stats"]["wounds"]
        assert model.leadership == chaplain_expected_data["stats"]["leadership"]
        assert (
            model.objective_control
            == chaplain_expected_data["stats"]["objective_control"]
        )
        assert model.is_alive()


def test_librarian_in_terminator_armour_properties():
    roster_loader = LoadUnitDataFromRoster(datasource=army_datasource_path)
    librarian = roster_loader.get_unit(librarian_expected_data["name"])

    all_models = librarian.all_models()
    assert len(all_models) == librarian_expected_data["model_count"]

    for model in all_models:
        assert model.movement == librarian_expected_data["stats"]["movement"]
        assert model.toughness == librarian_expected_data["stats"]["toughness"]
        assert model.save == librarian_expected_data["stats"]["save"]
        assert model.wounds == librarian_expected_data["stats"]["wounds"]
        assert model.leadership == librarian_expected_data["stats"]["leadership"]
        assert (
            model.objective_control
            == librarian_expected_data["stats"]["objective_control"]
        )
        assert model.is_alive()


def test_terminator_assault_squad_properties():
    roster_loader = LoadUnitDataFromRoster(datasource=army_datasource_path)
    assault_squad = roster_loader.get_unit(assault_squad_expected_data["name"])

    all_models = assault_squad.all_models()
    assert len(all_models) == assault_squad_expected_data["model_count"]

    # Verify model type composition
    for model_type, expected_count in assault_squad_expected_data[
        "model_types"
    ].items():
        assert model_type in assault_squad.model_types()
        assert len(assault_squad.models[model_type]) == expected_count

    # Verify all models have correct stats
    for model in all_models:
        assert model.movement == assault_squad_expected_data["stats"]["movement"]
        assert model.toughness == assault_squad_expected_data["stats"]["toughness"]
        assert model.save == assault_squad_expected_data["stats"]["save"]
        assert model.wounds == assault_squad_expected_data["stats"]["wounds"]
        assert model.leadership == assault_squad_expected_data["stats"]["leadership"]
        assert (
            model.objective_control
            == assault_squad_expected_data["stats"]["objective_control"]
        )
        assert model.is_alive()
