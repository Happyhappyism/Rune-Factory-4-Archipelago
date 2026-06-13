from typing import Callable, TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.AutoWorld import World
import logging
from .Items import area_items
from .Locations import recipe_data_table, shipment_data_table, recipe_levels, item_to_region, friend_data_table, tame_data_table, \
                        recipe_loc_name, ship_loc_name, request_loc_name, tame_loc_name, outfit_data_table, boss_tame_list, top_crop_list
from .game_data import game_consts
#from worlds.zillion import region
logger = logging.getLogger("Rune Factory 4 Rules")
if TYPE_CHECKING:
    from . import RF4World

from worlds.generic.Rules import add_rule, set_rule
import traceback

#  and state.has_from_list(area_items,  world.player, baths_need)
def get_region_rules(player, options):
    
    from .Locations import request_rules
    region_rule_dict =  {
        "Selphia -> Selphia Plains":
            lambda state: state.has("Volkanon Axe", player),
        "Selphia: Dragon Lake -> Obsidian Mansion":
            lambda state: state.has("Obsidian Bridge", player) and has_licenses(state,player),
        "Selphia -> Floating Empire":
            lambda state: state.has("Rune Sphere", player, options.fortress_runespheres.value) and state.has_from_list(area_items, player, 9) and has_licenses(state,player),
        "Selphia Plains -> Selphia Plains - West":
            lambda state: state.has("Obsidian Bridge", player) and has_licenses(state,player),

        "Yokmir Forest -> Yokmir Cave":
            lambda state: state.has("Chipsqueek Guide", player),

        
        "Selphia Plains - West -> Leon Karnak":
            lambda state: state.has("Etherlink", player),
        "Selphia Plains - West -> Autumn Road":
            lambda state: state.has("Autumn Bridge", player),
        "Leon Karnak -> Rune Prana":
            lambda state: state.has("Rune Sphere", player, options.runeprana_runespheres.value) and state.has_from_list(area_items, player, 10),

        "Autumn Road -> Maya Road":
            lambda state: state.has("Maya Bridge", player),
        "Autumn Road -> Silver Lake":
            lambda state: state.has("Winters Grasp", player),

        "Maya Road (Boss) -> Sechs Territory":
            lambda state: state.has("Winters Grasp", player),
        
        "Selphia Plains - East -> Sercerezo Hill":
            lambda state: state.has("Cerezo Bridge", player) and has_licenses(state,player),


        "Selphia -> Sharance Maze":
            lambda state: state.has("Rune Sphere", player, 4),

        "Selphia -> Forge":
            lambda state: state.has("Forging License", player),
        "Selphia -> Crafting":
            lambda state: state.has("Crafting License", player),
        "Selphia -> Chemistry":
            lambda state: state.has("Chemistry License", player),
        "Selphia -> EZ Cooking":
            lambda state: state.has("EZ Cooking License", player),
        "Selphia -> Pro Cooking":
            lambda state: state.has("Pro Cooking License", player),
        "Selphia -> Selphia Clothing Shop":
            lambda state: state.has("Clothing Shop", player),
    }
    for name, data in request_rules.items():
        required_request = data[0]
        item_reqs = data[1]
        if item_reqs:
            connection = f"{required_request} -> {name}"
            region_rule_dict[connection] = lambda state, item_reqs=item_reqs: all(request_rule_list(state, player, item_reqs))
            
                
    return region_rule_dict

def request_rule_list(state, player, item_reqs):
    
    request_list = []
    try:
        for item in item_reqs:
            if item == "Fenrir":
                request_list.append(state.has_from_list(area_items, player, 11))
            elif item == "Legendary Sickle":
                request_list.append(can_make_top_tool(state, player))
            elif item == "Quality Sickle":
                request_list.append(can_make_mid_tool(state, player))
            elif item[0:5] == "Ship%":
                percentage = int(item.replace("Ship% ","") )
                request_list.append(ship_percent(state, player, percentage))
            elif item in shipment_data_table:
                request_list.append(can_get_item(item, state, player))
                # tier = shipment_data_table[item].tier
                # item_region = shipment_data_table[item].region
                # request_list.append(state.has_from_list(area_items,  player, tier) and state.can_reach_region(item_region, player))
            else:
                request_list.append(state.has(item, player))
    except Exception as e:
        logger.warning(f"Issue with request rule list {e} items: {item_reqs}")
    if request_list:
        return request_list
    else:
        return [True]

def has_licenses(state,player):
    return state.has("Forging License", player) and state.has("Crafting License", player)

def can_make_top_tool(state, player): 
    return state.has("Forging License", player) and state.has("Forging Level Up", player, 19 ) and can_get_item("Platinum", state, player)

def can_make_mid_tool(state, player): 
    return state.has("Forging License", player) and state.has("Forging Level Up", player, 6 ) and can_get_item("Silver", state, player)

def ship_percent(state, player, percentage):
    return (((sum(
        [state.can_reach_region(data.region, player) for name, data in shipment_data_table.items()])
        )/ game_consts["total shipments"]) * 100) >= percentage

def can_reach_tier(state, player, tier):
    return state.has_from_list(area_items, player, tier)

def can_get_item(name, state, player):
    try:
        if name in recipe_data_table:
            return can_make_recipe(name, state, player)
        elif name in shipment_data_table:
            tier = shipment_data_table[name].tier
            if not tier:
                tier = 0
            item_region = shipment_data_table[name].region
            #logger.warning(f"{name}")
            return can_reach_tier(state, player, tier) and state.can_reach_region(item_region, player)
        else:
            logger.warning(f"Can't get item {name}")
            return False
    except Exception as e:
        logger.warning(f"Issue getting item {name}: \n\n{traceback.format_exc()}")

def can_make_recipe(name, state, player):
    try:
        level_raw = recipe_levels[name][0]
        level_req = int(level_raw / 5)
        craft_type = recipe_levels[name][1]
        ingredients = recipe_levels[name][2]
        # try:
        #     craft_tier_list = []
        #     craft_type = recipe_data_table[name].subtype
        #     for ingredient in ingredients:
        #         craft_tier_list.append(shipment_data_table[ingredient].tier)
        #     logger.warning(f"{name}: - {craft_type}: {max(craft_tier_list)}")
        # except Exception as e:
        #         logger.warning(f"Error generating tier listing for {name}")
        
        match craft_type:
            case "Crafting": # all([state.can_reach_region(item_to_region[ingredient],  player)
                return state.has("Crafting Level Up",  player, level_req) and all([can_get_item(ingredient, state, player) for ingredient in ingredients])
            case "Cooking":
                return state.has("Cooking Level Up",  player, level_req) and all([can_get_item(ingredient, state, player) for ingredient in ingredients])
            case "Forging":
                return state.has("Forging Level Up",  player, level_req) and all([can_get_item(ingredient, state, player) for ingredient in ingredients])
            case "Chemistry":
                return state.has("Chemistry Level Up",  player, level_req) and all([can_get_item(ingredient, state, player) for ingredient in ingredients])
            case _:
                pass
    except Exception as e:
        logger.warning(f"Ingredient: {e} not found for {name}")

def get_location_rules(player):
    location_rules = {
        "Rune Prana F2 B3 Anette's Necklace Recipe Chest":
            lambda state: can_make_recipe("Heavy Boots", state, player),
        "Rune Prana F2 B3 Greenifier+ x4 Chest":
            lambda state: can_make_recipe("Heavy Boots", state, player),
        "Accessory Bread":
            lambda state: state.has("Crafting License", state, player),
        "Accessory Bread+":
            lambda state: state.has("Crafting License", state, player),
        "Cooking Bread":
            lambda state: state.has("EZ Cooking License", state, player) or state.has("Pro Cooking License", state, player), 
        "Cooking Bread+":
            lambda state: state.has("EZ Cooking License", state, player) or state.has("Pro Cooking License", state, player),
        "Farming Bread":
            lambda state: state.has("Forging License", state, player),
        "Farming Bread+":
            lambda state: state.has("Forging License", state, player),
        "Medicine Bread":
            lambda state: state.has("Chemistry License", state, player),
        "Medicine Bread+":
            lambda state: state.has("Chemistry License", state, player),
        "Weapon Bread":
            lambda state: state.has("Forging License", state, player),
        "Weapon Bread+":
            lambda state: state.has("Forging License", state, player),
    }
    return location_rules,

def set_rules(world: "RF4World"):
    from .Locations import location_data_table, chest_recipes, chest_data_table, spell_list
    water_shoe_chests = [
    "Selphia Plains - West G12 Chest - Leveliser",
    "Selphia Plains - West G12 Chest - Boiled Gyoza Recipe",
    "Selphia Plains - West G12 Chest - Sacred Pole Recipe",
    "Selphia Plains - West G12 Chest - Relax Tea",
    "Autumn Road G1 Chest - Golden Turnip Staff Recipe",
    "Autumn Road G1 Chest - Joy Waterpot Recipe",
    "Autumn Road G1 Chest - Glitter Sashimi Recipe",
    "Autumn Road G1 Chest - Intelligencer",
    ]
    player_location_vals = world.get_locations()
    player_locations = []
    for location in player_location_vals:
        player_locations.append(location.name)
    #logger.warning(f"player locations: {player_locations}")
    for loc_name in water_shoe_chests:
        location = world.multiworld.get_location(loc_name, world.player)
        add_rule(location, lambda state: can_make_recipe("Water Shoes", state, world.player))
    #player = world.player

    region_rules = get_region_rules(world.player, world.options)
    for entrance_name, rule in region_rules.items():
        entrance = world.multiworld.get_entrance(entrance_name, world.player)
        entrance.access_rule = rule

    location_rules = get_location_rules(world.player)

    for location in world.multiworld.get_locations(world.player):
        name = location.name
        #if name in location_rules and location_data_table[name].can_create(self.multiworld, player):
        if name in location_rules:
            location.access_rule = location_rules[name]

    for loc_name in top_crop_list:
        if loc_name not in player_locations:
            continue
        location = world.multiworld.get_location(loc_name, world.player)
        add_rule(location, lambda state: state.has("Aquaticus Rain", world.player) or state.has("Fiersome Sun", world.player))
    

    for spell_name in spell_list:
        if spell_name not in player_locations:
            continue
        location = world.multiworld.get_location(spell_name, world.player)
        add_rule(location, lambda state: state.has("Magic Shop",  world.player))
    
    for name, recipe_list in chest_recipes.items():
        if recipe_list is None:
            continue
        for recipe in recipe_list:
            try:
                if name not in player_locations:
                    continue
                region = chest_data_table[name].region
                location = world.multiworld.get_location(recipe, world.player)
                add_rule(location, lambda state, region=region: state.can_reach_region(region, world.player))
            except Exception as e:
                logger.warning(f"location for recipe {recipe} not found")
    
    

    #for name, data in recipe_levels.items():
    #logger.warning(f"{player_locations}")
    for name in recipe_levels:
        loc_name = recipe_loc_name[name]
        if loc_name not in player_locations:
            #logger.warning(f"{loc_name} not in list")
            continue
        try:
            location = world.multiworld.get_location(loc_name, world.player)
            add_rule(location, lambda state, name=name: can_make_recipe(name, state, world.player))
        except Exception as e:
            logger.warning(f"Item: {e} not found\n\n{traceback.format_exc()}")
            continue
        #level_raw = data[0]
        #level_req = int(level_raw / 5)

        #craft_item = None
        #ingredients = data[2]
        #if level_req == 0:
        #    level_req = 1
        # match data[1]:
        #     case "Crafting":
        #         add_rule(location, lambda state, level_req=level_req: state.has("Crafting Level Up",  world.player, level_req))
        #     case "Cooking":
        #         add_rule(location, lambda state, level_req=level_req: state.has("Cooking Level Up",  world.player, level_req))
        #     case "Forging":
        #         add_rule(location, lambda state, level_req=level_req: state.has("Forging Level Up",  world.player, level_req))
        #     case "Chemistry":
        #         add_rule(location, lambda state, level_req=level_req: state.has("Chemistry Level Up",  world.player, level_req))
        #     case _:
        #         pass

        # try:
        #     add_rule(location, lambda state, ingredients=ingredients: all([state.can_reach_region(item_to_region[ingredient],  world.player) for ingredient in ingredients]))
            
        except Exception as e:
            logger.warning(f"Ingredient: {e} not found for {name}")

    
    for name, data in friend_data_table.items():
        loc_name = f"Selphia Friendship - {name}"
        if loc_name not in player_locations:
            continue
        
        location = world.multiworld.get_location(loc_name, world.player)
        add_rule(location, lambda state, tier=data.tier: can_reach_tier(state, world.player, tier))
        if data.tier >= 2:
            add_rule(location, lambda state, liked_item=data.liked_item: can_get_item(liked_item,state,world.player))
        if data.tier >= 5:
            add_rule(location, lambda state, loved_item=data.loved_item: can_get_item(loved_item,state,world.player))

    for name, data in outfit_data_table.items():
        loc_name = f"Selphia Clothing Shop - {name}"
        logger.warning(f"outfit: {name}")
        if loc_name not in player_locations:
            continue
        location = world.multiworld.get_location(loc_name, world.player)
        add_rule(location, lambda state, tier=data.tier: can_reach_tier(state, world.player, tier))

    for name_raw, data in tame_data_table.items():
        name = data.loc_name
        if name not in player_locations:
            continue
        location = world.multiworld.get_location(name, world.player)
        if data.liked_item:
            add_rule(location, lambda state, data=data: can_get_item(data.liked_item,state,world.player) and can_reach_tier(state, world.player, data.tier))
        else:
            add_rule(location, lambda state, data=data: can_reach_tier(state, world.player, data.tier))
    
    for loc_name in boss_tame_list:
        if loc_name not in player_locations:
            continue
        location = world.multiworld.get_location(loc_name, world.player)
        add_rule(location, lambda state: state.has("Pandora's Mandate", world.player))
    
    merged_data_dict = {**shipment_data_table, **chest_data_table}
    for name_raw, data in merged_data_dict.items():
        name = data.loc_name
        if name not in player_locations:
            continue
        try:
            location = world.multiworld.get_location(name, world.player)
        except Exception as e:
            logger.warning(f"Item: {e} not found for tiering")
            continue
        shipment_tier = data.tier

        if not shipment_tier or shipment_tier == 0:
            continue
        
        #match shipment_tier:
        #    case 1:
        #        1
        add_rule(location, lambda state, shipment_tier=shipment_tier: can_reach_tier(state, world.player, shipment_tier) ) #state.has_from_list(area_items,  world.player, shipment_tier))
    
    game_goal = world.options.game_goal.value
    
    if game_goal == 1: # Ethelberd
        world.multiworld.completion_condition[world.player] = (
            lambda state: state.can_reach_region("Floating Empire", world.player)
        )
    elif game_goal == 2: # Rune Prana
        world.multiworld.completion_condition[world.player] = (
            lambda state: state.can_reach_region("Rune Prana F7 (Boss)", world.player)
        )
    elif game_goal == 3: # Shipment Percentage
        world.multiworld.completion_condition[world.player] = (
            lambda state, percentage = world.options.shipment_percentage_requirement.value: ship_percent(state, world.player, percentage )
        )
    elif game_goal == 4: # Nationized Baths
        world.multiworld.completion_condition[world.player] = (
            lambda state: can_reach_tier(state, world.player, 9)
        )
    elif game_goal ==5 : # Eliza
        world.multiworld.completion_condition[world.player] = (
            lambda state: state.can_reach_region("From Eliza!", world.player)
        )
    elif game_goal == 6: # Mariage
        if world.options.friendsanity.value == 3:
            world.multiworld.completion_condition[world.player] = (
                lambda state: state.has("Popularity", world.player, 10) and state.can_reach_region("Sechs Territory", world.player)
            )
        else:
            world.multiworld.completion_condition[world.player] = (
                lambda state: can_reach_tier(state, world.player, 10) and state.can_reach_region("Sechs Territory", world.player)
            )
    elif game_goal == 7: # Rune Hunt
        world.multiworld.completion_condition[world.player] = (
            lambda state: state.has("Rune Sphere", world.player, world.options.sphere_hunt_spheres.value)
        )
    elif game_goal == 8: # Homeowner
        world.multiworld.completion_condition[world.player] = (
            lambda state: state.has("Forging License", world.player) and state.has("Crafting License", world.player) and state.has("Chemistry License", world.player) and 
            state.has("EZ Cooking License", world.player) and state.has("Pro Cooking License", world.player) and can_reach_tier(state, world.player, 9) and state.has("Business License", world.player)
        )
    elif game_goal == 0: # Custom Goal
        goal_location = world.options.custom_goal_location.value
        goal_loc_name = goal_location
        if goal_location in player_locations:
            goal_loc_name = goal_location
        elif goal_location in recipe_data_table:
            goal_loc_name = recipe_data_table[goal_location].loc_name

        elif goal_location in shipment_data_table:
            goal_loc_name = shipment_data_table[goal_location].loc_name

        elif goal_location in tame_data_table:
            goal_loc_name = tame_data_table[goal_location].loc_name

        elif goal_location in friend_data_table:
            goal_loc_name = friend_data_table[goal_location].loc_name


        #logger.warning(f"checking logic for {goal_loc_name}")
        world.multiworld.completion_condition[world.player] = (
            lambda state, goal_loc_name=goal_loc_name: state.can_reach_location(goal_loc_name, world.player)
        )