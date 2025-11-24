import json

from .warhammer import Model, Unit


class LoadUnitDataFromRoster:
    def __init__(self, datasource):
        self.datasource = datasource
        self.units = {}
        self._load_roster()

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
            if selection.get("type") == "unit":
                self._process_unit(selection)

    def _process_unit(self, unit_selection):
        """Process a unit selection and create Unit with Models."""
        unit_name = unit_selection.get("name")

        # Get unit profile characteristics
        profiles = unit_selection.get("profiles", [])
        unit_profile = None
        for profile in profiles:
            if profile.get("typeName") == "Unit":
                unit_profile = profile
                break

        # Extract model selections within the unit
        model_selections = unit_selection.get("selections", [])
        models = []

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

        # Create Unit
        unit = Unit(models=models, name=unit_name)
        self.units[unit_name] = unit
