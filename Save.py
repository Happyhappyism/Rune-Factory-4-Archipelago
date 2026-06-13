import os
import struct
from settings import get_settings
import shutil
import Utils
import pkgutil
import logging
import io
from typing import TYPE_CHECKING, Dict, List, Optional, cast
import zipfile
#from . import RF4World
from worlds.AutoWorld import World

hint_item_list = [
        "Volkanon Axe","Obsidian Bridge","Obsidian Bridge","Chipsqueek Guide","Etherlink",
        "Autumn Bridge","Cerezo Bridge","Maya Bridge","Winters Grasp","Forging License",
        "Crafting License","EZ Cooking License","Pro Cooking License","Chemistry License"
    ]
logger = logging.getLogger("Rune Factory 4 Save")
class RF4SaveData():
    game = "Rune Factory 4"
    patch_file_ending = ".sav"



def write_hint_data(world:World):
    wincon_text = ""
    match world.options.game_goal.value:
        case 0: # custom
             wincon_text = f"{world.options.custom_goal_location.value}."
        case 1: # ethelberd
            wincon_text = f"getting {world.options.fortress_runespheres.value} Rune Spheres and defeating the Emperor."
        case 2: # runeprana
            wincon_text = f"getting {world.options.runeprana_runespheres.value} Rune Spheres and bringing your friend home."
        case 3: # shipment_percentage
            wincon_text = f"shipping at least {world.options.shipment_percentage_requirement.value}% of your shipping catalogue."
        case 4: # nationized_baths
            wincon_text = f"nationalizing the bathhouse."
        case 5: # eliza
            wincon_text = f"fulfilling all of the townsfolk's requests."
        case 6: # mariage
            wincon_text = f"starting a family and claiming a legendary treasure."
        case 7: # runehunt
            wincon_text = f"finding {world.options.sphere_hunt_spheres.value} Rune Spheres out of {world.options.max_runespheres.value} in the world."
        case 8: # homeowner
            wincon_text = f"to become the owner of a fine new house."
        case _:
            wincon_text = f"[Wincon]"
    hint_dict = {"goal": wincon_text}
    for item_name in hint_item_list:
        if item_name == "Volkanon Axe" and world.options.axe_start:
            continue
        hint_location = world.multiworld.find_item(item_name, world.player)
        hint_player_name = world.multiworld.get_player_name(hint_location.player)
        hint_loc_name = hint_location.name
        hint_dict[item_name] = [hint_player_name, hint_loc_name]
        #logger.warning(f"item_name")
    return hint_dict

def write_save_data(world:World):
    #logger.warning(f"seed name: {world.multiworld.seed_name}")
    #logger.warning(f"seed: {world.multiworld.seed}")
    
    #logger.warning(f"seed: {hex(world.multiworld.seed)}")

    save_data_raw = pkgutil.get_data(__name__, f"data/rf4_sbase.sav")
    save_data = bytearray(save_data_raw)
    gender = world.options.player_character.value
    seed_name =  world.multiworld.seed_name
    seed_data = int(seed_name, 16) & 0xFFFF
    save_data[0x36] |= gender
    game_goal = world.options.game_goal.value
    #require_baths = int(world.options.require_nationize_baths.value) << 2
    #shipment_percentage = int((world.options.shipment_percentage_requirement.value) / 5) << 3
    # Set story progression state
    #if game_goal == 1:
    #    save_data[0x1E8C4] = 0x65
    if game_goal == 2:
        save_data[0x1E8C4] = 0x67

    # Write yaml options
    death_link = int(world.options.death_link.value)
    shopbox_link = int(world.options.shopbox_link.value) << 2
    doctor_option = int(world.options.no_jones_fee.value) << 1
    exp_multi = (world.options.exp_multiplier.value) & 3
    royalty_rank = world.options.starting_royalty.value
    fort_spheres = world.options.fortress_runespheres.value
    prana_spheres = world.options.runeprana_runespheres.value
    BGM_val = world.options.background_music.value
    drop_boost = world.options.drop_rate_increase.value
    appearance = world.options.character_appearance.value
    #if world.options.start_weapon.value == "random":
    #    start_weapon = world.random.choice([0x149,0x16A,0x18C,0x1C4,0x1AD,0x1FC,0x21B,0x1D8])
    #else:
    #    start_weapon = world.options.start_weapon.value
    #world.var_storage.start_weapon = world.start_weapon
    start_weapon = world.starting_weapon
    daily_trupin = world.options.daily_trupin
    show_enemy_level = world.options.show_enemy_level
    show_enemy_HP = world.options.show_enemy_HP
    #sharance_start = world.options.sharance_start
    tourism = [0, 100,250, 500, 1000, 2500, 2500]
    skill_exp_multi = ((world.options.skill_exp_multiplier.value)  & 3) << 2

    save_data[0x1E656] = death_link | doctor_option | shopbox_link        # 0
    save_data[0x1E657] = exp_multi | skill_exp_multi                      # 1
    save_data[0x1E658] = fort_spheres                                    # 2
    save_data[0x1E659] = prana_spheres                                   # 3
    save_data[0x1E65A] = game_goal                                          # 4
    save_data[0x1E65B] = drop_boost                                       # 5
    #if sharance_start:
    #    save_data[0x1E94F] |= 0x10
    save_data[0x20714] = (tourism[royalty_rank]) & 0xFF
    save_data[0x20715] = ((tourism[royalty_rank]) & 0xFF00) >> 8
    save_data[0x20718] = royalty_rank
    if appearance > 0x100:
        appearance -= 0x100
        save_data[0x20741] = 1
    save_data[0x5C48] = start_weapon & 0xFF
    if start_weapon < 0x100:
        save_data[0x5C49] -= 1
    elif start_weapon >= 0x200:
        save_data[0x5C49] += 1
    save_data[0x20740] = appearance
    save_data[0x1E947] = BGM_val
    if daily_trupin:
        save_data[0x2071F] |= 0x4
    if show_enemy_level:
        save_data[0x2071F] |= 0x20
    if show_enemy_HP:
        save_data[0x2071F] |= 0x40
    
    if world.options.recipe_start:
        save_data[0x1EB48] |= 0x80
        exclude_list = {
            0x2C2: 0x7C,
            0x2C8: 0xFC,
            0x2C9: 0xFF,
            0x2CA: 0x3F,
            0x2AF: 0x8
        }
        for offset in range(0x1EB49,0x1EB99, 1):
            save_data[offset] = 0xFF
        for offset, mask in exclude_list.items():
            save_data[0x1E8C4 + offset] ^= mask


    if shopbox_link: # Add shopbox furniture
        save_data[0x1E6DE] = 0x40 # MapID
        save_data[0x1E6DF] = 0x80 # Enabled
        save_data[0x1E6E0] = 0x7C # Shop Box Obj
        save_data[0x1E6E1] = 0x01
        save_data[0x1E6E2] = 0xBC # Xpos
        save_data[0x1E6E3] = 0x00
        save_data[0x1E6E4] = 0x50 # Y Pos
        save_data[0x1E6E5] = 0x01
    # Write run seed
    save_data[0x1EAC2] |= (seed_data & 0xFF)
    save_data[0x1EAC3] |= ((seed_data & 0xFF00) >> 8)

    player_name_bytes = bytearray(world.multiworld.player_name[world.player], "utf8")[:0x20]
    for offset in range(len(player_name_bytes)):
        name_chara = player_name_bytes[offset]
        if name_chara == b'\x00':
            break
        save_data[0x1D97A + offset] = player_name_bytes[offset]

    return bytes(save_data)

