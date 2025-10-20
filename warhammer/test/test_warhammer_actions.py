from ..warhammer_actions import RangedAttack, MeleeAttack
from ..warhammer import Unit, RangedWeapon, MeleeWeapon

def test_ranged_attack_action_properties():

    attacker = Unit(name="Space Marine", movement=6, toughness=4, save=3, wounds=2, leadership=8, objective_control=1)
    target = Unit(name="Necron Warrior", movement=5, toughness=4, save=4, wounds=1, leadership=7, objective_control=2)
    ranged_weapon = RangedWeapon(name="Bolter", range=24, attacks=1, ballistic_skill=4, strength=4, armour_penetration=-1, damage=1, bearer=attacker)
    attack_action = RangedAttack(attacker=attacker, target=target, weapon=ranged_weapon) 
    assert attack_action.attacker == attacker, "Attacker should be the unit that performs the attack"
    assert attack_action.target == target, "Target should be the unit that is being attacked"
    assert attack_action.weapon == ranged_weapon, "Weapon should be the weapon used in the attack"

def test_melee_attack_action_properties():

    attacker = Unit(name="Space Marine", movement=6, toughness=4, save=3, wounds=2, leadership=8, objective_control=1)
    target= Unit(name="Necron Warrior", movement=5, toughness=4, save=4, wounds=1, leadership=7, objective_control=2)
    melee_weapon = MeleeWeapon(name="Chainsword", attacks=2, weapon_skill=3, strength=4, armour_penetration=-1, damage=1, bearer=attacker)
    attack_action = MeleeAttack(attacker=attacker, target=target, weapon=melee_weapon) 
    assert attack_action.attacker == attacker, "Attacker should be the unit that performs the attack"
    assert attack_action.target == target, "Target should be the unit that is being attacked"
    assert attack_action.weapon == melee_weapon, "Weapon should be the weapon used in the attack"

def test_ranged_attack_hit_probability():

    pass