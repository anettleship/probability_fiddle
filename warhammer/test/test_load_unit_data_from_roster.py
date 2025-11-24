from pathlib import Path

import pytest

from ..load_unit_data_from_roster import LoadUnitDataFromRoster

single_squad_roster_path = (
    Path(__file__).parent.parent / "test_data" / "Single_Terminator_Squad_Roster.json"
)

army_datasource_path = (
    Path(__file__).parent.parent / "test_data" / "Test_Terminators_Roster.json"
)


@pytest.fixture
def roster_loader(datasource_path=single_squad_roster_path):
    """Initialize the loader with the path to the test roster file."""
    return LoadUnitDataFromRoster(datasource=datasource_path)


def test_load_terminator_squad_unit_from_roster_shows_single_unit(roster_loader):
    assert len(roster_loader.units) == 1, "Roster should contain exactly one unit"
    assert "Terminator Squad" in roster_loader.units, (
        "Roster should contain 'Terminator Squad' unit"
    )


def test_load_terminator_squad_unit_from_roster_models_have_correct_attributes(
    roster_loader,
):
    terminator_unit = roster_loader.units["Terminator Squad"]
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
    terminator_unit = roster_loader.units["Terminator Squad"]
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
    terminator_unit = roster_loader.units["Terminator Squad"]
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
    assert "Terminator Squad" in roster_loader.units, (
        "Army roster should contain 'Terminator Squad' unit"
    )
    assert "Terminator Assault Squad" in roster_loader.units, (
        "Army roster should contain 'Terminator Assault Squad' unit"
    )
    assert "Chaplain in Terminator Armour" in roster_loader.units, (
        "Army roster should contain 'Chaplain in Terminator Armour' unit"
    )
    assert "Librarian in Terminator Armour" in roster_loader.units, (
        "Army roster should contain 'Librarian in Terminator Armour' unit"
    )
