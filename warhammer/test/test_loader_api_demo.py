"""Demo showing the improved API for LoadUnitDataFromRoster."""

from pathlib import Path

from ..load_unit_data_from_roster import LoadUnitDataFromRoster

ork_army_roster_path = (
    Path(__file__).parent.parent / "test_data" / "Ork_Army_Roster.json"
)


def test_demo_easy_unit_lookup():
    """Demonstrate the easy unit lookup with the new API."""
    loader = LoadUnitDataFromRoster(datasource=ork_army_roster_path)

    # OLD WAY (with list):
    # warboss = [u for u in loader.units if u.name == "Warboss in Mega Armour"][0]

    # NEW WAY (with dict + helper):
    warboss = loader.get_unit("Warboss in Mega Armour")

    assert warboss is not None
    assert warboss.name == "Warboss in Mega Armour"
    assert len(warboss.all_models()) == 1


def test_demo_handling_duplicates():
    """Demonstrate handling duplicate unit names (2 Deff Dreads)."""
    loader = LoadUnitDataFromRoster(datasource=ork_army_roster_path)

    # OLD WAY (with list):
    # deff_dreads = [u for u in loader.units if u.name == "Deff Dread"]

    # NEW WAY (with dict + helper):
    deff_dreads = loader.get_units_by_name("Deff Dread")

    assert len(deff_dreads) == 2
    for dread in deff_dreads:
        assert dread.name == "Deff Dread"
        assert len(dread.all_models()) == 1


def test_demo_dict_still_accessible():
    """Show that the underlying dict is still accessible if needed."""
    loader = LoadUnitDataFromRoster(datasource=ork_army_roster_path)

    # Units are still stored in a dict with unique keys
    assert isinstance(loader.units, dict)
    assert len(loader.units) == 11

    # Keys are unique, even for duplicate names
    keys = list(loader.units.keys())
    assert "Deff Dread" in keys
    assert "Deff Dread_1" in keys  # Second Deff Dread gets unique key

    # Can still iterate over units if needed
    unit_names = [unit.name for unit in loader.units.values()]
    assert unit_names.count("Deff Dread") == 2
