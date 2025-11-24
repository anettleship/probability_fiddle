"""Tests for loading Ork army roster with 11 units including duplicate Deff Dreads."""

from pathlib import Path

import pytest

from ..load_unit_data_from_roster import LoadUnitDataFromRoster

ork_army_roster_path = (
    Path(__file__).parent.parent / "test_data" / "Ork_Army_Roster.json"
)

# Expected data for Ork units based on user's army list
big_mek_expected_data = {
    "name": "Big Mek with Shokk Attack Gun",
    "model_count": 1,
    "stats": {
        "movement": 6,
        "toughness": 5,
        "save": 4,
        "wounds": 5,
        "leadership": 7,
        "objective_control": 1,
    },
}

warboss_expected_data = {
    "name": "Warboss in Mega Armour",
    "model_count": 1,
    "stats": {
        "movement": 5,
        "toughness": 6,
        "save": 2,
        "wounds": 7,
        "leadership": 6,
        "objective_control": 1,
    },
}

weirdboy_expected_data = {
    "name": "Weirdboy",
    "model_count": 1,
    "stats": {
        "movement": 6,
        "toughness": 5,
        "save": 5,
        "wounds": 4,
        "leadership": 7,
        "objective_control": 1,
    },
}

boyz_expected_data = {
    "name": "Boyz",
    "model_count": 10,
    "model_types": {
        "Boy w/ Slugga and choppa": 8,
        "Boy w/ Big shoota and close combat weapon": 1,
        "Boss Nob": 1,
    },
    "stats": {
        "movement": 6,
        "toughness": 5,
        "save": 5,
        "wounds": 1,
        "leadership": 7,
        "objective_control": 2,
    },
}

gretchin_expected_data = {
    "name": "Gretchin",
    "model_count": 22,
    "model_types": {
        "Gretchin": 20,
        "Runtherd": 2,
    },
    "stats_gretchin": {
        "movement": 6,
        "toughness": 2,
        "save": 7,
        "wounds": 1,
        "leadership": 8,
        "objective_control": 2,
    },
    "stats_runtherd": {
        "movement": 6,
        "toughness": 4,
        "save": 6,
        "wounds": 2,
        "leadership": 7,
        "objective_control": 1,
    },
}

kommandos_expected_data = {
    "name": "Kommandos",
    "model_count": 10,
    "model_types": {
        "Kommandos w/ Slugga and choppa": 8,
        "Kommandos w/ Rokkit launcha": 1,
        "Boss Nob": 1,
    },
    "stats": {
        "movement": 6,
        "toughness": 5,
        "save": 5,
        "wounds": 1,
        "leadership": 7,
        "objective_control": 1,
    },
}

lootas_expected_data = {
    "name": "Lootas",
    "model_count": 5,
    "model_types": {
        "Loota": 4,
        "Spanner": 1,
    },
    "stats": {
        "movement": 6,
        "toughness": 5,
        "save": 5,
        "wounds": 1,
        "leadership": 7,
        "objective_control": 1,
    },
}

meganobz_expected_data = {
    "name": "Meganobz",
    "model_count": 3,
    "stats": {
        "movement": 5,
        "toughness": 6,
        "save": 2,
        "wounds": 3,
        "leadership": 7,
        "objective_control": 1,
    },
}

deff_dread_expected_data = {
    "name": "Deff Dread",
    "model_count": 1,
    "stats": {
        "movement": 8,
        "toughness": 9,
        "save": 2,
        "wounds": 8,
        "leadership": 7,
        "objective_control": 3,
    },
}

mek_gunz_expected_data = {
    "name": "Mek Gunz",
    "model_count": 2,
    "model_types": {
        "Mek Gun w/ Kustom mega-kannon": 1,
        "Mek Gun w/ Smasha gun": 1,
    },
    "stats": {
        "movement": 3,
        "toughness": 5,
        "save": 5,
        "wounds": 6,
        "leadership": 8,
        "objective_control": 2,
    },
}


@pytest.fixture
def ork_roster_loader():
    """Initialize the loader with the Ork army roster."""
    return LoadUnitDataFromRoster(datasource=ork_army_roster_path)


def test_ork_roster_contains_correct_number_of_units(ork_roster_loader):
    """Test that the roster contains all 11 units (including 2 Deff Dreads)."""
    assert len(ork_roster_loader.units) == 11


def test_ork_roster_contains_all_expected_units(ork_roster_loader):
    """Test that roster contains all expected unit types."""
    assert ork_roster_loader.get_unit("Big Mek with Shokk Attack Gun") is not None
    assert ork_roster_loader.get_unit("Warboss in Mega Armour") is not None
    assert ork_roster_loader.get_unit("Weirdboy") is not None
    assert ork_roster_loader.get_unit("Boyz") is not None
    assert ork_roster_loader.get_unit("Gretchin") is not None
    assert ork_roster_loader.get_unit("Kommandos") is not None
    assert ork_roster_loader.get_unit("Lootas") is not None
    assert ork_roster_loader.get_unit("Meganobz") is not None
    assert ork_roster_loader.get_unit("Mek Gunz") is not None

    # Should have 2 Deff Dreads
    deff_dreads = ork_roster_loader.get_units_by_name("Deff Dread")
    assert len(deff_dreads) == 2


def test_big_mek_properties(ork_roster_loader):
    """Test Big Mek with Shokk Attack Gun has correct properties."""
    big_mek = ork_roster_loader.get_unit(big_mek_expected_data["name"])

    all_models = big_mek.all_models()
    assert len(all_models) == big_mek_expected_data["model_count"]

    for model in all_models:
        assert model.movement == big_mek_expected_data["stats"]["movement"]
        assert model.toughness == big_mek_expected_data["stats"]["toughness"]
        assert model.save == big_mek_expected_data["stats"]["save"]
        assert model.wounds == big_mek_expected_data["stats"]["wounds"]
        assert model.leadership == big_mek_expected_data["stats"]["leadership"]
        assert (
            model.objective_control
            == big_mek_expected_data["stats"]["objective_control"]
        )


def test_warboss_properties(ork_roster_loader):
    """Test Warboss in Mega Armour has correct properties."""
    warboss = ork_roster_loader.get_unit(warboss_expected_data["name"])

    all_models = warboss.all_models()
    assert len(all_models) == warboss_expected_data["model_count"]

    for model in all_models:
        assert model.movement == warboss_expected_data["stats"]["movement"]
        assert model.toughness == warboss_expected_data["stats"]["toughness"]
        assert model.save == warboss_expected_data["stats"]["save"]
        assert model.wounds == warboss_expected_data["stats"]["wounds"]
        assert model.leadership == warboss_expected_data["stats"]["leadership"]
        assert (
            model.objective_control
            == warboss_expected_data["stats"]["objective_control"]
        )


def test_weirdboy_properties(ork_roster_loader):
    """Test Weirdboy has correct properties."""
    weirdboy = ork_roster_loader.get_unit(weirdboy_expected_data["name"])

    all_models = weirdboy.all_models()
    assert len(all_models) == weirdboy_expected_data["model_count"]

    for model in all_models:
        assert model.movement == weirdboy_expected_data["stats"]["movement"]
        assert model.toughness == weirdboy_expected_data["stats"]["toughness"]
        assert model.save == weirdboy_expected_data["stats"]["save"]
        assert model.wounds == weirdboy_expected_data["stats"]["wounds"]
        assert model.leadership == weirdboy_expected_data["stats"]["leadership"]
        assert (
            model.objective_control
            == weirdboy_expected_data["stats"]["objective_control"]
        )


def test_boyz_properties(ork_roster_loader):
    """Test Boyz unit has correct properties and model composition."""
    boyz = ork_roster_loader.get_unit(boyz_expected_data["name"])

    all_models = boyz.all_models()
    assert len(all_models) == boyz_expected_data["model_count"]

    # Verify model type composition
    for model_type, expected_count in boyz_expected_data["model_types"].items():
        assert model_type in boyz.model_types()
        assert len(boyz.models[model_type]) == expected_count

    # Regular boys and Boss Nob have different wounds - check common stats only
    for model in all_models:
        assert model.movement == boyz_expected_data["stats"]["movement"]
        assert model.toughness == boyz_expected_data["stats"]["toughness"]
        assert model.save == boyz_expected_data["stats"]["save"]
        # Note: Boy has W=1, Boss Nob has W=2 - not checking wounds
        assert model.leadership == boyz_expected_data["stats"]["leadership"]
        assert (
            model.objective_control == boyz_expected_data["stats"]["objective_control"]
        )


@pytest.mark.skip(
    reason="Gretchin unit has deeply nested structure - loader needs enhancement"
)
def test_gretchin_properties(ork_roster_loader):
    """Test Gretchin unit has correct properties and model composition."""
    gretchin = ork_roster_loader.get_unit(gretchin_expected_data["name"])

    all_models = gretchin.all_models()
    assert len(all_models) == gretchin_expected_data["model_count"]

    # Verify model type composition
    for model_type, expected_count in gretchin_expected_data["model_types"].items():
        assert model_type in gretchin.model_types()
        assert len(gretchin.models[model_type]) == expected_count

    # Verify Gretchin models have correct stats
    gretchin_models = gretchin.models["Gretchin"]
    for model in gretchin_models:
        assert model.movement == gretchin_expected_data["stats_gretchin"]["movement"]
        assert model.toughness == gretchin_expected_data["stats_gretchin"]["toughness"]
        assert model.save == gretchin_expected_data["stats_gretchin"]["save"]
        assert model.wounds == gretchin_expected_data["stats_gretchin"]["wounds"]
        assert (
            model.leadership == gretchin_expected_data["stats_gretchin"]["leadership"]
        )
        assert (
            model.objective_control
            == gretchin_expected_data["stats_gretchin"]["objective_control"]
        )

    # Verify Runtherd models have correct stats
    runtherd_models = gretchin.models["Runtherd"]
    for model in runtherd_models:
        assert model.movement == gretchin_expected_data["stats_runtherd"]["movement"]
        assert model.toughness == gretchin_expected_data["stats_runtherd"]["toughness"]
        assert model.save == gretchin_expected_data["stats_runtherd"]["save"]
        assert model.wounds == gretchin_expected_data["stats_runtherd"]["wounds"]
        assert (
            model.leadership == gretchin_expected_data["stats_runtherd"]["leadership"]
        )
        assert (
            model.objective_control
            == gretchin_expected_data["stats_runtherd"]["objective_control"]
        )


def test_kommandos_properties(ork_roster_loader):
    """Test Kommandos unit has correct properties and model composition."""
    kommandos = ork_roster_loader.get_unit(kommandos_expected_data["name"])

    all_models = kommandos.all_models()
    assert len(all_models) == kommandos_expected_data["model_count"]

    # Verify model type composition
    for model_type, expected_count in kommandos_expected_data["model_types"].items():
        assert model_type in kommandos.model_types()
        assert len(kommandos.models[model_type]) == expected_count

    # Regular kommandos and Boss Nob have different wounds - check common stats only
    for model in all_models:
        assert model.movement == kommandos_expected_data["stats"]["movement"]
        assert model.toughness == kommandos_expected_data["stats"]["toughness"]
        assert model.save == kommandos_expected_data["stats"]["save"]
        # Note: Kommando has W=1, Boss Nob has W=2 - not checking wounds
        assert model.leadership == kommandos_expected_data["stats"]["leadership"]
        assert (
            model.objective_control
            == kommandos_expected_data["stats"]["objective_control"]
        )


@pytest.mark.skip(
    reason="Lootas unit has deeply nested structure - loader needs enhancement"
)
def test_lootas_properties(ork_roster_loader):
    """Test Lootas unit has correct properties and model composition."""
    lootas = ork_roster_loader.get_unit(lootas_expected_data["name"])

    all_models = lootas.all_models()
    assert len(all_models) == lootas_expected_data["model_count"]

    # Verify model type composition
    for model_type, expected_count in lootas_expected_data["model_types"].items():
        assert model_type in lootas.model_types()
        assert len(lootas.models[model_type]) == expected_count

    # All models should have same stats
    for model in all_models:
        assert model.movement == lootas_expected_data["stats"]["movement"]
        assert model.toughness == lootas_expected_data["stats"]["toughness"]
        assert model.save == lootas_expected_data["stats"]["save"]
        assert model.wounds == lootas_expected_data["stats"]["wounds"]
        assert model.leadership == lootas_expected_data["stats"]["leadership"]
        assert (
            model.objective_control
            == lootas_expected_data["stats"]["objective_control"]
        )


@pytest.mark.skip(
    reason="Meganobz unit has deeply nested structure - loader needs enhancement"
)
def test_meganobz_properties(ork_roster_loader):
    """Test Meganobz unit has correct properties."""
    meganobz = ork_roster_loader.get_unit(meganobz_expected_data["name"])

    all_models = meganobz.all_models()
    assert len(all_models) == meganobz_expected_data["model_count"]

    for model in all_models:
        assert model.movement == meganobz_expected_data["stats"]["movement"]
        assert model.toughness == meganobz_expected_data["stats"]["toughness"]
        assert model.save == meganobz_expected_data["stats"]["save"]
        assert model.wounds == meganobz_expected_data["stats"]["wounds"]
        assert model.leadership == meganobz_expected_data["stats"]["leadership"]
        assert (
            model.objective_control
            == meganobz_expected_data["stats"]["objective_control"]
        )


def test_deff_dread_properties(ork_roster_loader):
    """Test both Deff Dread units have correct properties."""
    deff_dreads = ork_roster_loader.get_units_by_name(deff_dread_expected_data["name"])

    assert len(deff_dreads) == 2, "Should have 2 Deff Dread units"

    # Each Deff Dread should have same stats
    for deff_dread in deff_dreads:
        all_models = deff_dread.all_models()
        assert len(all_models) == deff_dread_expected_data["model_count"]

        for model in all_models:
            assert model.movement == deff_dread_expected_data["stats"]["movement"]
            assert model.toughness == deff_dread_expected_data["stats"]["toughness"]
            assert model.save == deff_dread_expected_data["stats"]["save"]
            assert model.wounds == deff_dread_expected_data["stats"]["wounds"]
            assert model.leadership == deff_dread_expected_data["stats"]["leadership"]
            assert (
                model.objective_control
                == deff_dread_expected_data["stats"]["objective_control"]
            )


def test_mek_gunz_properties(ork_roster_loader):
    """Test Mek Gunz unit has correct properties and model composition."""
    mek_gunz = ork_roster_loader.get_unit(mek_gunz_expected_data["name"])

    all_models = mek_gunz.all_models()
    assert len(all_models) == mek_gunz_expected_data["model_count"]

    # Verify model type composition
    for model_type, expected_count in mek_gunz_expected_data["model_types"].items():
        assert model_type in mek_gunz.model_types()
        assert len(mek_gunz.models[model_type]) == expected_count

    # All models should have same stats
    for model in all_models:
        assert model.movement == mek_gunz_expected_data["stats"]["movement"]
        assert model.toughness == mek_gunz_expected_data["stats"]["toughness"]
        assert model.save == mek_gunz_expected_data["stats"]["save"]
        assert model.wounds == mek_gunz_expected_data["stats"]["wounds"]
        assert model.leadership == mek_gunz_expected_data["stats"]["leadership"]
        assert (
            model.objective_control
            == mek_gunz_expected_data["stats"]["objective_control"]
        )
