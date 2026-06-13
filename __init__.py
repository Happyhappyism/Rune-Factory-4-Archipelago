from typing import List, Dict, Any, ClassVar

from BaseClasses import Region, Tutorial, MultiWorld, ItemClassification
from worlds.AutoWorld import WebWorld, World
from .Items import RF4Item, item_data_table, item_table, item_filler, item_filler_weight, trap_filler, trap_filler_weight, top_tools
from .Locations import RF4Location, location_data_table, location_table, locked_locations,bugged_locs, request_list, top_requests, friend_data_table, tame_data_table, outfit_data_table
from .Options import RF4Options, rf4_options_group
from .Regions import region_data_table
from .Rules import *
from .Rom import MD5Hash, RF4ProcedurePatch, write_tokens
from .Rom import get_base_rom_path as get_base_rom_path
from .Save import write_hint_data, write_save_data
from worlds.generic.Rules import set_rule, add_rule
from Utils import visualize_regions
#from .Rules import set_rules

from worlds.LauncherComponents import Component, components, Type, launch_subprocess, icon_paths
#from .Client import RF4Client

import Utils
import dataclasses
import typing
#import random
import os
#import pkgutil
#import Patch
import settings
#import math
import logging
import json

logger = logging.getLogger("Rune Factory 4")
def launch_client():
    from .Client import launch
    launch_subprocess(launch, name="Rune Factory 4 Client")

components.append(Component("Rune Factory 4 Client", "RF4Client", func=launch_client, component_type=Type.CLIENT,icon="Rune Factory 4",))
icon_paths["Rune Factory 4"] = "ap:worlds.rune4/data/icon.png"

class RF4Settings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Steam Rune Factory 4 Special Executable"""
        copy_to = "RF4S.exe"
        description = "Rune Factory 4 Executable"
        md5s = MD5Hash

    class BaseRF4Directory(settings.UserFolderPath):
        """Path to the Rune Factory 4 Special install directory"""
        copy_to = None
        description = "Rune Factory 4 Special install directory"

    class BMSPath(settings.UserFolderPath):
        """Path to the QuickBMS directory"""
        copy_to = None
        description = "QuickBMS Folder"

    class SavePath(settings.UserFolderPath):
        """Folder Path to Rune Factory 4 Saves"""
        copy_to = None
        description = " Rune Factory 4 Saves Folder"


    exe_file: RomFile = RomFile(RomFile.copy_to)
    bms_path: BMSPath = BMSPath(BMSPath.copy_to)
    save_file_path: SavePath = SavePath(SavePath.copy_to)
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
            #logger.warning(f"trap_filler: {trap_filler}, trap_filler_weight: {trap_filler_weight}, filler_pool: {filler_pool}")
            filler_pool += trap_filler
            filler_weight_pool += trap_filler_weight
            #logger.warning(f"filler_pool: {filler_pool}")

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
        import copy
        from .Locations import shipment_data_table
        for region_name in region_data_table.keys():
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

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
                case "Mushroom" | "Other" | "Grass" | "Seed":
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
                if data.tier >= self.options.max_ship_tier:
                    del duplicate_data_table[name]
                    continue
        # if not self.options.requestsanity:
        for name in request_list:
            del duplicate_data_table[name]
        # elif self.options.game_goal.value != 5:
        #     for name in top_requests:
        #         del duplicate_data_table[name]

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
                elif data.tier > self.options.max_ship_tier:
                    del duplicate_data_table[name]

        for name, data in outfit_data_table.items():
            if not self.options.outfitsanity:
                del duplicate_data_table[name]

        for name in bugged_locs:
            if name in duplicate_data_table:
                del duplicate_data_table[name]

        for region_name, region_data in region_data_table.items():
            #if region_name in self.included_stages or region_name in fixed_regions:
            region = self.get_region(region_name)
            region.add_locations({
                location_data.loc_name: location_data.address for location_name, location_data in duplicate_data_table.items()
                
                if location_data.region == region_name and location_data.can_create(self)
            }, RF4Location)
            #logger.warning(f"connecting {region_data_table[region_name].connecting_regions} region_name: {region_name} ")
            region.add_exits(region_data_table[region_name].connecting_regions)

    
    def get_filler_item_name(self, filler_pool,filler_weight_pool ) -> str:
        
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
            "Shipping_Percent": self.options.shipment_percentage_requirement.value,
            "Friendsanity": self.options.friendsanity.value,
            "Tamesanity": self.options.tamesanity.value,
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
            "start_weapon": self.starting_weapon,
            "progressive_weapon": self.options.progressive_weapon.value,
            "progressive_armor": self.options.progressive_armor.value,
            "progressive_accessory": self.options.progressive_accessory.value,
            "character_appearance": self.options.character_appearance.value,
        
        }
    
    def generate_output(self, output_directory: str):
        outfilepname = f"_P{self.player}"
        outfilepname += f"_{self.multiworld.get_file_safe_player_name(self.player).replace(' ', '').replace('_','')}"
        self.rom_name_text = f'RF4{Utils.__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed:11}\0'
        self.romName = bytearray(self.rom_name_text, "utf8")[:0x20]
        self.romName.extend([0] * (0x20 - len(self.romName)))
        self.rom_name = self.romName
        self.playerName = bytearray(self.multiworld.player_name[self.player], "utf8")[:0x20]
        self.playerName.extend([0] * (0x20 - len(self.playerName)))
        out_file_name = self.multiworld.get_out_file_name_base(self.player)
        player_alt_name = out_file_name.split("_",3)
        player_alt_name[3] = player_alt_name[3].split("_")[0]
        out_file_name = "_".join(player_alt_name)
        #logger.warning(f"player_name = {self.multiworld.player_name[self.player]}, out_file_name: {out_file_name}")
        #if "_" in self.multiworld.player_name[self.player]:
        #   out_file_name =  out_file_name.replace(self.multiworld.player_name[self.player],self.multiworld.player_name[self.player].replace("_","--"))
           #"".join(c for c in name if c not in '<>:"/\\|?*')


        #patch = RF4ProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
        #patch.write_file("base_patch.bsdiff4", pkgutil.get_data(__name__, "bombt.bsdiff4"))
        #procedure = [("apply_bsdiff4", ["base_patch.bsdiff4"]), ("apply_tokens", ["token_data.bin"])]
        #procedure = [("apply_tokens", ["token_data.bin"])]
        #patch.procedure = procedure
        #write_tokens(self, patch)
        
        #patch.write(os.path.join(output_directory, f"{out_file_name}{patch.patch_file_ending}"))
        if self.options.start_weapon.value == "Random" or  self.options.start_weapon.value == "random":
            self.starting_weapon = self.random.choice([0x149,0x16A,0x18C,0x1C4,0x1AD,0x1FC,0x21B,0x1D8])
        else:
            self.starting_weapon = self.options.start_weapon.value
        ap_save_bytes = write_save_data(self)
        save_slot_val = self.options.save_slot.value
        drop_rate = self.options.drop_rate_increase.value
        monster_model = int(self.options.shuffle_monster_models)
        monster_moveset = int(self.options.shuffle_monster_AI) << 1
        monster_ai = int(self.options.shuffle_monster_AI) << 2
        monster_options = monster_model | monster_moveset | monster_ai
        music_shuffle = int(self.options.shuffle_music)
        sfx_shuffle = int(self.options.shuffle_sound_effects) << 1
        trupin_hint = int(self.options.trupin_hint) << 2
        element_shuffle = int(self.options.shuffle_elements) << 3
        sound_options = music_shuffle | sfx_shuffle | trupin_hint | element_shuffle
        if save_slot_val < 10:
            save_slot = f"0{save_slot_val}"
        else:
            save_slot = f"{save_slot_val}"
        save_file_name = f"{out_file_name}_rf4_{drop_rate}_{monster_options}_{sound_options}_s{save_slot}.sav"
        
        # Save file parameters
         # 0 'AP'
         # 1 Seed
         # 2 Slot
         # 3 Name
         # 4 'rf4'
         # 5 drop rate
         # 6 monster options
         # 7 music | sfx | hint
         # 8 Save slot
        with open(os.path.join(output_directory, save_file_name), "wb") as f:
            f.write(ap_save_bytes)
        if self.options.trupin_hint:
            hint_file_name = f"{out_file_name}_rf4_hints.json"
            hint_data = write_hint_data(self)
            with open(os.path.join(output_directory, hint_file_name), "w") as f:
                json.dump(hint_data, f)
        # ap_save = RF4SaveData(self)
        # ap_save.write_contents(write_save_data(self, ap_save))
        # ap_save_bytes = write_save_data(self, ap_save)
        # ap_save_bytes.write(os.path.join(output_directory, f"{out_file_name}_save_data.sav"))