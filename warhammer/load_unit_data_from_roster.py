import json

from .warhammer import MeleeWeapon, Model, RangedWeapon, Unit


class LoadUnitDataFromRoster:
    def __init__(self, datasource):
        self.datasource = datasource
        self.units = {}  # Dict with unique keys for easy lookup
        self._unit_name_counters = {}  # Track duplicate names
        self._load_roster()

    def get_unit(self, name):
        """Get a unit by name. Returns first unit with matching name."""
        for key, unit in self.units.items():
            if unit.name == name:
                return unit
        return None

    def get_units_by_name(self, name):
        """Get all units with matching name (useful for duplicates like Deff Dreads)."""
        return [unit for unit in self.units.values() if unit.name == name]

    def _generate_unique_key(self, unit_name):
        """Generate unique key for unit, handling duplicates."""
        if unit_name not in self._unit_name_counters:
            self._unit_name_counters[unit_name] = 0
            return unit_name
        else:
            self._unit_name_counters[unit_name] += 1
            return f"{unit_name}_{self._unit_name_counters[unit_name]}"

    def _load_roster(self):
        """Load and parse the roster JSON file."""
        with open(self.datasource, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Navigate the roster structure
        roster = data.get("roster", {})
        forces = roster.get("forces", [])

        if not forces:
            return

        # Process first force
        force = forces[0]
        selections = force.get("selections", [])

        # Find unit selections (type="unit")
        for selection in selections:
            if selection.get("type") == "model":
                self._process_model(selection)
            if selection.get("type") == "unit":
                self._process_unit(selection)

    def _process_model(self, selection):
        """Used for processing characters who appear separately to a unit"""
        model_name = selection.get("name")

        profiles = selection.get("profiles", [])
        model_profile = None
        invulnerable_save = None

        for profile in profiles:
            if profile.get("typeName") == "Unit":
                model_profile = profile
            elif (
                profile.get("typeName") == "Abilities"
                and profile.get("name") == "Invulnerable Save"
            ):
                chars = profile.get("characteristics", [])
                if chars:
                    inv_text = chars[0].get("$text", "")
                    invulnerable_save = int(inv_text.replace("+", ""))

        # Extract weapons
        ranged_weapons, melee_weapons = self._extract_weapons(selection)

        models = []
        if model_profile:
            chars = model_profile.get("characteristics", [])
            characteristics = {c["name"]: c["$text"] for c in chars}

            # Create single model from characteristics
            model = Model(
                name=model_name,
                movement=int(characteristics.get("M", "0").replace('"', "")),
                toughness=int(characteristics.get("T", "0")),
                save=int(characteristics.get("SV", "0").replace("+", "")),
                wounds=int(characteristics.get("W", "0")),
                leadership=int(characteristics.get("LD", "0").replace("+", "")),
                objective_control=int(characteristics.get("OC", "0")),
                invulnerable_save=invulnerable_save,
                ranged_weapons=ranged_weapons,
                melee_weapons=melee_weapons,
            )
            models.append(model)

        # Create Unit (even though it's a single character model)
        unit = Unit(models=models, name=model_name)
        unique_key = self._generate_unique_key(model_name)
        self.units[unique_key] = unit

    def _process_unit(self, unit_selection):
        """Process a unit selection and create Unit with Models."""
        unit_name = unit_selection.get("name")

        # Extract model selections within the unit
        models = self._extract_models(unit_selection)

        # Create Unit
        unit = Unit(models=models, name=unit_name)
        unique_key = self._generate_unique_key(unit_name)
        self.units[unique_key] = unit

    def _extract_models(self, unit_selection):
        # Extract model selections within the unit
        models = []
        if unit_selection is None:
            return models

        # Check for unit-level invulnerable save
        unit_invulnerable_save = None
        unit_profiles = unit_selection.get("profiles", [])
        for profile in unit_profiles:
            if (
                profile.get("typeName") == "Abilities"
                and profile.get("name") == "Invulnerable Save"
            ):
                chars = profile.get("characteristics", [])
                if chars:
                    inv_text = chars[0].get("$text", "")
                    unit_invulnerable_save = int(inv_text.replace("+", ""))

        model_selections = unit_selection.get("selections", [])

        for model_sel in model_selections:
            if model_sel.get("type") == "model":
                model_count = model_sel.get("number", 1)

                # Get model profile and invulnerable save
                model_profiles = model_sel.get("profiles", [])
                model_profile = None
                model_invulnerable_save = (
                    unit_invulnerable_save  # Default to unit-level
                )

                for profile in model_profiles:
                    if profile.get("typeName") == "Unit":
                        model_profile = profile
                    elif (
                        profile.get("typeName") == "Abilities"
                        and profile.get("name") == "Invulnerable Save"
                    ):
                        chars = profile.get("characteristics", [])
                        if chars:
                            inv_text = chars[0].get("$text", "")
                            model_invulnerable_save = int(inv_text.replace("+", ""))

                # Extract weapons for this model
                ranged_weapons, melee_weapons = self._extract_weapons(model_sel)

                if model_profile:
                    chars = model_profile.get("characteristics", [])
                    characteristics = {c["name"]: c["$text"] for c in chars}

                    # Create models based on count
                    for _ in range(model_count):
                        model = Model(
                            name=model_sel.get("name"),
                            movement=int(
                                characteristics.get("M", "0").replace('"', "")
                            ),
                            toughness=int(characteristics.get("T", "0")),
                            save=int(characteristics.get("SV", "0").replace("+", "")),
                            wounds=int(characteristics.get("W", "0")),
                            leadership=int(
                                characteristics.get("LD", "0").replace("+", "")
                            ),
                            objective_control=int(characteristics.get("OC", "0")),
                            invulnerable_save=model_invulnerable_save,
                            ranged_weapons=ranged_weapons,
                            melee_weapons=melee_weapons,
                        )
                        models.append(model)

        return models

    def _extract_weapons(self, selection):
        """Extract weapons from a selection (model or unit)."""
        ranged_weapons = {}
        melee_weapons = {}

        # Look through selections for weapon upgrades
        selections = selection.get("selections", [])
        for sel in selections:
            if sel.get("type") == "upgrade":
                # Check profiles for weapon data
                profiles = sel.get("profiles", [])
                for profile in profiles:
                    weapon_type = profile.get("typeName")
                    if weapon_type in ["Ranged Weapons", "Melee Weapons"]:
                        weapon_name = profile.get("name")
                        chars = profile.get("characteristics", [])
                        characteristics = {c["name"]: c["$text"] for c in chars}

                        # Extract keywords and convert to list
                        keywords_str = characteristics.get("Keywords", "")
                        keywords = [
                            k.strip()
                            for k in keywords_str.split(",")
                            if k.strip() and k.strip() != "-"
                        ]

                        if weapon_type == "Ranged Weapons":
                            bs_value = characteristics.get("BS", "0")
                            # Handle N/A for auto-hit weapons
                            ballistic_skill = (
                                0
                                if bs_value == "N/A"
                                else int(bs_value.replace("+", ""))
                            )

                            weapon = RangedWeapon(
                                name=weapon_name,
                                range=int(
                                    characteristics.get("Range", "0").replace('"', "")
                                ),
                                attacks=self._parse_attacks(
                                    characteristics.get("A", "1")
                                ),
                                ballistic_skill=ballistic_skill,
                                strength=int(characteristics.get("S", "0")),
                                armour_penetration=int(characteristics.get("AP", "0")),
                                damage=self._parse_attacks(
                                    characteristics.get("D", "1")
                                ),
                                keywords=keywords,
                            )
                            ranged_weapons[weapon_name] = weapon
                        elif weapon_type == "Melee Weapons":
                            weapon = MeleeWeapon(
                                name=weapon_name,
                                attacks=self._parse_attacks(
                                    characteristics.get("A", "1")
                                ),
                                weapon_skill=int(
                                    characteristics.get("WS", "0").replace("+", "")
                                ),
                                strength=int(characteristics.get("S", "0")),
                                armour_penetration=int(characteristics.get("AP", "0")),
                                damage=self._parse_attacks(
                                    characteristics.get("D", "1")
                                ),
                                keywords=keywords,
                            )
                            melee_weapons[weapon_name] = weapon

        return ranged_weapons, melee_weapons

    def _parse_attacks(self, attacks_str):
        """Parse attacks value (handle D6, 2D6, etc.)."""
        # For now, return simple integer or average for dice
        if "D6" in attacks_str.upper():
            return 3  # Average of D6
        if "D3" in attacks_str.upper():
            return 2  # Average of D3
        try:
            return int(attacks_str)
        except ValueError:
            return 1  # Default
