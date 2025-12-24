from __future__ import annotations

import re

from .constants import WeaponAttribute


class Model:
    def __init__(
        self,
        name: str,
        movement: int,
        toughness: int,
        save: int,
        wounds: int,
        leadership: int,
        objective_control: int,
        invulnerable_save: int | None = None,
        feel_no_pain: int | None = None,
        ranged_weapons: dict | None = None,
        melee_weapons: dict | None = None,
    ) -> None:
        self.name = name
        self.movement = movement
        self.toughness = toughness
        self.save = save
        self.wounds = wounds
        self.health = wounds
        self.leadership = leadership
        self.objective_control = objective_control
        self.invulnerable_save = invulnerable_save
        self.feel_no_pain = feel_no_pain
        setattr(self, WeaponAttribute.RANGED.value, ranged_weapons if ranged_weapons is not None else {})
        setattr(self, WeaponAttribute.MELEE.value, melee_weapons if melee_weapons is not None else {})

    def is_alive(self) -> bool:
        return self.health > 0

    def health(self) -> int:
        return self.health


class Weapon:
    def __init__(
        self,
        name: str,
        attacks: int | str,
        strength: int,
        armour_penetration: int,
        damage: int | str,
        keywords: list[str] | None = None,
    ) -> None:
        self.name = name
        self.attacks = attacks
        self.strength = strength
        self.armour_penetration = armour_penetration
        self.damage = damage
        self.keywords = keywords if keywords is not None else []
    
    @staticmethod
    def parse_attacks_average(attacks: int | str) -> float:
        """Parse attacks notation and return the average expected number of attacks.
        
        Handles:
        - Fixed integers: 3 -> 3.0
        - D6: "D6" -> 3.5
        - D3: "D3" -> 2.0
        - Multiple dice: "2D6" -> 7.0
        """
        if isinstance(attacks, int):
            return float(attacks)
        
        if isinstance(attacks, str):
            # Handle pure integer strings
            if attacks.isdigit():
                return float(attacks)
            
            # Parse D6 notation
            pattern_d6 = r'^(\d*)D6$'
            match = re.match(pattern_d6, attacks, re.IGNORECASE)
            if match:
                num_dice = int(match.group(1)) if match.group(1) else 1
                return num_dice * 3.5
            
            # Parse D3 notation
            pattern_d3 = r'^(\d*)D3$'
            match = re.match(pattern_d3, attacks, re.IGNORECASE)
            if match:
                num_dice = int(match.group(1)) if match.group(1) else 1
                return num_dice * 2.0
        
        # If we can't parse it, raise an error
        raise ValueError(f"Cannot parse attacks notation: {attacks}")
    
    def get_average_attacks(self) -> float:
        """Return the average number of attacks for this weapon."""
        return self.parse_attacks_average(self.attacks)
    
    @staticmethod
    def roll_attacks(attacks: int | str, dice_roller=None) -> int:
        """Roll for actual number of attacks.
        
        Args:
            attacks: The attacks value (int or dice notation string like "D6", "2D6", "D3")
            dice_roller: Optional DiceRoll instance for rolling dice
        
        Returns:
            The actual number of attacks rolled
        """
        if isinstance(attacks, int):
            return attacks
        
        if isinstance(attacks, str):
            # Handle pure integer strings
            if attacks.isdigit():
                return int(attacks)
            
            # Parse D6 notation
            pattern_d6 = r'^(\d*)D6$'
            match = re.match(pattern_d6, attacks, re.IGNORECASE)
            if match:
                if dice_roller is None:
                    raise ValueError("dice_roller required for variable attacks")
                num_dice = int(match.group(1)) if match.group(1) else 1
                total = sum(dice_roller.roll() for _ in range(num_dice))
                return total
            
            # Parse D3 notation
            pattern_d3 = r'^(\d*)D3$'
            match = re.match(pattern_d3, attacks, re.IGNORECASE)
            if match:
                if dice_roller is None:
                    raise ValueError("dice_roller required for variable attacks")
                num_dice = int(match.group(1)) if match.group(1) else 1
                # D3 is a D6 divided by 2 (rounded up): 1-2=1, 3-4=2, 5-6=3
                total = sum((dice_roller.roll() + 1) // 2 for _ in range(num_dice))
                return total
        
        # If we can't parse it, raise an error
        raise ValueError(f"Cannot parse attacks notation: {attacks}")
    
    @staticmethod
    def parse_damage_average(damage: int | str) -> float:
        """Parse damage notation and return the average expected damage.
        
        Handles:
        - Fixed integers: 3 -> 3.0
        - D6: "D6" -> 3.5
        - D6 with modifier: "D6+2" -> 5.5
        - Multiple dice: "2D6" -> 7.0
        - Complex: "2D6+3" -> 10.0
        """
        if isinstance(damage, int):
            return float(damage)
        
        if isinstance(damage, str):
            # Handle pure integer strings
            if damage.isdigit():
                return float(damage)
            
            # Parse dice notation: XD6+Y or D6+Y or XD6 or D6
            # Pattern: optional number, D6, optional +/- and number
            pattern = r'^(\d*)D6([+-]\d+)?$'
            match = re.match(pattern, damage, re.IGNORECASE)
            
            if match:
                num_dice = int(match.group(1)) if match.group(1) else 1
                modifier = int(match.group(2)) if match.group(2) else 0
                
                # Average of D6 is 3.5
                return (num_dice * 3.5) + modifier
        
        # If we can't parse it, raise an error
        raise ValueError(f"Cannot parse damage notation: {damage}")
    
    def get_average_damage(self) -> float:
        """Return the average damage for this weapon."""
        return self.parse_damage_average(self.damage)
    
    @staticmethod
    def roll_damage(damage: int | str, dice_roller=None) -> int:
        """Roll for actual damage value.
        
        Args:
            damage: The damage value (int or dice notation string)
            dice_roller: Optional DiceRoll instance for rolling dice
        
        Returns:
            The actual damage rolled
        """
        if isinstance(damage, int):
            return damage
        
        if isinstance(damage, str):
            # Handle pure integer strings
            if damage.isdigit():
                return int(damage)
            
            # Parse dice notation
            pattern = r'^(\d*)D6([+-]\d+)?$'
            match = re.match(pattern, damage, re.IGNORECASE)
            
            if match:
                num_dice = int(match.group(1)) if match.group(1) else 1
                modifier = int(match.group(2)) if match.group(2) else 0
                
                # Roll the dice
                if dice_roller is None:
                    from .probability_objects import DiceRoll
                    dice_roller = DiceRoll(sides=6)
                
                total = sum(dice_roller.roll() for _ in range(num_dice))
                return total + modifier
        
        raise ValueError(f"Cannot parse damage notation: {damage}")


class RangedWeapon(Weapon):
    def __init__(
        self,
        name: str,
        range: int,
        attacks: int,
        ballistic_skill: int,
        strength: int,
        armour_penetration: int,
        damage: int | str,
        keywords: list[str] | None = None,
    ) -> None:
        super().__init__(name, attacks, strength, armour_penetration, damage, keywords)
        self.range = range
        self.ballistic_skill = ballistic_skill


class MeleeWeapon(Weapon):
    def __init__(
        self,
        name: str,
        attacks: int,
        weapon_skill: int,
        strength: int,
        armour_penetration: int,
        damage: int | str,
        keywords: list[str] | None = None,
    ) -> None:
        super().__init__(name, attacks, strength, armour_penetration, damage, keywords)
        self.weapon_skill = weapon_skill
