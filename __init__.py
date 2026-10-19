from typing import List, Dict, Any, ClassVar

from BaseClasses import Region, Tutorial, MultiWorld, ItemClassification
from worlds.AutoWorld import WebWorld, World
from .Items import RF4Item, item_data_table, item_table, item_filler, item_filler_weight, trap_filler, trap_filler_weight, top_tools
from .Locations import location_table, locked_locations, location_data_table
from .Options import RF4Options, rf4_options_group
from .Regions import region_data_table
from .Rules import *
from .Rom import get_base_rom_path as get_base_rom_path
#from .Save import write_hint_data, write_save_data
from .Gen import generate_aprf4s
from worlds.generic.Rules import set_rule, add_rule

#from .Rules import set_rules

from worlds.LauncherComponents import Component, components, Type, launch_subprocess, icon_paths, SuffixIdentifier
#from .Client import RF4Client

import Utils
import dataclasses
import typing
from base64 import b64encode
#import random
import io
import os
import yaml
#import pkgutil
#import Patch
import settings
#import math
import logging
import json
import zipfile


logger = logging.getLogger("Rune Factory 4")
def launch_client(*args: str):
    from .Client import launch
    launch_subprocess(launch, name="Rune Factory 4 Client", args=args)

components.append(Component("Rune Factory 4 Client", "RF4Client", func=launch_client, component_type=Type.CLIENT,icon="Rune Factory 4",file_identifier=SuffixIdentifier(".aprf4s")))
icon_paths["Rune Factory 4"] = "ap:worlds.rune4/data/icon.png"

class RF4Settings(settings.Group):
    # class RomFile(settings.UserFilePath):
    #     """File name of the Steam Rune Factory 4 Special Executable"""
    #     copy_to = "RF4S.exe"
    #     description = "Rune Factory 4 Executable"
    #     md5s = MD5Hash

    class BaseRF4Directory(settings.UserFolderPath):
        """Path to the Rune Factory 4 Special install directory"""
        copy_to = None
        description = "Rune Factory 4 Special install directory"

    # class BMSPath(settings.UserFolderPath):
    #     """Path to the QuickBMS directory"""
    #     copy_to = None
    #     description = "QuickBMS Folder"

    class SavePath(settings.UserFolderPath):
        """Folder Path to Rune Factory 4 Saves"""
        copy_to = None
        description = " Rune Factory 4 Saves Folder"


    #exe_file: RomFile = RomFile(RomFile.copy_to)
    #bms_path: BMSPath = BMSPath(BMSPath.copy_to)
    #save_file_path: SavePath = SavePath(SavePath.copy_to)
    rf4s_install_path: BaseRF4Directory = BaseRF4Directory(BaseRF4Directory.copy_to)



class RF4WebWorld(WebWorld):
    theme = "stone"

    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to playing Rune Factory 4.",
        language="English",
        file_name="guide_en.md",
        link="guide/en",
        authors=["Happymhappyism"]
    )

    tutorials = [setup_en]
    option_groups = rf4_options_group


class RF4World(World):
    """Have fun!"""

    game = "Rune Factory 4"
    data_version = 1
    web = RF4WebWorld()
    options_dataclass = RF4Options
    settings: ClassVar[RF4Settings]
    topology_present = False
    settings_key = "rf4_settings"
    options: RF4Options
    location_name_to_id = location_table
    item_name_to_id = item_table

    

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)

    def create_item(self, name: str) -> RF4Item:
        return RF4Item(name, item_data_table[name].type, item_data_table[name].code, self.player)
    
    def create_items(self) -> None:
        item_pool: List[RF4Item] = []
        filler_pool = item_filler.copy()
        filler_weight_pool = item_filler_weight.copy()
        if self.options.include_traps:
            filler_pool += trap_filler
            filler_weight_pool += trap_filler_weight

        for name, item in item_data_table.items():
                if item.code and item.can_create(self) and (item.working == True):
                    for x in range(item.num_exist):
                        item_pool.append(self.create_item(name))

        for x in range(self.options.max_runespheres.value):
            item_pool.append(self.create_item("Rune Sphere"))

        if self.options.progressive_weapon:
            for x in range(12):
                item_pool.append(self.create_item("Progressive Weapon"))

        if self.options.progressive_armor:
            for x in range(12):
                item_pool.append(self.create_item("Progressive Armor"))
            for x in range(14):
                item_pool.append(self.create_item("Progressive Shoes"))
                item_pool.append(self.create_item("Progressive Shield"))
                item_pool.append(self.create_item("Progressive Headgear"))

        if self.options.progressive_accessory:
            for x in range(14):
                item_pool.append(self.create_item("Progressive Accessory"))
        
        if self.options.friendsanity.value == 3:
            for x in range(10):
                item_pool.append(self.create_item("Popularity"))

        if self.options.axe_start:
            self.multiworld.push_precollected(self.create_item("Volkanon Axe"))
        else:
            item_pool.append(self.create_item("Volkanon Axe"))

        if self.options.shop_start:
            self.multiworld.push_precollected(self.create_item("Blossoms Groceries"))
            self.multiworld.push_precollected(self.create_item("Magic Shop"))
            self.multiworld.push_precollected(self.create_item("Jewelry Shop"))
            self.multiworld.push_precollected(self.create_item("Fish Market"))
        else:
            item_pool.append(self.create_item("Blossoms Groceries"))
            item_pool.append(self.create_item("Magic Shop"))
            item_pool.append(self.create_item("Jewelry Shop"))
            item_pool.append(self.create_item("Fish Market"))

        for item in top_tools:
            # Include a copy of all top tier farm tools
            item_pool.append(self.create_item(item))

        junk = len(self.multiworld.get_unfilled_locations(self.player)) - len(item_pool)
        item_pool += [self.create_item(self.get_filler_item_name(filler_pool,filler_weight_pool )) for _ in range(junk)]
        self.multiworld.itempool += item_pool

    def create_regions(self) -> None:
        from .Locations import RF4Location,  bugged_locs, request_list, top_requests, shipment_data_table, chest_data_table, festival_data_table, \
        friend_data_table, tame_data_table, outfit_data_table, barrier_data_table, box_data_table, search_data_table, boss_data_table
        from .location_data import chest_loc_list
        from .game_data import region_tiers

        import copy
        
        for region_name in region_data_table.keys():
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        max_tier = self.options.max_ship_tier.value
        # Handle option sanities
        duplicate_data_table = copy.deepcopy(location_data_table)
        for name, data in shipment_data_table.items():
            if name not in duplicate_data_table:
                continue
            match data.type:
                case "Fish":
                    if not self.options.fishsanity:
                        del duplicate_data_table[name]
                        continue
                case "Gold Crop":
                    if not self.options.goldcropsanity:
                        del duplicate_data_table[name]
                        continue
                case "Large Crop":
                    if not self.options.largecropsanity:
                        del duplicate_data_table[name]
                        continue
                case "Drop" | "Boss Drop":
                    if not self.options.dropsanity:
                        del duplicate_data_table[name]
                        continue
                case "Forge":
                    if not self.options.forgesanity:
                        del duplicate_data_table[name]
                        continue
                case "Craft":
                    if not self.options.craftsanity:
                        del duplicate_data_table[name]
                        continue
                case "Dish":
                    if not self.options.dishsanity:
                        del duplicate_data_table[name]
                        continue
                case "Spell":
                    if not self.options.spellsanity:
                        del duplicate_data_table[name]
                        continue
                case "Crop":
                    if not self.options.cropsanity:
                        del duplicate_data_table[name]
                        continue
                case "Mineral":
                    if not self.options.mineralsanity:
                        del duplicate_data_table[name]
                        continue
                case "Mushroom" | "Other" | "Grass" | "Seed" | "Special":
                    if not self.options.foragesanity:
                        del duplicate_data_table[name]
                        continue
                case "Vitamin" | "Potion":
                    if not self.options.chemicsanity:
                        del duplicate_data_table[name]
                        continue
                case "Product" | "Grocery" | "Fruit" | "Bread" | "Tool":
                    if not self.options.grocerysanity:
                        del duplicate_data_table[name]
                        continue
            if data.sell_value:
                if data.sell_value >= self.options.max_sell_value:
                    del duplicate_data_table[name]
                    continue
            if data.tier:
                if data.tier > max_tier:
                    del duplicate_data_table[name]
                    continue
        if not self.options.requestsanity:
            for name in request_list:
                del duplicate_data_table[name]
        elif self.options.game_goal.value != 5:
            for name in top_requests:
                del duplicate_data_table[name]

        if not self.options.chestsanity:
            for name in chest_loc_list:
                del duplicate_data_table[name]
        else:
            for name, data in chest_data_table.items():
                if data.tier > max_tier:
                    del duplicate_data_table[data.loc_name]

        max_friend = self.options.max_friendship.value
        friendsanity_type = self.options.friendsanity.value
        for name, data in friend_data_table.items():
            if friendsanity_type != 1:
                del duplicate_data_table[name]
            else:
                if data.tier > max_friend:
                    del duplicate_data_table[name]

        for name, data in tame_data_table.items():
            if name in duplicate_data_table:
                if not self.options.tamesanity:
                    del duplicate_data_table[name]
                elif data.tier > max_tier:
                    del duplicate_data_table[name]



        for name, data in outfit_data_table.items():
            if not self.options.outfitsanity:
                del duplicate_data_table[name]

        for name, data in barrier_data_table.items():
            if not self.options.barriersanity:
                del duplicate_data_table[name]
            elif data.region in region_tiers:
                if  region_tiers[data.region] > max_tier:
                    del duplicate_data_table[name]
                        
        for name, data in box_data_table.items():
            if not self.options.boxsanity:
                del duplicate_data_table[name]
            elif data.region in region_tiers:
                if region_tiers[data.region] > max_tier :
                    del duplicate_data_table[name]

        for name, data in search_data_table.items():
            if not self.options.searchsanity:
                del duplicate_data_table[name]
            elif data.region in region_tiers:
                if region_tiers[data.region] > max_tier:
                    del duplicate_data_table[name]

        for name_raw, data in boss_data_table.items():
            name = data.loc_name
            if name in duplicate_data_table:
                if not self.options.boss_sanity:
                    del duplicate_data_table[name]
                elif data.tier > max_tier:
                    del duplicate_data_table[name]

        for name, data in festival_data_table.items():
            if not self.options.festival_sanity:
                if name in duplicate_data_table:
                    del duplicate_data_table[name]

        for name in bugged_locs:
            if name in duplicate_data_table:
                del duplicate_data_table[name]

        goal_val = self.options.game_goal.value
        match goal_val:
            case 0:
                custom_goal_loc = self.options.custom_goal_location.value
                if custom_goal_loc in location_data_table:
                    duplicate_data_table[custom_goal_loc] = location_data_table[custom_goal_loc]
            #case 6:
            #    duplicate_data_table["Sechs Territory Shipment - White Stone"] = location_data_table["Sechs Territory Shipment - White Stone"]

        for region_name, region_data in region_data_table.items():
            #if region_name in self.included_stages or region_name in fixed_regions:
            region = self.get_region(region_name)
            region.add_locations({
                location_data.loc_name: location_data.address for location_name, location_data in duplicate_data_table.items()
                
                if location_data.region == region_name and location_data.can_create(self)
            }, RF4Location)
            region.add_exits(region_data_table[region_name].connecting_regions)

    
    def get_filler_item_name(self, filler_pool,filler_weight_pool ) -> str:
        # Create filler items
        junk_item = self.random.choices(filler_pool,filler_weight_pool)[0]
        return junk_item
    
    set_rules = set_rules
        
    
    def fill_slot_data(self) -> dict:
        goal_loc_option = self.options.custom_goal_location.value
        
        if goal_loc_option in location_data_table:
            goal_loc = location_data_table[goal_loc_option].address
        else:
            goal_loc = None
        return {
            "DeathLink": self.options.death_link.value,
            "ShopboxLink": self.options.shopbox_link.value,
            "Goal": self.options.game_goal.value,
            "GoalLoc": goal_loc,
            "ShipSanities": {
                "CropSanity": self.options.cropsanity.value,
                "GoldcropSanity": self.options.goldcropsanity.value,
                "LargeCropSanity": self.options.largecropsanity.value,
                "DropSanity": self.options.dropsanity.value,
                "SpellSanity": self.options.spellsanity.value,
                "MineralSanity": self.options.mineralsanity.value,
                "GrocerySanity": self.options.grocerysanity.value,
                "ForageSanity": self.options.foragesanity.value,
                "Fishsanity": self.options.fishsanity.value,
                "ForgeSanity": self.options.forgesanity.value,
                "CraftSanity": self.options.craftsanity.value,
                "DishSanity": self.options.dishsanity.value,
                "ChemicSanity": self.options.chemicsanity.value,
            },
            "Shipping_Percent": self.options.shipment_percentage_requirement.value,
            "ChestSanity": self.options.chestsanity.value,
            "Friendsanity": self.options.friendsanity.value,
            "RequestSanity": self.options.requestsanity.value,
            "Tamesanity": self.options.tamesanity.value,
            "OutfitSanity": self.options.outfitsanity.value,
            "BarrierSanity": self.options.barriersanity.value,
            "BoxSanity": self.options.boxsanity.value,
            "SearchSanity": self.options.searchsanity.value,
            "fortress_runespheres": self.options.fortress_runespheres.value,
            "runeprana_runespheres": self.options.runeprana_runespheres.value,
            "sphere_hunt_spheres": self.options.sphere_hunt_spheres.value,
            "no_jones_fee": self.options.no_jones_fee.value,
            "exp_multiplier": self.options.exp_multiplier.value,
            "skill_exp_multiplier": self.options.skill_exp_multiplier.value,
            "friendship_multiplier": self.options.friendship_multiplier.value,
            "drop_rate_increase": self.options.drop_rate_increase.value,
            "open_airship": self.options.out_of_logic_airship.value,
            "gay_dating": self.options.gay_dating.value,
            "start_weapon": self.options.start_weapon.value,
            "progressive_weapon": self.options.progressive_weapon.value,
            "progressive_armor": self.options.progressive_armor.value,
            "progressive_accessory": self.options.progressive_accessory.value,
            "character_appearance": self.options.character_appearance.value,
            "boss_sanity": self.options.boss_sanity.value,
            "festival_sanity": self.options.festival_sanity.value,
            "chest_shuffle": self.options.chest_shuffle.value,
        }
    
    def generate_output(self, output_directory: str):
        generate_aprf4s(self,output_directory)
                