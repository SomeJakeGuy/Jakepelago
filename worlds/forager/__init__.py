from typing import ClassVar

from worlds.AutoWorld import World
from worlds.LauncherComponents import Component, components, icon_paths, launch as launch_component, Type

from .forager_constants import GAME_NAME, CLIENT_NAME
from .forager_items import create_world_items
from .forager_rules import create_region_access_rules
from .forager_webworld import ForagerWebWorld
from .helper_functions import load_tables, load_json_tables
from .forager_regions import load_regions, create_locations
from .forager_options import ForagerOptions


# Define the client launch state function and add it to the AP Launcher
def launch_client():
    from .Client import launch
    launch_component(launch, name=CLIENT_NAME)
components.append(Component(CLIENT_NAME, func=launch_client, component_type=Type.CLIENT))


class ForagerWorld(World):
    game = GAME_NAME
    item_name_to_id: ClassVar[dict[str, int]]
    item_name_groups: ClassVar[dict[str, set[str]]]
    item_class_sets: ClassVar[dict[str, dict[str, str]]]

    location_name_to_id: ClassVar[dict[str, int]]
    location_name_groups: ClassVar[dict[str, set[str]]]
    json_tables: dict[str, dict] = load_json_tables()

    item_name_to_id, item_name_groups, item_class_sets, location_name_to_id, location_name_groups = (
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
        create_locations(self)


    def create_rules(self):
        """Attach the various rules for both locations and regions"""
        # TODO make location rules as well.
        create_region_access_rules(self)


    def create_items(self):
        """Creates the various items required based on the user's options"""
        create_world_items(self)

    def generate_basic(self) -> None:
        print("")


    def create_item(self, name):
        # TODO get the item from item categories and see if its not in Misc. If not misc, progression for now, else filler.
        pass
        #return ForagerItem(name, IClass.progression, self.item_name_to_id[name],
        #                   self.player)  # Needs to have item classifications done