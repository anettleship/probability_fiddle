"""Test that the loader can handle duplicate unit names (e.g., 2 Deff Dreads)."""

from pathlib import Path

from ..load_unit_data_from_roster import LoadUnitDataFromRoster

ork_army_roster_path = (
    Path(__file__).parent.parent / "test_data" / "Ork_Army_Roster.json"
)


def test_loader_handles_duplicate_unit_names():
    """Test that loader preserves both Deff Dread units instead of overwriting."""
    roster_loader = LoadUnitDataFromRoster(datasource=ork_army_roster_path)

    # Filter units to find all Deff Dreads
    deff_dreads = roster_loader.get_units_by_name("Deff Dread")

    assert len(deff_dreads) == 2, (
        f"Should have 2 Deff Dread units, but got {len(deff_dreads)}"
    )

    # Each Deff Dread should be a single model unit
    for deff_dread in deff_dreads:
        assert len(deff_dread.all_models()) == 1
        model = deff_dread.all_models()[0]
        assert model.movement == 8
        assert model.toughness == 9
        assert model.save == 2
        assert model.wounds == 8
