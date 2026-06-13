
from typing import TYPE_CHECKING, Set, Optional, Dict, Any
import logging
from .pc_ap_methods import *
from settings import get_settings
from .game_data import *
from .client_methods import *
from .game_routines import *
#from .game_patches import *
#from .Items import inventory_slots
from .Locations import shipment_data, chest_data, request_data, \
shipment_data_table, recipe_data_table, chest_data_table, request_data_table,\
friend_items, tame_data, tame_data_table, outfit_game_data
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
        #loggerExt.warning(f"recieved items: {got_items}")
        for item in got_items:
            item_id = item.item
            #ogger.warning(f"{item_id_to_name[item_id]}")
        

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
            loggerExt.warning(f"Error sending item {e}\n{traceback.format_exc()}")

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
            loggerExt.warning(f"Error Printing debug {e}\n{traceback.format_exc()}")



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
                    loggerExt.warning(f"drop celing: {drop_celing} drop boost: {self.ctx.drop_boost}")
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
            loggerExt.warning(f"Error getting info {e}\n{traceback.format_exc()}")
            


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
    tamesanity: bool = False
    rune_spheres: int = 0

    processes_base = None
    game_flags= None
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
    acc_eff_ptr = None
    fodder_ptr = None
    playerfile_ptr = None
    map_id = 0
    player_name = None
    character_appearance = None

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

    friendsanity = 0
    tamesanity = 0
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

    
    try:
        if pc_check_process(pid):
            processes_base = pc_get_proc_base(pid)
            if pm:
                pm.close_process()
            pm = pymem.Pymem(pid)
            game_flags = pc_read_ptr(pm, pc_read_ptr(pm, processes_base + 0xE9E4B0) + 8) #  0x1D7552 + 0xCC6F5E
            seed_options = pc_read_bytes(pm,processes_base + 0xE90F4E, 0x12)
            playerObj = pc_read_ptr(pm, processes_base + 0xE15078)
            #ExpGainAd = get_ptr(0x6, 0xE, b"\\x48\\x83\\xEC\\x20\\xF7\\x05....\\x00\\x00\\x00\\x40\\x48\\x8B\\xD9")
            ExpGainAd = processes_base + 0xE9AC14
            storage_box_ptr = get_inv_ptr("Storage", pm, processes_base)
            fridge_ptr = get_inv_ptr("Fridge", pm, processes_base)
            rune_abilites_ptr = get_inv_ptr("Runes", pm, processes_base)
            shop_box_ptr = get_inv_ptr("Shop", pm, processes_base)
            rf4d = processes_base + 0xE704A0
            shipment_base = rf4d - 0x1390
            moneyPtr = processes_base + 0xE94FA0
            datatblfile_base = pc_read_ptr(pm, processes_base + 0xE9E558)
            npc_table_base = pc_read_ptr(pm,(datatblfile_base + ((0xAD94*8)-0x18) ))
            #npc_table_base = pc_aob_scan(p, b"\\x4E\\x4C\\x43\\x4C\\x02\\x10\\x19\\x20")
            monster_base = npc_table_base + 0x39DC
            monster_ptr = processes_base + 0xE98FB0
            #equip_effects = pc_read_ptr(pm, pc_read_ptr(pm, processes_base + 0xE98FB0) + 0x130)
            #acc_eff_ptr =  pc_read_ptr(pm, equip_effects + 0x198) 
    except Exception as e:
        loggerExt.critical(f"Error {e}\n{traceback.format_exc()}")

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
                loggerExt.warning(f"seed: {hex(self.seed)}, seed_name: {self.seed_name}")
            if cmd in {"Connected"}:
                self.setup_pointers()
                player_data = args['players']
                self.slot_id = args['slot']
                #loggerExt.warning(f"ARGS: {args}")
                loggerExt.warning(f"slot data: {args['slot_data']}")
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
                if(args['slot_data']['Friendsanity']):
                    self.friendsanity = args['slot_data']['Friendsanity']
                if(args['slot_data']['Tamesanity']):
                    self.tamesanity = args['slot_data']['Tamesanity']
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
                
                
                #loggerExt.warning(f"Player slots: {self.player_to_slot}")
            if cmd in {"Bounced"}:
                try:
                    if 'tags' in args and 'slots' in args:
                        tags = args['tags']
                        player_slot = args['slots'][0]
                        loggerExt.warning(f"recieved bounce packet, tags:{tags}, slot: {player_slot}/{self.slot}")
                        if "ShopboxLink" in tags and self.slot == player_slot:
                            loggerExt.warning(f"Bounced package: {args}")
                            item_base64 = args['data']
                            item_bytes = base64.b64decode(item_base64)
                            shopbox_bytes = get_inv_bytes(self.pm, self.shop_box_ptr)
                            free_slot = find_free_inv_slot(shopbox_bytes, self.shop_box_ptr)
                            pc_write_bytes(self.pm,free_slot,item_bytes)
                except Exception as e:
                    loggerExt.warning(f"Error recieving bounce packet {e}\n{traceback.format_exc()}")

            if cmd in {"PrintJSON"}:
                pass
            if cmd in {"ReceivedItems"}:
                try:
                    start_index = args["index"]
                    item_list = args['items']
                    if (not self.seed_check()) or (self.recv_item_storage):
                        # could result in lost items if all start index is 0
                        self.recv_item_storage[start_index] = item_list
                    else:
                        loggerExt.warning(f"processing items from recieved items")
                        process_items(self, item_list, start_index)
                    #ap_port = pc_read(p, self.game_flags+ RECV_INDEX)
                    #recv_index = ap_port & 0xFFFF
                    
                    #loggerExt.warning(f"args: {args}")
                    
                    
                except TypeError as e:
                    self.recv_item_storage[start_index] = item_list
                    try:
                        processes_base = pc_get_proc_base(pid)
                        if processes_base:
                            self.setup_pointers()
                    except Exception as e:
                        loggerExt.critical("Could not find RF4S process")
                except Exception as e:
                    self.recv_item_storage[start_index] = item_list
                    loggerExt.warning(f"Error recieving item {e}\n{traceback.format_exc()}")
                loggerExt.warning(f"finished recieving items, item_storage{self.recv_item_storage}")
        except Exception as e:
            
            loggerExt.critical(f"Error processing server package {e}\n{traceback.format_exc()}")

    def run_gui(self):
        from kvui import GameManager
        class LOLManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
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
            self.processes_base = pc_get_proc_base(pid)
            if self.processes_base:
                if self.pm:
                    self.pm.close_process()
                self.pm = pymem.Pymem(pid)
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
                self.game_flags = pc_read_ptr(self.pm, pc_read_ptr(self.pm, self.processes_base + 0x1D7552 + 0xCC6F5E) + 8)
                self.datatblfile_base = pc_read_ptr(self.pm, self.processes_base + 0xE9E558)
                if self.datatblfile_base:
                    self.npc_table_base = pc_read_ptr(self.pm,(self.datatblfile_base + ((0xAD94*8)-0x18) ))
                #if not self.npc_table_base:
                #    self.npc_table_base = pc_aob_scan(p, b"\\x4E\\x4C\\x43\\x4C\\x02\\x10\\x19\\x20")
                self.storage_box_ptr = get_inv_ptr("Storage", self.pm, self.processes_base)
                self.fridge_ptr = get_inv_ptr("Fridge", self.pm, self.processes_base)
                self.rune_abilites_ptr = get_inv_ptr("Runes", self.pm, self.processes_base)
                self.shop_box_ptr = get_inv_ptr("Shop", self.pm, self.processes_base)

                self.friend_ptr = pc_read_ptr(self.pm, self.processes_base + 0xE9C490)

                self.monster_base = self.npc_table_base + 0x39DC
                self.time_pointer =  pc_read_ptr(self.pm, pc_read_ptr(self.pm,self.processes_base+0xE12868) +0xB0)
                self.monster_ptr = self.processes_base + 0xE98FB0

                #self.equip_effects = pc_read_ptr(self.pm, pc_read_ptr(self.pm, self.processes_base + 0xE15078) + 0x130)
                #if self.equip_effects:
                #    self.acc_eff_ptr =  pc_read_ptr(self.pm, self.equip_effects + 0x198) 
                
                self.fodder_ptr = pc_read_ptr(self.pm, self.processes_base + 0xE9ABE0) + 0xFC
                if self.game_flags:
                    self.rune_spheres = pc_readb(self.pm, self.game_flags + 0x1F8)
                self.playerfile_ptr = pc_read_ptr(self.pm, self.processes_base + 0xE15078)
                #self.menu_state_ptr = pc_read_ptr(self.pm, pc_read_ptr(self.pm, self.processes_base + 0xDCAA10) + 0x18)
                #log_pointers(self)
                #self.update_seed_options()
                if self.extra_routine_ptr:
                    pc_free_mem(self.pm,self.extra_routine_ptr)
                patch_injects(self)
                loggerExt.warning(f"extra_routine_ptr: {hex(self.extra_routine_ptr)}")
                patch_game(self)
                
                got_items = self.items_received
                #loggerExt.warning(f"processing items from setup pointers")
                process_items(self, got_items, 0)
                if self.game_goal == 8: # Homeowner
                    pc_set_bit(self.pm, self.ExpGainAd + 0x2D, 6) # Give autumn field

                #if self.processes_base:
                
                player_name_bytes = pc_read_bytes(self.pm, self.processes_base + 0xE90272, 0x20)
                self.player_name = bytes([byte for byte in player_name_bytes if byte != 0]).decode("utf-8")
                
                if self.character_appearance:
                    #logger.warning(f"character_appearance:{self.character_appearance}")
                    pc_write(self.pm, self.processes_base + 0xE9AC38, self.character_appearance)
                #if not self.auth:
                #    loggerExt.warning(f"player_name_bytes:{player_name_bytes}, player_name:{self.player_name}")
                #    self.auth = self.player_name
            else:
                loggerExt.warning(f"Process base not found ctx.processes_base:{self.processes_base}")
        except Exception as e:
            loggerExt.critical(f"Error setting up pointers game probably not loaded/n {e}")


    def log_pointers(self):
        try:
            # Logging pointers in game memory used by the client for debugging purposes
            loggerExt.warning(f"processes_base = {hex(self.processes_base)}")
            loggerExt.warning(f"shipment = {hex(self.shipment_base)}")
            loggerExt.warning(f"rf4d = {hex(self.rf4d)}")
            loggerExt.warning(f"expgain = {hex(self.ExpGainAd)}")
            loggerExt.warning(f"moneyPtr = {hex(self.moneyPtr)}")
            loggerExt.warning(f"playerObj = {hex(self.playerObj)}")
            loggerExt.warning(f"game_flags = {hex(self.game_flags)}")
            loggerExt.warning(f"npc_table_base = {hex(self.npc_table_base)}")
            loggerExt.warning(f"monster_base = {hex(self.monster_base)}")
            loggerExt.warning(f"storage_base = {hex(self.storage_box_ptr)}")
            loggerExt.warning(f"time_pointer = {hex(self.time_pointer)}")
        except Exception as e:
            loggerExt.warning(f"Something wrong with logging the pointers {e}\n{traceback.format_exc()}")

    def seed_check(self):
        if self.game_flags:
            try:
                seed_check = pc_read(self.pm, self.game_flags+ RECV_INDEX + 2) & 0xFFFF
                if (seed_check != self.seed) or (seed_check == 0) or (self.seed is None):
                    if seed_check != 0:
                        logger.warning(f"Seed mismatch detected, please ensure the right file is loaded. Expected: {hex(self.seed)}, Found: {hex(seed_check)}")
                    processes_base = pc_get_proc_base(pid)
                    if processes_base:
                        self.setup_pointers()
                    return False
                else:
                    return True
            except TypeError as t:
                #loggerExt.warning(f"Error checking seed {t}\n{traceback.format_exc()}")
                self.setup_pointers()
                return False
        else:
            self.setup_pointers()
            return False

async def game_watcher(ctx: RF4Client):
    try:
        processes_base = ctx.processes_base
        ctx.setup_pointers()
        # Old AOB scans, was inefficient delete later
        #ExpGainAd = get_ptr(0x6, 0xE, b"\\x48\\x83\\xEC\\x20\\xF7\\x05....\\x00\\x00\\x00\\x40\\x48\\x8B\\xD9")
        #moneyPtr = get_ptr(0xA, 0xE, b"\\x48\\x8B\\x05....\\x44\\x8B\\x3D....\\x48\\x85\\xC0")
        #playerObj = get_ptr(0x4, 0x8, b"\\x4C\\x0F\\x44\\x35....\\xF2\\x41\\x0F\\x10\\x46\\x58")
        #game_flags = get_ptr(0,0,b'\\x48\\x8B\\x0D....\\x45\\x8B\\xC2\\x41\\x8B\\xD1')
        #inv_base = get_base_inv()

        while not ctx.exit_event.is_set():
            try:
                if ctx.seed is None:
                    # This might be the cause of the client not connecting properly
                    await asyncio.sleep(10)
                    continue
                
                #loggerExt.warning(f"checking game_watcher seed")
                # Make sure save file matches run seed
                seed_check_result = ctx.seed_check()
                if not seed_check_result:
                    #print(f"Seed mismatch, please ensure you have loaded the correct save file")
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
                game_clear = False



                if ctx.recv_item_storage:
                    loggerExt.warning(f"found item storage {ctx.recv_item_storage}")
                    for start_index, item_list in ctx.recv_item_storage.items():
                        process_items(ctx,item_list,start_index)
                    ctx.recv_item_storage.clear()

                sending = []
                
                
                shipment_bytes = pc_read_bytes(ctx.pm, ctx.shipment_base, 4151)
                
                player_hp = pc_read(ctx.pm, ctx.combat_ptr)
                player_status_eff = pc_readb(ctx.pm, ctx.playerObj + 0xB4)
                menu_state = pc_readb(ctx.pm, ctx.processes_base + 0xE128F0)
                ctx.map_id = pc_read(ctx.pm, ctx.processes_base + 0x9EC578) & 0xFFFF
                #in_dialog = pc_readb(ctx.pm, ctx.self.dialog_ptr + 0x30)
                if ctx.death_link:
                    # Check if player is dead
                    #if player_hp <= 0 and ctx.last_death_link + 15 < time.time():
                    #logger.warning(f"last_death:{ctx.last_death_link} dflag:{hex(player_status_eff)} player_hp:{player_hp} menu:{menu_state}")
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
                    # if ctx.pending_death_link:
                    #     loggerExt.warning("recieved death link")
                        
                    #     ctx.pending_death_link = False

                # Handle outbound shopbox link
                if ctx.sending_item:
                    #inv_ptr = 
                    inv_data = get_inv_slot_data(ctx.pm, ctx.shop_box_ptr, 0)
                    clear_inv_slot(ctx.pm, ctx.shop_box_ptr, 0)
                    shop_link_json = create_shop_link_json(inv_data, ctx.sending_item)
                    await ctx.send_msgs([shop_link_json])
                    ctx.sending_item = 0

                game_flags = pc_read_bytes(ctx.pm, ctx.game_flags, 0x33F)
                # if game_flags[0x5D] != 0xFF:
                #     pc_writeb(p, ctx.game_flags + 0x5D, 0xFF) # Set tutorial flags
                
                # Check Shipment Locations
                ship_count = 0
                for loc_id, loc_data in shipment_data.items():
                    
                    byte_slice = shipment_bytes[loc_data[0]: loc_data[0]+4]
                    shipment_val = mask_shipment(byte_slice, loc_data[1])
                    if shipment_val:
                        ship_count += 1
                        sending.append(loc_id)
                    
                # Check Chest Locations
                for loc_id, loc_data in chest_data.items():
                    offset = loc_data[0]
                    mask = loc_data[1]
                    try:
                        if game_flags[offset] & mask:
                            sending.append(loc_id)
                    except Exception as e:
                        loggerExt.critical(f"Error {e}\nlooking for {hex(offset)} for {hex(loc_id)} using mask {mask}")

                # Check Request Locations
                for loc_id, loc_data in request_data.items():
                    offset = loc_data[0]
                    mask = loc_data[1]
                    try:
                        if game_flags[offset] & mask:
                            sending.append(loc_id)
                    except Exception as e:
                        loggerExt.critical(f"Error {e}\nlooking for {hex(offset)} for {hex(loc_id)} using mask {mask}")

                # Check Friendsanity Locations
                if ctx.friendsanity == 1:
                    friend_levels = check_friendship_level(ctx.pm, ctx.friend_ptr)
                    for name, index in friendsanity_data.items():
                        for level in range(0,10):
                            loc_id = 0x1C4300 + ((index * 0x10) + level)
                            if friend_levels[name][0] > level:
                                sending.append(loc_id)
                
                # Check Tamesanity Locations
                if ctx.tamesanity:
                    monster_bytes = pc_read_bytes(ctx.pm, ctx.monster_ptr, 0x1C20)
                    for monster_slot in range(0, 0x1C20, 0x24):
                        monster_id = monster_bytes[monster_slot+0x14]
                        if monster_id != 0 and (monster_id in tame_data):
                            loc_id = tame_data[monster_id]
                            sending.append(loc_id)

                # Check Outfitsanity Locations
                for loc_id, data in outfit_game_data.items():
                    offset = data[0]
                    mask = data[1]
                    try:
                        if game_flags[offset] & mask:
                            sending.append(loc_id)
                    except Exception as e:
                        loggerExt.critical(f"Error {e}\nlooking for otufit {hex(offset)} for {hex(loc_id)} using mask {mask}")


                #loggerExt.warning(f"local locations: {ctx.local_checked_locations}")
                if sending != ctx.local_checked_locations:
                    ctx.local_checked_locations = sending
                    
                # Send new Locations
                    message = [{"cmd": 'LocationChecks', "locations": sending}]
                    await ctx.send_msgs(message)

                #ctx.c
                # Process Client Commands
                #if ctx.time_speed_command:
                #    pass

                # Check Goal completetion
                story_state = pc_readb(ctx.pm, ctx.game_flags)
                #loggerExt.warning(f"story_state: {story_state}, game_goal: {ctx.game_goal}")
                match ctx.game_goal:
                    case 1: # Ethelberd
                        if story_state == 0xEB:
                            game_clear = True
                        
                        
                    case 2: # Ragnarok
                        if story_state == 0xFF:
                            game_clear = True

                    case 3: # Ship percentage
                        if ((ship_count / game_consts["total shipments"])* 100) >= ctx.ship_percent_need: 
                            
                            game_clear = True
                    case 4: # Baths
                        if pc_read(ctx.pm, ctx.processes_base + 0xE9AC16) & 0x40:
                            game_clear = True

                    case 6:
                        if 0x1C3FA0 in ctx.checked_locations: # Shipped White Stone
                            game_clear = True

                    case 7: #Rune Sphere Hunt
                        loggerExt.warning(f"rune_spheres: {ctx.rune_spheres} - sphere_hunt_spheres: {ctx.sphere_hunt_spheres}")
                        if ctx.rune_spheres >= ctx.sphere_hunt_spheres:
                            game_clear = True

                    case 8: # Homeowner
                        if not game_flags[0x20F] & 0x2:
                            game_clear = True

                    case 0: # Specific goal
                        if ctx.goal_loc in ctx.local_checked_locations:
                            game_clear = True
                        
                if not ctx.finished_game and game_clear:
                    #loggerExt.warning(f"Goal!")
                    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                    ctx.finished_game = True
            except TypeError:
                try:
                    processes_base = pc_get_proc_base(ctx.pm, pid)
                    if processes_base:
                        ctx.setup_pointers()
                except Exception as e:
                    loggerExt.critical("Could not find RF4S process")
            except Exception as e:
                loggerExt.critical(f"Error in game loop: {e}\n{traceback.format_exc()}")

            try:
                await asyncio.sleep(1)
            except Exception as e:
                loggerExt.critical(f"Error in async sleep: {e}\n{traceback.format_exc()}")

    except Exception as e:
        loggerExt.critical(f"Error {e}\n{traceback.format_exc()}")


def launch():
    try:
        save_player_name = check_files()
        logger.warning(f"save_player_name: {save_player_name}")
        #player_name = None
        #if save_file_name:
            #save_file_data = save_file_name.split("_")
            #player_name = save_file_data[3]
    except Exception as e:
        save_player_name = None
        loggerExt.critical(f"Error {e}\n{traceback.format_exc()}")
    async def main(args):
        try:
            ctx = RF4Client(args.connect, args.password)
            ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
            if gui_enabled:
                ctx.run_gui()
            ctx.run_cli()
            if save_player_name:
                ctx.auth = save_player_name
            progression_watcher = asyncio.create_task(
                game_watcher(ctx), name="RF4ProgressionWatcher")
            
            await ctx.exit_event.wait()
            ctx.server_address = None
            #loggerExt.warning(f"seed: {ctx.seed}, seed_name: {ctx.seed_name}")
            #if ctx.seed_name:
            
            await progression_watcher
            loggerExt.warning(f"exiting script")
            closing_functions(ctx.seed_name)
            await ctx.shutdown()
        except Exception as e:
            loggerExt.critical(f"Error Starting up client task {e}\n{traceback.format_exc()}")
    import colorama
    parser = get_base_parser(description="Rune Factory 4 Client text interface")

    args, rest = parser.parse_known_args()
    colorama.init()
    asyncio.run(main(args))
    colorama.deinit()