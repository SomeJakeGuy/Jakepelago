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