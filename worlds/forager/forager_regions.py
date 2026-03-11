from typing import TYPE_CHECKING, NamedTuple

from BaseClasses import Region, Entrance, CollectionState
from worlds.generic.Rules import add_rule

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


def interpret_region_access(world: "ForagerWorld", region_name: str):
    """Reads the input Region data class to then determine the various rules to apply to the given region.
    This includes parsing items required, xp, gold, etc."""
    # TODO may be reused for locations in a similar fashion.
    region_data: ForagerRegionData = region_access[region_name]
    main_ent: Entrance = world.get_region(region_name).connect(world.get_region(region_data.parent_region))

    # Make the connection bidirectional so AP can have an easier time to generate.
    world.get_region(region_data.parent_region).connect(world.get_region(region_name))

    # If the connection requires any items to access
    if region_data.items_required:
        add_rule(main_ent, lambda state: state.has_all(region_data.items_required))

def load_regions(world: "ForagerWorld"):
    region_list: list[str] = list(world.json_tables["regions"])
    for region_name in region_list:
        world.multiworld.regions.append(Region(region_name, world.player, world.multiworld))
        if region_name in region_access:
            interpret_region_access(world, region_name)

    land_list: list[str] = list(world.json_tables["itemslands"]["Lands"].keys())
    for land_name in land_list:
        world.multiworld.regions.append(Region(land_name, world.player, world.multiworld))
        if land_name in region_access:
            interpret_region_access(world, land_name)


def can_make_leather(state : CollectionState, player : int):
    return state.has_all(("Foraging","Sewing"), player)

def can_make_plastic(state : CollectionState, player : int):
    return can_make_leather(state,player) and state.has_all(("Drilling", "Manufacturing"), player)

def can_reach_void(state : CollectionState, player : int):
    #TODO : Star Fragments not considered rn
    return can_make_plastic(state,player) and state.has("Summoning", player)

def can_make_void_steel(state: CollectionState, player: int):
    return state.has_all(("Transmutation", "Spirituality"), player) and can_reach_void(state,player)