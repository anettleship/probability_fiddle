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
    expected_hit_probability = 1 / 2  # 4+ to hit on a D6
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


def test_armour_save_probabily_with_benefit_of_cover_for_space_marine_on_necron(
    space_marine, necron_warrior, bolter
):
    attack_action = RangedAttack(
        attacker=space_marine, target=necron_warrior, weapon=bolter
    )
    expected_probabilty_to_fail_save = (
        1 / 2
    )  # 4+ armour save on a D6 for a Necron Warrior with 4+ save and -1 AP but +1 benefit of cover is 1/2 chance to fail

    assert (
        attack_action.probability_to_fail_save(benefit_of_cover=True)
        == expected_probabilty_to_fail_save
    ), (
        "Ranged attack armour save probability should be correct based on target's save and weapon's AP"
    )


def test_armour_save_probabily_with_benefit_of_cover_for_necron_on_space_marine_does_not_go_below_3_plus(
    space_marine, necron_warrior, gauss_flayer
):
    attack_action = RangedAttack(
        attacker=necron_warrior, target=space_marine, weapon=gauss_flayer
    )
    expected_probabilty_to_fail_save = (
        1 / 3
    )  # 3+ armour save on a D6 for a Space Marine with 3+ save and 0 AP but +1 benefit of cover is still 1/3 chance to fail because benefit of cover cannot reduce save below a 3+

    assert (
        attack_action.probability_to_fail_save(benefit_of_cover=True)
        == expected_probabilty_to_fail_save
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
        attack_action.probability_to_fail_save(benefit_of_cover=False)
        == expected_probabilty_to_fail_save
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
        attack_action.probability_to_fail_save(benefit_of_cover=False)
        == expected_probabilty_to_fail_save
    ), (
        "Ranged attack armour save probability should use invulnerable save when it is better than normal save"
    )
