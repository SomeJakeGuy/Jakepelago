from types import MappingProxyType
from typing import TYPE_CHECKING

from BaseClasses import Entrance, CollectionState, Location

from .forager_regions import ForagerRegionData, region_access, LevelGroups
from worlds.generic.Rules import add_rule

if TYPE_CHECKING:
    from . import ForagerWorld


def interpret_region_access(world: "ForagerWorld", region_name: str, region_data: ForagerRegionData):
    """Reads the input Region data class to then determine the various rules to apply to the given region.
    This includes parsing items required, xp, gold, etc."""
    main_ent: Entrance = world.get_region(region_data.parent_region).connect(world.get_region(region_name))

    # Make the connection bidirectional so AP can have an easier time to generate.
    world.get_region(region_name).connect(world.get_region(region_data.parent_region))

    # If the connection requires any items to access
    if region_data.items_required:
        add_rule(main_ent, lambda state: state.has_all(region_data.items_required, world.player))


def create_region_access_rules(world: "ForagerWorld"):
    """Create the entrance and update the rules for each region based on the region access list"""
    for region_name, region_data in region_access.items():
        interpret_region_access(world, region_name, region_data)


def create_location_access_rules(world: "ForagerWorld"):
    # Create the victory condition
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)

    # Create the tools, minus the rods
    tools_not_create: list[str] = ["Fire Rod", "Meteor Rod", "Thunder Rod", "Storm Rod", "Ice Rod",
        "Blizzard Rod", "Necro Rod", "Death Rod"]
    for tool_name, tool_data in world.json_tables["locations"]["Tools"].items():
        if tool_name in tools_not_create or not list(tool_data["required_items"]):
            continue

        tool_loc: Location = world.get_location(tool_name)
        for item_req in list(tool_data["required_items"]):
            if "Leather" in item_req:
                add_rule(tool_loc, (lambda state: can_make_leather(state, world.player)))
            elif "Plastic" in item_req:
                add_rule(tool_loc, (lambda state: can_make_plastic(state, world.player)))
            else:
                add_rule(tool_loc, (lambda state, loc_item=item_req: state.has(loc_item, world.player)))

    # Create logic rules to lock the Levels behind
    for lvl_group in LevelGroups:
        if len(world.get_region(str(lvl_group)).entrances) > 0:
            for reg_entrace in world.get_region(str(lvl_group)).entrances:
                match lvl_group:
                    case LevelGroups.SecondGroup: # Levels 6-10
                        add_rule(reg_entrace, lambda state: can_make_leather(state, world.player))
                        continue

                    case LevelGroups.ThirdGroup: # Levels 11-20
                        add_rule(reg_entrace, lambda state, prog_pick=MappingProxyType({"Progressive Pickaxe": 2}):
                            state.has_all_counts(prog_pick, world.player) and (can_make_royal_steel(state, world.player)
                                or can_make_royal_clothing(state, world.player)))
                        continue

                    case LevelGroups.FourthGroup: # Levels 21-30
                        add_rule(reg_entrace, lambda state, prog_pick=MappingProxyType({"Progressive Pickaxe": 3}):
                            state.has_all_counts(prog_pick, world.player) and (can_make_royal_steel(state, world.player)
                                or can_make_royal_clothing(state, world.player)))
                        continue

                    case LevelGroups.FifthGroup: # Levels 31-40
                        add_rule(reg_entrace, lambda state, req_items=MappingProxyType({"Progressive Pickaxe": 4,
                            "Progressive Book": 2}): state.has_all_counts(req_items, world.player) and
                            can_reach_void(state, world.player))
                        continue

                    case LevelGroups.SixthGroup: # Levels 41-50
                        add_rule(reg_entrace, lambda state, req_items=MappingProxyType({"Progressive Pickaxe": 5,
                            "Progressive Book": 4}): state.has_all_counts(req_items, world.player) and
                            can_make_void_steel(state, world.player))
                        continue

                    case LevelGroups.SeventhGroup: # Levels 51-60
                        add_rule(reg_entrace, lambda state, req_items=MappingProxyType({"Progressive Pickaxe": 6,
                            "Progressive Book": 6}): state.has_all_counts(req_items, world.player) and
                            can_make_cosmic_steel(state, world.player))
                        continue

                    case LevelGroups.EighthGroup: # Levels 61-65
                        add_rule(reg_entrace, lambda state, req_items=MappingProxyType({"Progressive Pickaxe": 7,
                            "Progressive Book": 8}): state.has_all_counts(req_items, world.player) and
                            can_make_nuclear(state, world.player))
                        continue

                    case _:
                        continue


def can_make_leather(state : CollectionState, player : int):
    return state.has_all(["Foraging", "Sewing"], player)

def can_make_royal_clothing(state : CollectionState, player : int):
    return can_make_leather(state, player) and state.has_all(["Craftmanship", "Prospecting"], player)

def can_make_royal_steel(state : CollectionState, player : int):
    return state.has_all(["Industry", "Craftmanship", "Prospecting"], player)

def can_make_plastic(state : CollectionState, player : int):
    return can_make_royal_steel(state, player) and state.has_all(["Drilling", "Manufacturing"], player)

def can_reach_void(state : CollectionState, player : int):
    #TODO : Star Fragments not considered rn
    return can_make_plastic(state,player) and state.has_all(["Summoning", "Combat"], player)

def can_make_void_steel(state: CollectionState, player: int):
    return can_reach_void(state,player) and state.has_all(["Transmutation", "Spirituality"], player) and (
        state.has("Progressive Sword", player, 6))

def can_make_cosmic_steel(state: CollectionState, player: int):
    return can_reach_void(state, player) and state.has("Astrology", player)

def can_make_nuclear(state: CollectionState, player: int):
    return can_make_royal_steel(state, player) and state.has("Physics", player)