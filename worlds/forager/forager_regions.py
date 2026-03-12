from typing import TYPE_CHECKING, NamedTuple

from BaseClasses import Region, Entrance, CollectionState

if TYPE_CHECKING:
    from worlds.forager import ForagerWorld


class ForagerRegionData(NamedTuple):
    """Gives the flexibility to add multiple types of region requirements in the future, such as required gold, xp, etc."""
    parent_region: str
    items_required: list[str] = None


# Defines the region and any access related requirements
region_access: dict[str, ForagerRegionData] = {
    "Steel": ForagerRegionData("Menu", ["Industry"]),
    "Royal Steel": ForagerRegionData("Steel", ["Craftmanship","Prospecting"]),
    "Electronics": ForagerRegionData("Royal Steel", ["Manufacturing"]),
    "Void Steel": ForagerRegionData("Electronics", ["Foraging", "Sewing", "Summoning", "Transmutation", "Spirituality"]),
    "Cosmic Steel": ForagerRegionData("Void Steel", ["Astrology"]),
    "Nuclear": ForagerRegionData("Void Steel", ["Physics"]),
}

def load_regions(world: "ForagerWorld"):
    region_list: list[str] = list(world.json_tables["regions"]) + list(world.json_tables["itemslands"]["Lands"].keys())
    for region_name in region_list:
        world.multiworld.regions.append(Region(region_name, world.player, world.multiworld))

    if world.options.game_mode.value == world.options.game_mode.option_default:
        # TODO create logical groups for locations based on group A up to X xp, then do some other groups.
        #   Formulas to calculate xp per region to follow in rules.py
        pass


def create_locations(world: "ForagerWorld"):
    # TODO start moving locations into their logical regions. Create locked items for each land, rules to follow later.
    pass