from typing import TYPE_CHECKING

from BaseClasses import Entrance, CollectionState

from .forager_regions import ForagerRegionData, region_access
from worlds.generic.Rules import add_rule

if TYPE_CHECKING:
    from . import ForagerWorld


def interpret_region_access(world: "ForagerWorld", region_name: str, region_data: ForagerRegionData):
    """Reads the input Region data class to then determine the various rules to apply to the given region.
    This includes parsing items required, xp, gold, etc."""
    main_ent: Entrance = world.get_region(region_name).connect(world.get_region(region_data.parent_region))

    # Make the connection bidirectional so AP can have an easier time to generate.
    world.get_region(region_data.parent_region).connect(world.get_region(region_name))

    # If the connection requires any items to access
    if region_data.items_required:
        add_rule(main_ent, lambda state: state.has_all(region_data.items_required))


def create_region_access_rules(world: "ForagerWorld"):
    """Create the entrance and update the rules for each region based on the region access list"""
    for region_name, region_data in region_access.items():
        interpret_region_access(world, region_name, region_data)


def can_make_leather(state : CollectionState, player : int):
    return state.has_all(("Foraging","Sewing"), player)

def can_make_plastic(state : CollectionState, player : int):
    return can_make_leather(state,player) and state.has_all(("Drilling", "Manufacturing"), player)

def can_reach_void(state : CollectionState, player : int):
    #TODO : Star Fragments not considered rn
    return can_make_plastic(state,player) and state.has("Summoning", player)

def can_make_void_steel(state: CollectionState, player: int):
    return state.has_all(("Transmutation", "Spirituality"), player) and can_reach_void(state,player)