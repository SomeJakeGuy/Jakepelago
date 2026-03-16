from enum import StrEnum
from typing import TYPE_CHECKING, NamedTuple

from BaseClasses import Region, Location
if TYPE_CHECKING:
    from worlds.forager import ForagerWorld


class LevelGroups(StrEnum):
    FirstGroup = "Levels 2-5"
    SecondGroup = "Levels 6-10"
    ThirdGroup = "Levels 11-20"
    FourthGroup = "Levels 21-30"
    FifthGroup = "Levels 31-40"
    SixthGroup = "Levels 41-50"
    SeventhGroup = "Levels 51-60"
    EighthGroup = "Levels 61-65"


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

    str(LevelGroups.FirstGroup.name): ForagerRegionData("Menu"),
    str(LevelGroups.SecondGroup.name): ForagerRegionData(str(LevelGroups.FirstGroup.name), ["Industry"]),
    str(LevelGroups.ThirdGroup.name): ForagerRegionData(str(LevelGroups.SecondGroup.name)),
    str(LevelGroups.FourthGroup.name): ForagerRegionData(str(LevelGroups.ThirdGroup.name)),
    str(LevelGroups.FifthGroup.name): ForagerRegionData(str(LevelGroups.FourthGroup.name)),
    str(LevelGroups.SixthGroup.name): ForagerRegionData(str(LevelGroups.FifthGroup.name)),
    str(LevelGroups.SeventhGroup.name): ForagerRegionData(str(LevelGroups.SixthGroup.name)),
    str(LevelGroups.EighthGroup.name): ForagerRegionData(str(LevelGroups.SeventhGroup.name)),
}

def load_regions(world: "ForagerWorld"):
    region_list: list[str] = list(world.json_tables["regions"]) + list(world.json_tables["islands"]["Lands"].keys())
    for region_name in region_list:
        world.multiworld.regions.append(Region(region_name, world.player, world.multiworld))

    if world.options.game_mode.value == world.options.game_mode.option_default:
        for lvl_enum in LevelGroups:
            world.multiworld.regions.append(Region(str(lvl_enum.name), world.player, world.multiworld))
            # TODO Formulas to calculate xp per region to follow in rules.py
            pass


def create_locations(world: "ForagerWorld"):
    # Create all levels first.
    first_level: int = world.json_tables["locations"]["Level"]["first_id"]
    last_level: int = world.json_tables["locations"]["Level"]["last_id"]
    for i in range(2, last_level - first_level + 2):
        group_to_use: str = str(LevelGroups.FirstGroup.name)
        match i:
            case i if 5 < i <= 10:
                group_to_use: str = str(LevelGroups.SecondGroup.name)
            case i if 10 < i <= 20:
                group_to_use: str = str(LevelGroups.SecondGroup.name)
            case i if 20 < i <= 30:
                group_to_use: str = str(LevelGroups.FourthGroup.name)
            case i if 30 < i <= 40:
                group_to_use: str = str(LevelGroups.FifthGroup.name)
            case i if 40 < i <= 50:
                group_to_use: str = str(LevelGroups.SixthGroup.name)
            case i if 50 < i <= 60:
                group_to_use: str = str(LevelGroups.SeventhGroup.name)
            case i if 60 < i <= 65:
                group_to_use: str = str(LevelGroups.EighthGroup.name)

        world.get_region(group_to_use).locations.append(
            Location(world.player, f"Level {i}", (first_level + i) - 2))

    # Create the tools, minus the rods
    tools_not_create: list[str] = ["Fire Rod", "Meteor Rod", "Thunder Rod", "Storm Rod", "Ice Rod",
        "Blizzard Rod", "Necro Rod", "Death Rod"]
    for loc_group, loc_list in world.json_tables["locations"].items():
        if loc_group == "Level" or loc_group == "Bundles":
            continue

        for loc_name, loc_data in loc_list.items():
            if loc_name in tools_not_create:
                continue

            world.get_region(str(loc_data["region"])).locations.append(Location(
                world.player, loc_name, loc_data["id"]))