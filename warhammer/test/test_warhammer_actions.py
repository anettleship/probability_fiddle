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


def test_attack_wound_probability_should_be_correct_for_space_marine(
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
