import json

from .warhammer import Model, Unit


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
        for profile in profiles:
            if profile.get("typeName") == "Unit":
                model_profile = profile
                break

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

        model_selections = unit_selection.get("selections", [])

        for model_sel in model_selections:
            if model_sel.get("type") == "model":
                model_count = model_sel.get("number", 1)

                # Get model profile
                model_profiles = model_sel.get("profiles", [])
                model_profile = None
                for profile in model_profiles:
                    if profile.get("typeName") == "Unit":
                        model_profile = profile
                        break

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
                        )
                        models.append(model)

        return models
