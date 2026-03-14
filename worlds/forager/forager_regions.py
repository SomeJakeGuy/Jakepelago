from enum import StrEnum
from typing import TYPE_CHECKING, NamedTuple

from BaseClasses import Region

if TYPE_CHECKING:
    from worlds.forager import ForagerWorld


class LevelGroups(StrEnum):
    FirstGroup = "Levels 1-5"
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
    # TODO start moving locations into their logical regions. Create locked items for each land, rules to follow later.
    pass