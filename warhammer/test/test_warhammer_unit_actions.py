def test_unit_can_shoot_single_weapon_type_at_target(
    terminator_with_storm_bolter, necron_warrior_unit
):
    # Single terminator model wrapped in unit shoots at necron warrior unit
    # Storm Bolter: 2 attacks, BS 3+, S4, AP0, D1
    # Expected: attacks × P(hit) × P(wound) × P(fail_save) × damage
    # = 2 × (2/3) × (1/2) × (1/2) × 1 = 1/3

    from warhammer import Unit

    single_terminator_unit = Unit(
        models=[terminator_with_storm_bolter], name="Single Terminator"
    )

    results = single_terminator_unit.shoot_at(necron_warrior_unit)

    assert len(results.weapon_results) == 1
    assert results.weapon_results[0].weapon_name == "Storm Bolter"
    assert abs(results.total_expected_damage - (1 / 3)) < 0.001


def test_unit_ranged_attacked_probabilities_match_expected(
    necron_warrior_unit, terminator_unit
):
    # TODO NEXT STEP Check that this test is actually True!

    # Terminator unit composition:
    # - 1 Sergeant with Storm Bolter (2 attacks, S4, AP0, D1)
    # - 3 Terminators with Storm Bolters (2 attacks each = 6 total, S4, AP0, D1)
    # - 1 Terminator with Heavy Flamer (D6 attacks = 6 in fixture, S5, AP-1, D1, Auto-hit, Ignores Cover)
    #
    # Expected shooting order (most powerful first):
    # 1. Heavy Flamer: 6 attacks (D6), S5, AP-1, D1
    # 2. Storm Bolters: 8 attacks total (4 models × 2), S4, AP0, D1
    #
    # Expected damage calculation per weapon accounts for number of attacks:
    # expected_damage = attacks × P(hit) × P(wound) × P(fail_save) × damage

    # Execute unit ranged attack
    results = terminator_unit.shoot_at(necron_warrior_unit)

    # Verify results structure
    assert hasattr(results, "weapon_results"), "Results should have weapon_results"
    assert len(results.weapon_results) == 2, "Should have 2 weapon types fired"

    # Heavy Flamer should be first (higher strength, better AP)
    heavy_flamer_result = results.weapon_results[0]
    assert heavy_flamer_result.weapon_name == "Heavy Flamer"
    assert heavy_flamer_result.attacks == 6
    assert heavy_flamer_result.expected_hits > 0
    assert heavy_flamer_result.expected_wounds > 0
    assert heavy_flamer_result.expected_damage > 0

    # Storm Bolters should be second
    storm_bolter_result = results.weapon_results[1]
    assert storm_bolter_result.weapon_name == "Storm Bolter"
    assert storm_bolter_result.attacks == 8  # 4 models with 2 attacks each
    assert storm_bolter_result.expected_hits > 0
    assert storm_bolter_result.expected_wounds > 0
    assert storm_bolter_result.expected_damage > 0

    # Verify total expected damage
    total_expected_damage = sum(wr.expected_damage for wr in results.weapon_results)
    assert total_expected_damage > 0
    assert hasattr(results, "total_expected_damage")
    assert results.total_expected_damage == total_expected_damage
