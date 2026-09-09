
from typing import TYPE_CHECKING, Set, Optional, Dict, Any, NamedTuple
import logging
from .pc_ap_methods import *
from settings import get_settings
from .game_data import *
from .client_methods import *
from .game_routines import *
#from .game_patches import *
#from .Items import inventory_slots
from .Locations import  \
shipment_data_table, recipe_data_table, chest_data_table, request_data_table,\
friend_items, tame_data_table
from .Launch import *

import base64
import pymem


# Big thank you to the Lobotomy Corperation Developer K3 for reference on how to setup the client

import asyncio
import Utils
import time
# import os
# import sys
# import shutil
# import requests
import json

#Debug
import traceback

if __name__ == "__main__":
    Utils.init_logging("RF4Client", exception_logger="Client")

from NetUtils import NetworkItem, ClientStatus
from CommonClient import gui_enabled, logger, get_base_parser,  ClientCommandProcessor,\
    CommonContext, server_loop

loggerExt = logging.getLogger("Rune Factory 4 Client")

pid = "RF4S.exe"
RECV_INDEX = 0x1FC

class RF4CommandProcessor(ClientCommandProcessor):
    ctx: "RF4Client"
    def _cmd_timespeed(self, *speed:str):
        """Change the in game time speed
        These can be in the following formats
        tuple name example: double, triple, half
        percentage: 200%, 300%, 50%
        multiplier: 2x, 3x, 0.5x"""
        if speed:
            speed_arg = speed[0].lower()
            match speed_arg:
                case "tenth" | "0.1x" | "10%" | "1/10":
                    game_speed = 410
                case "quarter" | "0.25x" | "25%" | "1/4":
                    game_speed = 1024
                case "half" | "0.5x" | "50%" | "1/2":
                    game_speed = 2048
                case "normal" | "1x" | "100%":
                    game_speed = 4096
                case "double" | "2x" | "200%":
                    game_speed = 8192
                case "triple" | "3x" | "300%":
                    game_speed = 12288
                case "quadruple" | "4x" | "400%":
                    game_speed = 16384
                case "quintuple" | "5x" | "500%":
                    game_speed = 20480
                case "decuple" | "10x" | "1000%":
                    game_speed = 40960
                case _:
                    try:
                        game_speed = 4096 * int(speed_arg.replace('x',''))
                        if game_speed > 100000:
                            game_speed = 100000
                    except Exception as e:
                        game_speed = 4096
                        self.output(f"Invalid Time")
            pc_write(self.ctx.pm, self.ctx.time_pointer + 0x30, game_speed)

    def _cmd_resync(self):
        """Resync memory in case something goes wrong"""
        self.ctx.setup_pointers()
        self.output(f"Resyncing Memory")
        got_items = self.ctx.items_received
        process_items(self.ctx, got_items, 0)
        for item in got_items:
            item_id = item.item


    def _cmd_deathlink(self):
        """Use this command to turn Death Link on and off."""
        if self.ctx.death_link:
            self.ctx.death_link = False
            self.output(f"Death Link turned off")
        else:
            self.ctx.death_link = True
            self.output(f"Death Link turned on")

    def _cmd_senditem(self, *player_name:str):
        """Send an item to another player using /senditem [playername]
        this will take the first slot of your shopbox and send it to the desired player"""
        try:
            if player_name:
                player_name = player_name[0].lower()
                if player_name in self.ctx.player_to_slot:
                    player_slot = self.ctx.player_to_slot[player_name]
                    self.ctx.sending_item = player_slot
                    self.output(f"Item sent to {player_name}")
                else:
                    self.output(f"Player not found")
            else:
                self.output(f"Missing Player name")
        except Exception as e:
            loggerExt.error(f"Error sending item {e}\n{traceback.format_exc()}")

    def _cmd_debug(self, *info_type:str):
        """Prints some debug information. Options are
        goal, shopbox_link, seed, slot, goal_loc, rune_spheres, process_base,
        fortress_sphere_need, time_speed, death_link, ship_percent_need"""
        try:
            if info_type:
                match info_type[0]:
                    case "goal":
                        self.output(f"{self.ctx.game_goal}")
                    case "shopbox_link":
                        self.output(f"{self.ctx.shopbox_link}")
                    case "seed":
                        self.output(f"{self.ctx.seed}")
                    case "slot":
                        self.output(f"{self.ctx.slot}")
                    case "goal_loc":
                        self.output(f"{self.ctx.goal_loc}")
                    case "rune_spheres":
                        self.output(f"{self.ctx.rune_spheres}")
                    case "process_base":
                        if self.ctx.processes_base:
                            self.output(f"{hex(self.ctx.processes_base)}")
                        else:
                            self.output(f"None")
                    case "fortress_sphere_need":
                        self.output(f"{self.ctx.fortress_sphere_need}")
                    case "prana_sphere_need":
                        self.output(f"{self.ctx.prana_sphere_need}")
                    case "time_speed":
                        self.output(f"{self.ctx.time_speed}")
                    case "death_link":
                        self.output(f"{self.ctx.death_link}")
                    case "ship_percent_need":
                        self.output(f"{self.ctx.ship_percent_need}")
                    case _:
                        self.output(f"{info_type} Invalid Argument")
            else:
                self.output("no argument detected")
        except Exception as e:
            loggerExt.error(f"Error Printing debug {e}\n{traceback.format_exc()}")



    def _cmd_info(self, *item_name:str):
        """Get information on location, use Camel Case for item names ex. 'Earth Crystal'.
        For items that are two or more words be sure to include them in apostrophe ''
        Shipable items: shipped, monster, tier, region
        Recipies: ingredients, level, type
        Monsters: tamed, region, tier, likes, produce, drop
        Villagers: likes, loves"""
        try:
            if item_name:
                item_name_var = item_name[0].title()
                if len(item_name) > 1:
                    info_type = item_name[1].lower()
                else:
                    info_type = None
                if item_name_var in item_alias:
                    item_name_var = item_alias[item_name_var]
                if item_name_var in recipe_data_table:
                    item_data = recipe_data_table[item_name_var]
                    ship_data = shipment_data_table[item_name_var]
                    match info_type:
                        case None:
                            loc_id = ship_data.apid
                            if loc_id in self.ctx.local_checked_locations:
                                shipped = "Shipped"
                            else:
                                shipped = "Unshipped"
                            self.output(f"{shipped}\n{item_data.craft_type} lvl {item_data.level}\n{item_data.ingredients}")
                        case "type":
                            self.output(f"{item_name_var} is {item_data.craft_type}")
                        case "ingredients":
                            self.output(f"{item_name_var} needs {item_data.ingredients}")
                        case "level":
                            self.output(f"{item_name_var} is level {item_data.level}")

                elif item_name_var in shipment_data_table:
                    item_data = shipment_data_table[item_name_var]
                    match info_type:
                        case None:
                            loc_id = item_data.apid
                            if loc_id in self.ctx.local_checked_locations:
                                shipped = "Shipped"
                            else:
                                shipped = "Unshipped"
                            self.output(f"{shipped}\n{item_data.region} Tier {item_data.tier}\ndropped by {item_data.monster}")
                        case "region":
                            self.output(f"{item_name_var} found in {item_data.region}")
                        case "tier":
                            self.output(f"{item_name_var} is tier {item_data.tier}")
                        case "monster":
                            self.output(f"{item_name_var} dropped by {item_data.monster}")
                        case "shipped":
                            loc_id = shipment_data_table[item_name_var].apid
                            if loc_id in self.ctx.local_checked_locations:
                                self.output(f"{item_name_var} has been shipped")
                            else:
                                self.output(f"{item_name_var} was not shipped")

                elif item_name_var in friend_items:
                    match info_type:
                        case None:
                            self.output(f"{item_name_var} likes {friend_items[item_name_var][0]} and loves {friend_items[item_name_var][1]}" )
                        case "likes":
                            self.output(f"{item_name_var} likes {friend_items[item_name_var][0]}")
                        case "loves":
                            self.output(f"{item_name_var} loves {friend_items[item_name_var][1]}")

                elif item_name_var in tame_data_table:
                    monster_data = tame_data_table[item_name_var]
                    drop_list = monster_data.drop
                    drop_chance = monster_data.drop_rates
                    drop_str = ""
                    drop_celing = 1000 - pc_read(self.ctx.pm, self.ctx.ExpGainAd + 0x28)
                    for x in range(len(drop_list)):

                        drop_rate = ((int(drop_chance[x]) + self.ctx.drop_boost) / drop_celing) * 100
                        drop_str += f"{drop_list[x]}: {drop_rate:.2f}%, "
                    match info_type:
                        case None:
                            loc_id = monster_data.apid
                            if monster_data.liked_item is None:
                                shipped = "Not Tameable"
                            elif loc_id in self.ctx.local_checked_locations:
                                shipped = "Tamed"
                            else:
                                shipped = "Untamed"
                            self.output(f"{shipped}\n{monster_data.region} Tier {monster_data.tier}\nlikes: {monster_data.liked_item} produces: {monster_data.produce}\n{drop_str}")
                        case "likes":
                            self.output(f"{item_name_var} likes {monster_data.liked_item}")
                        case "region":
                            self.output(f"{item_name_var} is in {monster_data.region}")
                        case "produce":
                            if monster_data.produce:
                                self.output(f"{item_name_var} makes {monster_data.produce}")
                            else:
                                self.output(f"{item_name_var} doesn't produce anything")
                        case "drop":
                            self.output(f"{item_name_var} drops {drop_str}")
                        case "tier":
                            self.output(f"{item_name_var} is in tier {monster_data.tier}")
                        case "tamed":
                            loc_id = monster_data.apid
                            if monster_data.liked_item is None:
                                self.output(f"{item_name_var} is not tamable")
                            elif loc_id in self.ctx.local_checked_locations:
                                self.output(f"{item_name_var} has been tamed")
                            else:
                                self.output(f"{item_name_var} was not tamed")

                elif item_name_var in request_data_table:
                    request_info = request_data_table[item_name_var]
                    match info_type:
                        case "requires":
                            self.output(f"{item_name_var} requires {request_info.request_req}")

                elif item_name_var in chest_data_table:
                    chest_index = next((key for key, data in chest_data_table.items() if data.loc_name == item_name_var), None)
                    if chest_index:
                        chest_notes = chest_data_table[item_name_var]
                        self.output(f"Notes: {chest_notes}")
                    else:
                        self.output(f"Chest location name not found")

                else:
                    self.output(f"item not found")
            else:
                self.output(f"No item name given")

        except Exception as e:
            loggerExt.error(f"Error getting info {e}\n{traceback.format_exc()}")



class RF4Client(CommonContext):
    command_processor: int = RF4CommandProcessor
    game = "Rune Factory 4"
    local_checked_locations: Set[int]
    recieved_items: Set[str]

    items_handling = 0b111 # Full remote

    death_link: bool = False
    shopbox_link: bool = False
    sending_death_link: bool = True
    pending_death_link: bool = False
    sending_item = 0
    pending_item = None
    seed = None
    slot = None
    pm = None
    goal_loc = None
    player_to_slot = {}
    rune_spheres: int = 0
    game_flags = None

    processes_base = None
    game_flag_ptr_base = None
    game_flags_ptr = None
    seed_options = None
    playerObj = None
    combat_ptr = None
    skill_base = None
    ExpGainAd = None
    storage_box_ptr = None
    fridge_ptr = None
    rune_abilites_ptr = None
    shop_box_ptr = None
    friend_ptr = None
    rf4d = None
    shipment_base = None
    moneyPtr = None
    datatblfile_base = None
    npc_table_base = None
    monster_base = None
    time_pointer = None
    monster_ptr = None
    equip_effects = None
    seed_check_result: bool = False
    acc_eff_ptr = None
    fodder_ptr = None
    playerfile_ptr = None
    map_id = 0
    prev_map = 0
    player_name = None
    character_appearance = None
    menu_state_ptr = None

    doctor_option = False
    skill_exp_multi = 0
    exp_multi = 0
    fp_multi = 0

    extra_routine_ptr = None
    sphere_hunt_spheres = 100

    start_weapon: str = None
    progressive_weapon: int  = None
    progressive_armor: bool = None
    progressive_accessory: bool = None
    wep_prog: int = 0
    armor_prog: int= 0
    shield_prog: int = 0
    shoe_prog: int = 0
    head_prog: int = 0
    acc_prog: int = 0

    chestsanity = 0
    friendsanity = 0
    requestsanity = 0
    tamesanity = 0
    outfitsanity = 0
    barriersanity = 0
    boxsanity = 0
    searchsanity = 0
    game_goal = 0
    drop_boost = 0
    open_airship: bool = False
    gay_dating: bool = False
    fortress_sphere_need: int = 0x7F
    prana_sphere_need: int = 0x7F
    #require_baths = 0
    ship_percent_need = 100
    recv_item_storage = {}
    time_speed = 4096
    ship_count: int = 0

    seed_f:SeedFileInfo = None


    def __init__(self, server_address, password) -> None:
        super(RF4Client, self).__init__(server_address, password)
        self.send_index: int = 0
        self.local_checked_locations = set()
        self.recieved_items = set()
        self.syncing = False
        self.slot_data = ""
        self.time_speed_command = None

    async def server_auth(self, password_requested: bool= False):
        if password_requested and not self.password:
            await super(RF4Client, self).server_auth(password_requested)
        if not self.auth:
            if self.player_name:
                self.auth = self.player_name
            else:
                await self.get_username()
        await self.send_connect()

    async def connection_closed(self):
        await super(RF4Client, self).connection_closed()

    @property
    def endpoints(self):
        if self.server:
            return [self.server]
        else:
            return []

    async def shutdown(self):
        await super(RF4Client, self).shutdown()

    def on_package(self, cmd: str, args: dict) -> None:
        try:
            if cmd in {"RoomInfo"}:
                self.seed_name = args['seed_name']
                self.seed = (int(self.seed_name, 16) & 0xFFFF)
                loggerExt.info(f"seed: {hex(self.seed)}, seed_name: {self.seed_name}")
            if cmd in {"Connected"}:
                self.setup_pointers()
                player_data = args['players']
                self.slot_id = args['slot']
                for player in player_data:
                    self.player_to_slot[(player.name).lower()] = player.slot
                if(args['slot_data']['DeathLink']):
                    self.death_link = True
                    #self.update_death_link(self.death_link)
                if(args['slot_data']['ShopboxLink']):
                    self.shopbox_link = True
                if(args['slot_data']['Goal']):
                    self.game_goal = args['slot_data']['Goal']
                if(args['slot_data']['GoalLoc']):
                    self.goal_loc = args['slot_data']['GoalLoc']
                if(args['slot_data']['Shipping_Percent']):
                    self.ship_percent_need = args['slot_data']['Shipping_Percent']
                if(args['slot_data']['ChestSanity']):
                    self.chestsanity = args['slot_data']['ChestSanity']
                if(args['slot_data']['Friendsanity']):
                    self.friendsanity = args['slot_data']['Friendsanity']
                if(args['slot_data']['Tamesanity']):
                    self.tamesanity = args['slot_data']['Tamesanity']
                if(args['slot_data']['OutfitSanity']):
                    self.outfitsanity = args['slot_data']['OutfitSanity']

                if(args['slot_data']['RequestSanity']):
                    self.requestsanity = args['slot_data']['RequestSanity']
                if(args['slot_data']['BoxSanity']):
                    self.boxsanity = args['slot_data']['BoxSanity']
                if(args['slot_data']['BarrierSanity']):
                    self.barriersanity = args['slot_data']['BarrierSanity']
                if(args['slot_data']['SearchSanity']):
                    self.searchsanity = args['slot_data']['SearchSanity']

                if(args['slot_data']['fortress_runespheres']):
                    self.fortress_sphere_need = args['slot_data']['fortress_runespheres']
                if(args['slot_data']['runeprana_runespheres']):
                    self.prana_sphere_need = args['slot_data']['runeprana_runespheres']
                if(args['slot_data']['sphere_hunt_spheres']):
                    self.sphere_hunt_spheres = args['slot_data']['sphere_hunt_spheres']
                if(args['slot_data']['no_jones_fee']):
                    self.doctor_option = args['slot_data']['no_jones_fee']
                if(args['slot_data']['exp_multiplier']):
                    self.exp_multi = args['slot_data']['exp_multiplier']
                if(args['slot_data']['skill_exp_multiplier']):
                    self.skill_exp_multi = args['slot_data']['skill_exp_multiplier']
                if(args['slot_data']['friendship_multiplier']):
                    self.fp_multi = args['slot_data']['friendship_multiplier']
                if(args['slot_data']['drop_rate_increase']):
                    self.drop_boost = args['slot_data']['drop_rate_increase']
                if(args['slot_data']['open_airship']):
                    self.open_airship = args['slot_data']['open_airship']
                if(args['slot_data']['gay_dating']):
                    self.gay_dating = args['slot_data']['gay_dating']
                if(args['slot_data']['start_weapon']):
                    weapon_id = args['slot_data']['start_weapon']
                    wep_name = "Random"
                    match weapon_id:
                        case 0x149:
                            wep_name = "Short Sword"
                        case 0x16A:
                            wep_name = "Long Sword"
                        case 0x18C:
                            wep_name = "Spear"
                        case 0x1C4:
                            wep_name = "Axe/Hammer"
                        case 0x1AD:
                            wep_name = "Axe/Hammer"
                        case 0x1FC:
                            wep_name = "Dual Blade"
                        case 0x21B:
                            wep_name = "Fist"
                        case 0x1D8:
                            wep_name = "Staff"
                        case 0xFF:
                            wep_name = "Random"
                        case _:
                            wep_name = "Random"
                    self.start_weapon = wep_name
                if(args['slot_data']['progressive_weapon']):
                    self.progressive_weapon = args['slot_data']['progressive_weapon']
                if(args['slot_data']['progressive_armor']):
                    self.progressive_armor = args['slot_data']['progressive_armor']
                if(args['slot_data']['progressive_accessory']):
                    self.progressive_accessory = args['slot_data']['progressive_accessory']
                if(args['slot_data']['character_appearance']):
                    self.character_appearance = args['slot_data']['character_appearance']


            if cmd in {"Bounced"}:
                try:
                    if 'tags' in args and 'slots' in args:
                        tags = args['tags']
                        player_slot = args['slots'][0]
                        loggerExt.info(f"recieved bounce packet, tags:{tags}, slot: {player_slot}/{self.slot}")
                        if "ShopboxLink" in tags and self.slot == player_slot:
                            loggerExt.info(f"Bounced package: {args}")
                            item_base64 = args['data']
                            item_bytes = base64.b64decode(item_base64)
                            shopbox_bytes = get_inv_bytes(self.pm, self.shop_box_ptr)
                            free_slot = find_free_inv_slot(shopbox_bytes, self.shop_box_ptr)
                            pc_write_bytes(self.pm,free_slot,item_bytes)
                except Exception as e:
                    loggerExt.error(f"Error recieving bounce packet {e}\n{traceback.format_exc()}")

            if cmd in {"PrintJSON"}:
                pass
            if cmd in {"ReceivedItems"}:
                try:
                    start_index = args["index"]
                    item_list = args['items']
                    if (not self.seed_check_result) or (self.recv_item_storage):
                        # could result in lost items if all start index is 0
                        self.recv_item_storage[start_index] = item_list
                    elif self.game_flags_ptr:
                        self.recv_item_storage[start_index] = item_list
                    else:
                        process_items(self, item_list, start_index)


                except TypeError as e:
                    loggerExt.error(f"Error recieving items {e}\n{traceback.format_exc()}")
                    self.recv_item_storage[start_index] = item_list
                    try:
                        self.processes_base = pc_get_proc_base(self.pm)
                        if self.processes_base:
                            self.setup_pointers()
                    except Exception as e:
                        loggerExt.critical(f"Could not find RF4S process {e}\n{traceback.format_exc()}")
                except Exception as e:
                    self.recv_item_storage[start_index] = item_list
                    loggerExt.warning(f"Error recieving item {e}\n{traceback.format_exc()}")
        except Exception as e:

            loggerExt.critical(f"Error processing server package {e}\n{traceback.format_exc()}")

    def run_gui(self):
        from kvui import GameManager
        class LOLManager(GameManager):
            # Each pair becomes a tab in the client window showing that logger's output.
            # Without the extra entries the world's own loggers only reach the log file.
            logging_pairs = [
                ("Client", "Archipelago"),
                ("Rune Factory 4 Client", "RF4 Client"),
                ("Rune Factory 4 Launcher", "RF4 Launcher"),
                ("Rune Factory 4 Client Lib", "RF4 Lib"),
                ("pc_ap_methods", "RF4 Memory"),
            ]
            base_title = "Archipelago Rune Factory 4 Client"
        self.ui = LOLManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    # async def send_deathlink(self) -> None:
    #     self.sending_death_link = True
    #     self.last_death_link = time.time()
    #     await self.send_death("Megaman Died.")

    def on_deathlink(self, data):
        # kill player
        self.last_death_link = time.time()
        if self.map_id not in death_map_excludes:
            pc_writeb(self.pm, self.playerObj + 0xB4, 0x40)


    def setup_pointers(self):
        try:
            loggerExt.info(f"Setting up pointers")
            self.processes_base = pc_get_proc_base(self.pm)
            if self.processes_base:
                # reads all game pointers from game memory, if the process base is not found will instead
                
                self.rf4d = self.processes_base + 0xE704A0
                self.shipment_base = self.rf4d - 0x1390
                self.seed_options = pc_read_bytes(self.pm,self.processes_base + 0xE90F4E, 0x12)
                
                self.ExpGainAd = self.processes_base + 0xE9AC14
                self.moneyPtr = self.processes_base + 0xE94FA0
                self.playerObj = pc_read_ptr(self.pm, self.processes_base + 0xE15078)
                if self.playerObj:
                    self.combat_ptr = pc_read_ptr(self.pm, self.playerObj+ 0x130)
                    self.skill_base = pc_read_ptr(self.pm, self.playerObj + 0x138)
                self.datatblfile_base = pc_read_ptr(self.pm, self.processes_base + 0xE9E558)
                if self.datatblfile_base:
                    self.npc_table_base = pc_read_ptr(self.pm,(self.datatblfile_base + ((0xAD94*8)-0x18) ))
                    self.monster_base = self.npc_table_base + 0x39DC
                self.friend_ptr = pc_read_ptr(self.pm, self.processes_base + 0xE9C490)
                self.monster_ptr = self.processes_base + 0xE98FB0
                self.fodder_ptr = pc_read_ptr(self.pm, self.processes_base + 0xE9ABE0) + 0xFC
                if self.game_flags_ptr:
                    self.rune_spheres = pc_readb(self.pm, self.game_flags_ptr + 0x1F8)
                self.playerfile_ptr = pc_read_ptr(self.pm, self.processes_base + 0xE15078)
                if self.extra_routine_ptr:
                    pc_free_mem(self.pm,self.extra_routine_ptr)
                patch_injects(self)
                patch_game(self)

                got_items = self.items_received
                process_items(self, got_items, 0)
                if self.game_goal == 8: # Homeowner
                    pc_set_bit(self.pm, self.ExpGainAd + 0x2D, 6) # Give autumn field

                player_name_bytes = pc_read_bytes(self.pm, self.processes_base + 0xE90272, 0x20)
                self.player_name = bytes([byte for byte in player_name_bytes if byte != 0]).decode("utf-8")

                if self.character_appearance:
                    pc_write(self.pm, self.processes_base + 0xE9AC38, self.character_appearance)
            else:
                loggerExt.warning(f"Process base not found ctx.processes_base:{self.processes_base}")
        except Exception as e:
            loggerExt.critical(f"Error setting up pointers game probably not loaded/n {e}\n{traceback.format_exc()}")


    def log_pointers(self):
        try:
            # Logging pointers in game memory used by the client for debugging purposes
            loggerExt.info(f"processes_base = {hex(self.processes_base)}")
            loggerExt.info(f"shipment = {hex(self.shipment_base)}")
            loggerExt.info(f"rf4d = {hex(self.rf4d)}")
            loggerExt.info(f"expgain = {hex(self.ExpGainAd)}")
            loggerExt.info(f"moneyPtr = {hex(self.moneyPtr)}")
            loggerExt.info(f"playerObj = {hex(self.playerObj)}")
            loggerExt.info(f"game_flags = {hex(self.game_flags_ptr)}")
            loggerExt.info(f"npc_table_base = {hex(self.npc_table_base)}")
            loggerExt.info(f"monster_base = {hex(self.monster_base)}")
            loggerExt.info(f"storage_base = {hex(self.storage_box_ptr)}")
            loggerExt.info(f"time_pointer = {hex(self.time_pointer)}")
        except Exception as e:
            loggerExt.error(f"Something wrong with logging the pointers {e}\n{traceback.format_exc()}")

def seed_check(ctx: RF4Client):
    ctx.game_flag_ptr_base = pc_read_ptr(ctx.pm, ctx.processes_base + 0xE9E4B0)
    if not ctx.game_flag_ptr_base:
        return False
    ctx.game_flags_ptr = pc_read_ptr(ctx.pm, ctx.game_flag_ptr_base + 8)
    if ctx.game_flags_ptr:
        try:
            seed_check = pc_read(ctx.pm, ctx.game_flags_ptr+ RECV_INDEX + 2) & 0xFFFF
            if (seed_check != ctx.seed) or (seed_check == 0) or (ctx.seed is None):
                if seed_check != 0:
                    logger.warning(f"Seed mismatch detected, please ensure the right file is loaded. Expected: {hex(ctx.seed)}, Found: {hex(seed_check)}")
                ctx.processes_base = pc_get_proc_base(ctx.pm)
                if ctx.processes_base:
                    ctx.setup_pointers()
                return False
            else:
                if ctx.seed_check_result == False:
                    on_save_load(ctx)
                    logger.info(f"Seed check passed")
                return True
        except TypeError as t:
            loggerExt.error(f"Error checking seed {t}\n{traceback.format_exc()}")
            ctx.setup_pointers()
            return False
    else:
        loggerExt.error(f"Game flag pointer not found")
        ctx.setup_pointers()
        return False

def attach_process_memory(ctx:RF4Client):
    process_id = ctx.seed_f.process_obj.pid
    ctx.pm = pymem.Pymem()
    ctx.pm.open_process_from_id(process_id)

async def game_watcher(ctx: RF4Client):
    try:
        attach_process_memory(ctx)
        while not (ctx.processes_base) and not ctx.exit_event.is_set():
            #if pc_check_process(pid):
            ctx.processes_base = pc_get_proc_base(ctx.pm)
            if ctx.processes_base:
                patch_injects(ctx)
                pc_process_resume(ctx.seed_f.process_obj.pid)
                ctx.setup_pointers()
                varify_patches(ctx)
            else:
                loggerExt.warning(f"Can not find process, attempting again")
            await asyncio.sleep(10)
        
        

        while not ctx.exit_event.is_set():
            try:
                if ctx.seed is None:
                    # This might be the cause of the client not connecting properly
                    await asyncio.sleep(10)
                    continue
                # Make sure save file matches run seed
                ctx.seed_check_result = seed_check(ctx)
                if not ctx.seed_check_result:
                    await asyncio.sleep(2)
                    continue

                varify_patches(ctx)

                if ctx.death_link and "DeathLink" not in ctx.tags:
                    await ctx.update_death_link(ctx.death_link)
                if not ctx.death_link and "DeathLink" in ctx.tags:
                    await ctx.update_death_link(ctx.death_link)

                if ctx.syncing == True:
                    #ctx.send_slot_data()
                    sync_msg = [{'cmd': 'Sync'}]
                    if ctx.locations_checked:
                        sync_msg.append({"cmd": "LocationChecks", "locations": list(ctx.locations_checked)})
                    await ctx.send_msgs(sync_msg)
                    ctx.syncing = False

                if ctx.recv_item_storage:
                    #loggerExt.warning(f"found item storage {ctx.recv_item_storage}")
                    for start_index, item_list in ctx.recv_item_storage.items():
                        process_items(ctx,item_list,start_index)
                    ctx.recv_item_storage.clear()

                player_hp = pc_read(ctx.pm, ctx.combat_ptr)
                player_status_eff = pc_readb(ctx.pm, ctx.playerObj + 0xB4)
                menu_state = pc_readb(ctx.pm, ctx.processes_base + 0xE128F0)
                ctx.map_id = pc_read(ctx.pm, ctx.processes_base + 0x9EC578) & 0xFFFF
                if ctx.death_link:
                    # Check if player is dead
                    if player_status_eff & 0x40 and player_hp > 0:
                        ctx.sending_death_link = False
                        ctx.last_death_link = time.time()
                    elif menu_state:
                        ctx.sending_death_link = False
                        ctx.last_death_link = time.time()
                    elif ctx.map_id in death_map_excludes:
                        ctx.sending_death_link = False
                        ctx.last_death_link = time.time()
                    elif player_hp <= 0 and ctx.last_death_link + 6 < time.time():
                        await ctx.send_death(ctx.player_names[ctx.slot]+" died.")
                    else:
                        ctx.sending_death_link = False

                # Handle outbound shopbox link
                if ctx.sending_item:
                    inv_data = get_inv_slot_data(ctx.pm, ctx.shop_box_ptr, 0)
                    clear_inv_slot(ctx.pm, ctx.shop_box_ptr, 0)
                    shop_link_json = create_shop_link_json(inv_data, ctx.sending_item)
                    await ctx.send_msgs([shop_link_json])
                    ctx.sending_item = 0

                # Send extra slot data
                if ctx.map_id != ctx.prev_map:
                    await ctx.send_msgs([
                        {
                            "cmd": "Bounce",
                            "slots": [ctx.slot],
                            "currentMap": ctx.map_id,
                        }
                    ])
                ctx.prev_map = ctx.map_id
                ctx.game_flags = pc_read_bytes(ctx.pm, ctx.game_flags_ptr, 0x33F)
                sending = check_locations(ctx)
                # Send new Locations
                if sending != ctx.local_checked_locations:
                    ctx.local_checked_locations = sending
                    message = [{"cmd": 'LocationChecks', "locations": sending}]
                    await ctx.send_msgs(message)

                # Check Goal completetion
                game_clear = check_goals(ctx)

                if not ctx.finished_game and game_clear:
                    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                    ctx.finished_game = True
            except TypeError as e:
                try:
                    ctx.processes_base = pc_get_proc_base(ctx.pm)
                    if ctx.processes_base:
                        loggerExt.error(f"Error {e}\n {traceback.format_exc()}")
                        ctx.setup_pointers()
                except Exception as e:
                    loggerExt.critical(f"Could not find RF4S process{e}\n{traceback.format_exc()}")
            except Exception as e:
                loggerExt.critical(f"Error in game loop: {e}\n{traceback.format_exc()}")

            try:
                await asyncio.sleep(1)
            except Exception as e:
                loggerExt.critical(f"Error in async sleep: {e}\n{traceback.format_exc()}")

    except Exception as e:
        loggerExt.critical(f"Error {e}\n{traceback.format_exc()}")


def launch(*args):
    try:
        seed_f = SeedFileInfo()
        start_launch(seed_f) # -> Launch.py
        
    except Exception as e:
        loggerExt.error(f"Error: {e}\n{traceback.format_exc()}")
        return

    async def main(args):
        try:
            ctx = RF4Client(args.connect, args.password)
            ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
            if gui_enabled:
                ctx.run_gui()
            ctx.run_cli()
            if seed_f.player_name:
                ctx.auth = seed_f.player_name
            if args.name:
                ctx.auth = args.name
            ctx.seed_f = seed_f
            progression_watcher = asyncio.create_task(
                game_watcher(ctx), name="RF4ProgressionWatcher")

            await ctx.exit_event.wait()
            ctx.server_address = None

            await progression_watcher
            logger.warning(f"exiting script")
            closing_functions(ctx.seed_f)
            await ctx.shutdown()
        except Exception as e:
            loggerExt.critical(f"Error Starting up client task {e}\n{traceback.format_exc()}")
    import colorama
    parser = get_base_parser(description="Rune Factory 4 Client text interface")
    parser.add_argument('--name', default=None, help="Slot Name to connect as.")

    args, rest = parser.parse_known_args(args)
    colorama.init()
    asyncio.run(main(args))
    colorama.deinit()
