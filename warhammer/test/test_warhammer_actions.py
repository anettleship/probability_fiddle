import pytest

from ..warhammer_actions import MeleeAttack, RangedAttack


def test_ranged_attack_action_properties(space_marine, necron_warrior, bolter):
    attack_action = RangedAttack(
        attacker=space_marine, target=necron_warrior, weapon=bolter
    )
    assert attack_action.attacker == space_marine, (
        "Attacker should be the unit that performs the attack"
    )
    assert attack_action.target == necron_warrior, (
        "Target should be the unit that is being attacked"
    )
    assert attack_action.weapon == bolter, (
        "Weapon should be the weapon used in the attack"
    )


def test_melee_attack_action_properties(space_marine, necron_warrior, chainsword):
    attack_action = MeleeAttack(
        attacker=space_marine, target=necron_warrior, weapon=chainsword
    )
    assert attack_action.attacker == space_marine, (
        "Attacker should be the unit that performs the attack"
    )
    assert attack_action.target == necron_warrior, (
        "Target should be the unit that is being attacked"
    )
    assert attack_action.weapon == chainsword, (
        "Weapon should be the weapon used in the attack"
    )


def test_ranged_attack_hit_probability_should_be_correct_for_space_marine(
    space_marine, necron_warrior, bolter
):
    attack_action = RangedAttack(
        attacker=space_marine, target=necron_warrior, weapon=bolter
    )
    expected_hit_probability = 2 / 3  # 3+ to hit on a D6
    assert attack_action.probability_to_hit() == expected_hit_probability, (
        "Ranged attack hit probability should be correct based on ballistic skill"
    )


def test_melee_attack_hit_probability_should_be_correct_for_space_marine(
    space_marine, necron_warrior, chainsword
):
    attack_action = MeleeAttack(
        attacker=space_marine, target=necron_warrior, weapon=chainsword
    )
    expected_hit_probability = 2 / 3  # 3+ to hit on a D6
    assert attack_action.probability_to_hit() == expected_hit_probability, (
        "Melee attack hit probability should be correct based on weapon skill"
    )


def test_ranged_attack_wound_probability_should_be_correct_for_space_marine(
    space_marine, necron_warrior, bolter
):
    attack_action = RangedAttack(
        attacker=space_marine, target=necron_warrior, weapon=bolter
    )
    expected_wound_probability = (
        1 / 2
    )  # 4+ to wound on a D6 when Strength equals Toughness
    assert attack_action.probability_to_wound() == expected_wound_probability, (
        "Ranged attack wound probability should be correct based on strength vs toughness"
    )


def test_melee_attack_wound_probability_should_be_correct_for_space_marine(
    space_marine, necron_warrior, chainsword
):
    attack_action = MeleeAttack(
        attacker=space_marine, target=necron_warrior, weapon=chainsword
    )
    expected_wound_probability = (
        1 / 2
    )  # 4+ to wound on a D6 when Strength equals Toughness
    assert attack_action.probability_to_wound() == expected_wound_probability, (
        "Melee attack wound probability should be correct based on strength vs toughness"
    )


def test_armour_save_probabily_without_benefit_of_cover_for_space_marine_on_necron(
    space_marine, necron_warrior, bolter
):
    attack_action = RangedAttack(
        attacker=space_marine, target=necron_warrior, weapon=bolter
    )
    expected_probabilty_to_fail_save = (
        2 / 3
    )  # 5+ armour save on a D6 for a Necron Warrior with 4+ save and -1 AP is 2/3 chance to fail

    assert (
        attack_action.probability_to_fail_save() == expected_probabilty_to_fail_save
    ), (
        "Ranged attack armour save probability should be correct based on target's save and weapon's AP"
    )


def test_armour_save_for_melee_attack_does_not_apply_benefit_of_cover(
    space_marine, necron_warrior, chainsword
):
    attack_action = MeleeAttack(
        attacker=space_marine,
        target=necron_warrior,
        weapon=chainsword,
        benefit_of_cover=True,
    )
    expected_probabilty_to_fail_save = (
        2 / 3
    )  # 5+ armour save on a D6 for a Necron Warrior with 4+ save and -1 AP is 2/3 chance to fail

    assert (
        attack_action.probability_to_fail_save() == expected_probabilty_to_fail_save
    ), (
        "Melee attack armour save probability should be correct based on target's save and weapon's AP without benefit of cover"
    )


def test_armour_save_probabily_with_benefit_of_cover_for_space_marine_on_necron(
    space_marine, necron_warrior, bolter
):
    attack_action = RangedAttack(
        attacker=space_marine,
        target=necron_warrior,
        weapon=bolter,
        benefit_of_cover=True,
    )
    expected_probabilty_to_fail_save = (
        1 / 2
    )  # 4+ armour save on a D6 for a Necron Warrior with 4+ save and -1 AP but +1 benefit of cover is 1/2 chance to fail

    assert (
        attack_action.probability_to_fail_save() == expected_probabilty_to_fail_save
    ), (
        "Ranged attack armour save probability should be correct based on target's save and weapon's AP"
    )


def test_armour_save_probabily_with_benefit_of_cover_for_necron_on_space_marine_does_not_go_below_3_plus(
    space_marine, necron_warrior, gauss_flayer
):
    attack_action = RangedAttack(
        attacker=necron_warrior,
        target=space_marine,
        weapon=gauss_flayer,
        benefit_of_cover=True,
    )
    expected_probabilty_to_fail_save = (
        1 / 3
    )  # 3+ armour save on a D6 for a Space Marine with 3+ save and 0 AP but +1 benefit of cover is still 1/3 chance to fail because benefit of cover cannot reduce save below a 3+

    assert (
        attack_action.probability_to_fail_save() == expected_probabilty_to_fail_save
    ), (
        "Ranged attack armour save probability should be correct based on target's save and weapon's AP"
    )


def test_armour_save_probabily_does_not_exceed_impossible_save(
    space_marine, necron_warrior, lascannon
):
    attack_action = RangedAttack(
        attacker=space_marine, target=necron_warrior, weapon=lascannon
    )
    expected_probabilty_to_fail_save = 1  # 7+ armour save on a D6 for a Necron Warrior with 4+ save and -3 AP is 1.0 chance to fail because save cannot exceed impossible save

    assert (
        attack_action.probability_to_fail_save() == expected_probabilty_to_fail_save
    ), (
        "Ranged attack armour save probability should be correct based on target's save and weapon's AP"
    )


def test_armour_save_probabily_invulnerable_save_overrides_normal_save(
    space_marine, terminator_with_storm_bolter, lascannon
):
    attack_action = RangedAttack(
        attacker=space_marine, target=terminator_with_storm_bolter, weapon=lascannon
    )
    expected_probabilty_to_fail_save = (
        1 / 2
    )  # 4+ invulnerable save on a D6 for a Terminator when hit with a lascannon with -3 AP is better than modified save of 5+

    assert (
        attack_action.probability_to_fail_save() == expected_probabilty_to_fail_save
    ), (
        "Ranged attack armour save probability should use invulnerable save when it is better than normal save"
    )


@pytest.mark.parametrize(
    "attacker_fixture,target_fixture,weapon_fixture,expected_hit,expected_wound,expected_fail_save",
    [
        (
            "space_marine",
            "necron_warrior",
            "bolter",
            2 / 3,
            1 / 2,
            2 / 3,
        ),  # Space Marine with bolter vs Necron
        (
            "necron_warrior",
            "terminator_with_heavy_flamer",
            "gauss_flayer",
            1 / 2,
            1 / 3,
            1 / 6,
        ),  # Necron with gauss flayer vs Terminator (uses invuln save)
        (
            "terminator_with_heavy_flamer",
            "necron_warrior",
            "heavy_flamer",
            1,
            2 / 3,
            2 / 3,
        ),  # Terminator with heavy flamer vs Necron (auto-hit, 5+ save = 4/6 fail)
    ],
)
def test_attack_action_with_to_hit_to_wound_and_save_without_benefit_of_cover_meet_expected_values(
    request,
    attacker_fixture,
    target_fixture,
    weapon_fixture,
    expected_hit,
    expected_wound,
    expected_fail_save,
):
    attacker = request.getfixturevalue(attacker_fixture)
    target = request.getfixturevalue(target_fixture)
    weapon = request.getfixturevalue(weapon_fixture)

    attack_action = RangedAttack(
        attacker=attacker, target=target, weapon=weapon, benefit_of_cover=False
    )

    assert attack_action.probability_to_hit() == expected_hit, (
        "Ranged attack hit probability should be correct based on ballistic skill"
    )

    assert attack_action.probability_to_wound() == expected_wound, (
        "Ranged attack wound probability should be correct based on strength vs toughness"
    )

    assert attack_action.probability_to_fail_save() == expected_fail_save, (
        "Ranged attack armour save probability should be correct based on target's save and weapon's AP"
    )
    assert (
        attack_action.probability_to_damage()
        == expected_hit * expected_wound * expected_fail_save
    )


@pytest.mark.parametrize(
    "attacker_fixture,target_fixture,weapon_fixture,expected_hit,expected_wound,expected_fail_save",
    [
        (
            "space_marine",
            "necron_warrior",
            "bolter",
            2 / 3,
            1 / 2,
            1 / 2,
        ),  # Space Marine with bolter vs Necron
        (
            "necron_warrior",
            "terminator_with_heavy_flamer",
            "gauss_flayer",
            1 / 2,
            1 / 3,
            1 / 6,
        ),  # Necron with gauss flayer vs Terminator
        (
            "terminator_with_heavy_flamer",
            "necron_warrior",
            "heavy_flamer",
            1,
            2 / 3,
            2 / 3,
        ),  # Terminator with heavy flamer vs Necron (auto-hit, 5+ save = 4/6 fail) - benefit of cover has no effect for ignores cover weapon
    ],
)
def test_attack_action_with_to_hit_to_wound_and_save_with_benefit_of_cover_meet_expected_values(
    request,
    attacker_fixture,
    target_fixture,
    weapon_fixture,
    expected_hit,
    expected_wound,
    expected_fail_save,
):
    attacker = request.getfixturevalue(attacker_fixture)
    target = request.getfixturevalue(target_fixture)
    weapon = request.getfixturevalue(weapon_fixture)

    attack_action = RangedAttack(
        attacker=attacker, target=target, weapon=weapon, benefit_of_cover=True
    )

    assert attack_action.probability_to_hit() == expected_hit, (
        "Ranged attack hit probability should be correct based on ballistic skill"
    )

    assert attack_action.probability_to_wound() == expected_wound, (
        "Ranged attack wound probability should be correct based on strength vs toughness"
    )

    assert attack_action.probability_to_fail_save() == expected_fail_save, (
        "Ranged attack armour save probability should be correct based on target's save and weapon's AP with benefit of cover"
    )
    assert (
        attack_action.probability_to_damage()
        == expected_hit * expected_wound * expected_fail_save
    )


def test_weapon_with_lethal_hits_keyword_auto_wounds_on_critical_hit(
    space_marine, tough_target, lethal_hits_weapon
):
    attack = RangedAttack(
        attacker=space_marine, target=tough_target, weapon=lethal_hits_weapon
    )

    # Lethal Hits: Critical hit rolls (unmodified 6s) auto-wound
    #
    # Hit roll breakdown (BS 3+ means hit on 3,4,5,6):
    # - Critical hits: roll 6 to hit (1/6 probability)
    # - Normal hits: roll 3,4,5 to hit (3/6 probability)
    # - Misses: roll 1,2 (2/6 probability)
    #
    # Wound roll (S4 vs T8 = need 6+ to wound):
    # - Without Lethal Hits: ALL hits need 6+ to wound (1/6 probability)
    # - With Lethal Hits: Critical hits skip wound roll (auto-wound)
    #
    # Probability to wound calculation:
    # - Critical hits (1/6) → auto-wound (100%) = 1/6
    # - Normal hits (3/6) → must roll to wound (1/6) = 3/6 × 1/6 = 1/12
    # - Total probability to wound = 1/6 + 1/12 = 3/12 = 1/4

    expected_wound_probability = 1 / 4

    assert attack.probability_to_wound() == expected_wound_probability, (
        "Lethal Hits weapon should auto-wound on critical hits (unmodified 6s)"
    )
