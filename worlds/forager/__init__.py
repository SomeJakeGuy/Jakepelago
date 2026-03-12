from typing import ClassVar

from worlds.AutoWorld import World
from worlds.LauncherComponents import Component, components, icon_paths, launch as launch_component, Type
from BaseClasses import ItemClassification as IClass, Item

from .forager_constants import GAME_NAME, CLIENT_NAME
from .forager_rules import create_region_access_rules
from .forager_webworld import ForagerWebWorld
from .helper_functions import load_tables, load_json_tables
from .forager_regions import load_regions
from .forager_options import ForagerOptions


# Define the client launch state function and add it to the AP Launcher
def launch_client():
    from .Client import launch
    launch_component(launch, name=CLIENT_NAME)
components.append(Component(CLIENT_NAME, func=launch_client, component_type=Type.CLIENT))


class ForagerWorld(World):
    game = GAME_NAME
    item_name_to_id: ClassVar[dict[str, int]]
    location_name_to_id: ClassVar[dict[str, int]]
    json_tables: dict[str, dict] = load_json_tables()

    item_name_to_id, item_name_groups, location_name_to_id, location_name_groups = (
        load_tables(json_tables["items"], json_tables["locations"]))

    options: ForagerOptions
    options_dataclass = ForagerOptions

    web = ForagerWebWorld()
    required_level_count: int

    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)
        self.required_level_count = 0

    def generate_early(self) -> None:
        """Used for evaluating any OptionErrors we see fit, updating some option values based on invalid combos, etc."""
        if self.options.game_mode.value == self.options.game_mode.option_default:
            self.required_level_count = 65


    def create_regions(self):
        """Loads both the regions and the locations"""
        load_regions(self)


    def create_rules(self):
        """Attach the various rules for both locations and regions"""
        # TODO make location rules as well.
        create_region_access_rules(self)


    def create_items(self):
        """Creates the various items required based on the user's options"""
        item_pool: list[Item] = []

        for category_name, category in self.json_tables["items"].items():
            if category_name == "Misc":
                continue

            for item_name, item_id in category.items():
                if category_name == "Tools":
                    for tool_count in range(item_id["count"]):
                        item_pool.append(Item(item_name, IClass.progression, item_id["id"], self.player))
                else:
                    item_pool.append(Item(item_name, IClass.progression, item_id, self.player))

        # Calculate the number of progression items required vs the number of unfilled locations left.
        # Create that many of filler items remaining.
        locations_left_to_fill: int = len(self.multiworld.get_unfilled_locations(self.player)) - len(item_pool)
        for loc_to_fill in range(locations_left_to_fill):
            # Pick a random filler item and add that to the item pool
            random_filler: str = self.random.choice(list(self.json_tables["items"]["Misc"].keys()))
            item_pool.append(Item(random_filler, IClass.filler,
                self.json_tables["items"]["Misc"][random_filler], self.player))

        self.multiworld.itempool += item_pool


    def create_item(self, name):
        # TODO get the item from item categories and see if its not in Misc. If not misc, progression for now, else filler.
        pass
        #return ForagerItem(name, IClass.progression, self.item_name_to_id[name],
        #                   self.player)  # Needs to have item classifications done