from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification as IC

from .forager_constants import GAME_NAME
if TYPE_CHECKING:
    from worlds.forager import ForagerWorld


class ForagerItem(Item):
    game: str = GAME_NAME
    
    def __init__(self, name: str, classification: IC, code: int, player: int):
        super().__init__(name, classification, code, player)
        
def create_world_items(world: "ForagerWorld"):
    item_pool: list[Item] = []

    items_to_create: dict = {**dict(world.item_class_sets["Progression"]), **dict(world.item_class_sets["Useful"].items())}
    for prog_name, prog_category in items_to_create.items():
        if prog_category in ["Seals", "Relics"]:
            continue

        json_data: dict = world.json_tables["items"][prog_category][prog_name]
        if json_data.get("count", ""):
            for tool_count in range(json_data["count"]):
                item_pool.append(ForagerItem(prog_name, IC.progression, json_data["id"], world.player))
        else:
            item_pool.append(ForagerItem(prog_name, IC.progression, json_data["id"], world.player))

    # Calculate the number of progression items required vs the number of unfilled locations left.
    # Create that many of useful/filler items remaining.
    locations_left_to_fill: int = len(world.multiworld.get_unfilled_locations(world.player)) - len(item_pool)
    for loc_to_fill in range(locations_left_to_fill):
        # Pick a random filler item and add that to the item pool
        random_filler: str = world.random.choice(list(world.json_tables["items"]["Misc"].keys()))
        item_pool.append(ForagerItem(random_filler, IC.filler,
            world.json_tables["items"]["Misc"][random_filler], world.player))

    world.multiworld.itempool += item_pool