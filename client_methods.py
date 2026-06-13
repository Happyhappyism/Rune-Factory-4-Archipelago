from .pc_ap_methods import *
from NetUtils import NetworkItem, ClientStatus
from .game_data import *
from .Items import item_data_table, wep_cats, story_flag_items, order_flag_items,special_items, perm_items, physical_items, item_id_to_name, trap_items, progressive_items
from .game_routines import *
from .Locations import recipe_tiering
import logging
import traceback
import base64
import struct
import random

loggerExt = logging.getLogger("Rune Factory 4 Client Lib")

pid = "RF4S.exe"
RECV_INDEX = 0x1FC

def find_free_inv_slot(inv_bytes,inv_ptr):
    try:
        #loggerExt.warning(f"inv_ptr {hex(inv_ptr)}")
        offset = 0
        slot_item = int.from_bytes((inv_bytes[offset: offset+2]),"little")
        #loggerExt.warning(f"slot item:{slot_item} at {hex(inv_ptr + offset)}")
        while (slot_item) != 0:
            offset += 0x30
            slot_item = int.from_bytes((inv_bytes[offset: offset+2]),"little")
            #loggerExt.warning(f"slot item:{slot_item} at {hex(inv_ptr + offset)}")
            if offset >= len(inv_bytes):
                #loggerExt.warning(f"No free slot found")
                return None
        #loggerExt.warning(f"Found free slot at {hex((inv_ptr) + offset)}")
        return (inv_ptr) + offset
    except Exception as e:
        loggerExt.warning(f"Error finding free slot {e}\n{traceback.format_exc()}")
    #     ptr_check = pc_read_ptr(p, offset + 0x20)
    #     if  ptr_check == inv_ptr - 0x18:
    #         offset += 0x30
    #         continue
    #     else:
    #         return None
    # return offset

def get_inv_bytes(pm, inv_ptr):
    try:
        entry_count = pc_read(pm, inv_ptr-0x10) & 0xFFFF
        read_size = entry_count * 0x30
        inv_bytes = pc_read_bytes(pm, inv_ptr, read_size)
        #loggerExt.warning(f"read_size {read_size}, entry_count: {entry_count}, inv_ptr: {hex(inv_ptr)}")
        return inv_bytes
    except Exception as e:
        loggerExt.warning(f"Error getting inventory bytes {e}\n{traceback.format_exc()}")

def give_furniture(pm, processes_base, furniture,mapid,xpos,ypos):
    furniture_offset = processes_base + 0xE95D60
    furniture_block = pc_read_bytes(pm, furniture_offset, 0x210)
    if furniture in furniture_name_to_id:
        furniture_id = furniture_name_to_id[furniture]
    else:
        furniture_id= furniture
    offset = 0# + 0xE95D60
    slot_id = 0
    #loggerExt.warning(f"furniture offset:{offset}")
    while (furniture_block[offset+1] != 0x00):
        offset += 8
        slot_id +=1
        if offset >= len(furniture_block):
            return None
    # while ((pc_readb(pm, offset+1) != 0x00) and slot_id < 65):
    #     loggerExt.warning(f"furniture offset:{offset}")
    #     offset += 8
    #     slot_id +=1
    #     if slot_id >= 65:
    #         return None
    #loggerExt.warning(f"furniture offset:{offset}")
    map_bytes = mapid.to_bytes(1, byteorder='little')
    place_bytes = (0x80).to_bytes(1, byteorder='little')
    funiture_bytes = (furniture_id).to_bytes(2, byteorder='little')
    x_bytes = xpos.to_bytes(2, byteorder='little')
    y_bytes = ypos.to_bytes(2, byteorder='little')
    furnitre_bytes = b''.join([map_bytes,place_bytes,funiture_bytes,x_bytes,y_bytes])
    pc_write_bytes(pm, furniture_offset + offset, furnitre_bytes)

def give_progressive_item(ctx, item_type, progress_offset, tier_base):
    try:
        #recipe_tiering
        progress_counter = pc_readb(ctx.pm, ctx.processes_base + 0xE90296 + progress_offset)
        tier_level = (progress_counter) + tier_base
        progress_counter += 1
        #loggerExt.warning(f"tier_level:{tier_level}")
        if tier_level > 11:
            tier_level = 11
        while not recipe_tiering.get(item_type, {}).get(tier_level):
            tier_level += 1
            if tier_level > 20:
                break
        #loggerExt.warning(f"recipe_tiering:{recipe_tiering}")
        item_name = random.choice(recipe_tiering[item_type][tier_level])
        #oggerExt.warning(f"item_name:{item_name}")
        item_idx = item_data_table[item_name].item_id
        #loggerExt.warning(f"progressive item_idx:{item_idx}")
        give_item(ctx, item_idx)
        pc_writeb(ctx.pm, ctx.processes_base + 0xE90296 + progress_offset, progress_counter)
    except Exception as e:
        give_item(ctx, item_data_table["Rune Crystal"].item_id)
        loggerExt.critical(f"Error recieving progressive item {e}\nitem_type:{item_type}, progress_counter:{progress_counter}, tier_base:{tier_base}\n{traceback.format_exc()}")

def give_item(ctx, item_idx):
    try:
        inv_ptr = ctx.storage_box_ptr
        inv_bytes = get_inv_bytes(ctx.pm, inv_ptr)
        free_slot = find_free_inv_slot(inv_bytes, inv_ptr)
        if free_slot:
            item_amount = 1
            amount_mask = item_amount << 11
            item_write = item_idx | amount_mask
            #loggerExt.warning(f"Getting item, storage base {hex(inv_ptr)}, free-slot: {hex(free_slot)}, item_idx: {hex(item_idx)}, amount: {hex(item_amount)}, amount_mask: {hex(amount_mask)}, item_write: {hex(item_write)}")
            pc_write(ctx.pm, free_slot, item_write)
        else: # Free slot not found
            loggerExt.warning(f"Could not get item: {item_idx}")
    except Exception as e:
        loggerExt.critical(f"Error giving item item {e}\nitem_idx:{item_idx}\n{traceback.format_exc()}")


def get_inv_ptr(inventory, pm, processes_base):
    match inventory:
        case "Equipment":
            inventory_pointers = pc_read_ptr(pm, processes_base + 0xE6EED0)
            return pc_read_ptr(pm, inventory_pointers + ptr_offset)
        case "Backpack":
            ptr_offset = 0x8
        case "Runes":
            ptr_offset = 0x10
        case "Fridge":
            ptr_offset = 0x18
        case "Storage":
            ptr_offset = 0x20
        case "Bookshelf":
            ptr_offset = 0x28
        case "Weapon Rack":
            ptr_offset = 0x30
        case "Wardrobe":
            ptr_offset = 0x38
        case "Farm Toolbox":
            ptr_offset = 0x40
        case "Shipping":
            ptr_offset = 0x48
        case "Shop":
            ptr_offset = 0x50
        case "Unknown":
            ptr_offset = 0x58
    
    inventory_pointers = pc_read_ptr(pm, processes_base + 0xE6EED0)
    inventory_base = pc_read_ptr(pm, inventory_pointers + ptr_offset)
    inventory_first_slot = pc_read_ptr(pm, inventory_base)
    #loggerExt.warning(f"step 1: {inventory_pointers}, step 2: {inventory_base}, step 3: {inventory_first_slot}")
    return inventory_first_slot
    


def mask_shipment(byte_slice, start_bit):
    # Shipment record values are stored as unaligned 30 bit values.
    raw_mask = 0x3FFFFFFF
    bit_mask = raw_mask << start_bit
    
    raw_value = int.from_bytes(byte_slice, byteorder="little")
    masked_value = raw_value & bit_mask
    sale_value = masked_value >> start_bit
    return sale_value

def clear_inv_slot(pm, inv_ptr, inv_slot):
    loggerExt.warning(f"clearing {hex(inv_ptr)} / {hex(inv_ptr + (inv_slot * 0x30))}")
    clear_bytes = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00'
    pc_write_bytes(pm, inv_ptr + (inv_slot * 0x30), clear_bytes)

def get_inv_slot_data(pm, inv_ptr, inv_slot):
    inv_data = pc_read_bytes(pm, inv_ptr + (inv_slot * 0x30), 0x20)
    return inv_data

def create_shop_link_json(inv_data, player_slot):
    encoded_inv_data = base64.b64encode(inv_data)
    inv_data_str = encoded_inv_data.decode('ascii')
    json_data = {
        "cmd": "Bounce",
        "data": inv_data_str,
        "games": ["Rune Factory 4"],
        "slots": [player_slot],
        "tags": ["ShopboxLink"]
    }
    return json_data

def reverse_ptr_endian(val):
    val_bytes = val.to_bytes(8, byteorder= 'little')
    pass

def reverse_bits(val, size):
    res = 0
    for i in range(size):
        bit = (val >> i) & 1
        res |= (bit << (size-1 - i))
    return res

def check_friendship_level(pm, friend_base):
    try:
        friend_dict = {}
        for character, index in friendsanity_data.items():
            chara_friend_ptr = pc_read_ptr(pm, friend_base+ (index * 8))+ 0xC
            chara_friendship = pc_read(pm,chara_friend_ptr)
            friend_level = 0
            for x in range(1,11):
                if chara_friendship >= friendship_ranks[x]:
                    friend_level += 1
                else:
                    break
            friend_dict[character] = [friend_level, chara_friend_ptr]
        return friend_dict
    except Exception as e:
        loggerExt.critical(f"Error checking friendship levels {e}\n{traceback.format_exc()}")


def expand_barns(barn_int):
    other_flag = barn_int & 3
    barn_shift = barn_int >> 2
    #barn_status = {}
    barn_count = 0
    for x in range(10):
        barn_val = barn_shift & 7
        barn_lvl = reverse_bits(barn_val, 3)
        if barn_lvl < 5:
            break
        #barn_status[x] = reverse_bits(barn_val, 3)
        barn_count += 1
        barn_shift >>= 3
    barn_lvl += 1
    barn_lvl_restore = reverse_bits(barn_lvl, 3)
    rebuild = other_flag
    count = 0
    for rb in range(barn_count):
        rebuild |= 5 << ((3 * rb)+ 2)
        count += 1
    rebuild |= barn_lvl_restore << ((3 *(count) )+2)
    #loggerExt.warning(f"rebuild: {hex(rebuild)} barn_count {barn_count} barn_lvl: {barn_lvl} barn int: {hex(barn_int)}")
    return rebuild

def varify_patches(ctx):
    #loggerExt.warning(f"doctor_option: {ctx.doctor_option}, skill_exp_multi: {ctx.skill_exp_multi}, ctx.exp_multi: {ctx.exp_multi}")
    if ctx.doctor_option:
        byte_val = pc_readb(ctx.pm, ctx.processes_base + 0x20D97F)
        #loggerExt.warning(f"doctor_option = {byte_val}")
        if byte_val != 0x90:
            #loggerExt.warning(f"doctor_option patch not active")
            patch_game(ctx)
    elif ctx.skill_exp_multi:
        byte_val = pc_readb(ctx.pm, ctx.processes_base + 0xB3E73)
        #loggerExt.warning(f"skill_exp_multi = {byte_val}")
        if byte_val != 0x48:
            #loggerExt.warning(f"skill_exp_multipatch not active")
            patch_game(ctx)
    elif ctx.exp_multi:
        byte_val = pc_readb(ctx.pm, ctx.processes_base + 0xB2874)
        #loggerExt.warning(f"exp_multi = {byte_val}")
        if  byte_val != 0x48:
            #loggerExt.warning(f"exp_multi patch not active")
            patch_game(ctx)
    byte_val = pc_readb(ctx.pm, ctx.processes_base + 0x1F464B)
    if byte_val == 0xC1:
        #loggerExt.warning(f"inject = {byte_val}")
        if ctx.extra_routine_ptr:
            pc_free_mem(ctx.pm,ctx.extra_routine_ptr)
        #loggerExt.warning(f"injects not active")
        patch_injects(ctx)

def patch_game(ctx):
    # Instead of a base patch, the client writes all patches directly to memory here
    try:
        #loggerExt.warning(f"options: {options}")
        # doctor_option = bool(ctx.seed_options[0] & 0x2)
        # exp_multi = ctx.seed_options[1] & 3
        # skill_exp_multi = (ctx.seed_options[1] & 0xC) >> 2

        #have_king_order = ctx.seed_options[0xA] & 1
        for offset, patch in basic_patches.items():
            mem_offset = ctx.processes_base + offset
            pc_write_bytes(ctx.pm,mem_offset,bytes(patch))
        if ctx.doctor_option:
            pc_write_bytes(ctx.pm,ctx.processes_base+0x20D97F,bytes([0x90,0x90,0x90,0x90,0x90,0x90]))
        if ctx.skill_exp_multi:
            pc_write_bytes(ctx.pm,ctx.processes_base+0xB3E73,bytes([0x48, 0xC1, 0xE7, ctx.skill_exp_multi, 0x90,0x90,0x90,0x90,0x90,0x90,0x90,0x90,0x90,0x90]))
        if ctx.exp_multi:
            pc_write_bytes(ctx.pm,ctx.processes_base+0xB2874,bytes([0x48, 0xC1, 0xE7, ctx.exp_multi,       0x90,0x90,0x90,0x90,0x90,0x90,0x90,0x90,0x90,0x90]))
        if ctx.gay_dating:
            pc_write_bytes(ctx.pm,ctx.processes_base+0x2044B2,bytes([0x75]))
            pc_write_bytes(ctx.pm,ctx.processes_base+0x2273A2,bytes([0x75]))
        
        pandora = pc_read_bit(ctx.pm, ctx.ExpGainAd + 26, 0) & 1
        if pandora: 
            pc_writeb(ctx.pm,ctx.processes_base+0x971EF, 0x1F)
        else:
            pc_writeb(ctx.pm,ctx.processes_base+0x971EF, 0x3F)
        
        iris = pc_read_bit(ctx.pm, ctx.game_flags + 254, 0) & 2
        if iris:
            pc_write_bytes(ctx.pm,ctx.processes_base+0xED0A3,bytes([0xBE,0x00,0x00,0x00,0x00,0x90,0x90])) # mov esi, 0x00
            pc_write_bytes(ctx.pm,ctx.processes_base+0xED0A3,bytes([0x90,0x90])) # mov esi, 0x00
        
        king_order = pc_read_bit(ctx.pm, ctx.game_flags + 254, 0) & 1
        if king_order:
            pc_write_bytes(ctx.pm,ctx.processes_base+0x21CE92,bytes([0xE9, 0xBC,0x00,0x00,0x00, 0x90])) # jmp +0xBC
        
        pc_write_bytes(ctx.pm,ctx.processes_base+0x970D4,bytes([0x48,0xC1,0xE3,0x02,0x90,0x90])) # Triple Friend item tame bonus
        # Friendship point multiplier, this replaces a check for doug under specific conditons
        pc_write_bytes(ctx.pm,ctx.processes_base+0x225F44,bytes([
            0x49,0x8B,0xCF, # mov rcx,r15 {r15: fp_add, eax: new_fp}
            0xC1,0xE1,ctx.fp_multi, # shl ecx,02
            0x01,0xCF, # add edi,ecx
            0xEB,0x22, # jmp RF4S.exe+225F70
            0x90,0x90,0x90,0x90,0x90,0x90,0x90,0x90,0x90,0x90,0x90,0x90,0x90,0x90,0x90,0x90,
            0x90,0x90,0x90,0x90,0x90,0x90,0x90,0x90,0x90,0x90,0x90,0x90,0x90,0x90,0x90,0x90,0x90,0x90]))
        #pc_writeb(ctx.pm, ctx.extra_routine_ptr+ 0x40, 20)
        #if have_king_order:
        #    pc_writeb(p, process_base + 0x21CE13, 0x00)
    except Exception as e:
        loggerExt.critical(f"Error Patching: {e}\n{traceback.format_exc()}")


def patch_injects(ctx):
    ctx.extra_routine_ptr = pc_alloc_mem(ctx.pm, 0x1000)
    pc_write_bytes(ctx.pm, ctx.extra_routine_ptr + 0x200, airship_mod())
    pc_write_bytes(ctx.pm, ctx.processes_base+0x1F464B, generate_inject(ctx.extra_routine_ptr, 0x200, 2))

    pc_write_bytes(ctx.pm, ctx.extra_routine_ptr + 0x240, airship_mod_2())
    pc_write_bytes(ctx.pm, ctx.processes_base+0x21C656, generate_inject(ctx.extra_routine_ptr, 0x240, 5))


    pc_write_bytes(ctx.pm, ctx.extra_routine_ptr + 0x0, generate_fish(ctx.processes_base))
    pc_write_bytes(ctx.pm, ctx.processes_base+0x180CC0, generate_inject(ctx.extra_routine_ptr, 0, 4))

    pc_write_bytes(ctx.pm, ctx.extra_routine_ptr + 0x40, aquaticus_rain(ctx.processes_base))
    pc_write_bytes(ctx.pm, ctx.processes_base+0x185830, generate_inject(ctx.extra_routine_ptr, 0x40, 1))

    pc_write_bytes(ctx.pm, ctx.extra_routine_ptr + 0x80, ventis_wind(ctx.processes_base))
    pc_write_bytes(ctx.pm, ctx.processes_base+0x1711F4, generate_inject(ctx.extra_routine_ptr, 0x80, 20, "r14"))

    pc_write_bytes(ctx.pm, ctx.extra_routine_ptr + 0xC0, fiersome_sun(ctx.processes_base))
    pc_write_bytes(ctx.pm, ctx.processes_base+0x185C26, generate_inject(ctx.extra_routine_ptr, 0xC0, 1, "rdx"))

    pc_write_bytes(ctx.pm, ctx.extra_routine_ptr + 0x140, pandora_mandate(ctx.processes_base))
    pc_write_bytes(ctx.pm, ctx.processes_base+0x1E3841, generate_inject(ctx.extra_routine_ptr, 0x140, 3, "rcx"))

    pc_write_bytes(ctx.pm, ctx.extra_routine_ptr + 0x280, lucky_charm(ctx.processes_base))
    pc_write_bytes(ctx.pm, ctx.processes_base+0x9676D, generate_inject(ctx.extra_routine_ptr, 0x280, 2, "rcx"))

def set_airship_flags(ctx, airship_base, story_item):
    for data in airship_flags[story_item]:
        offset = data[0]
        bit = data[1]
        pc_set_bit(ctx.pm, airship_base + offset, bit)

def process_items(ctx, item_list, start_index):
    
    try:
        #loggerExt.warning(f"recv_adr: {hex(ctx.game_flags + RECV_INDEX)}")
        ap_port = pc_read(ctx.pm, ctx.game_flags + RECV_INDEX)
        recv_index = ap_port & 0xFFFF
        #loggerExt.warning(f"Processing items: {item_list} from {start_index} with recv_idx: {recv_index}")
        new_idx = start_index
        #if recv_index <= start_index:
        
        for item in item_list:
            netItem =  NetworkItem(*item)
            item_id = netItem.item
            ctx.recieved_items.add(item_id_to_name[item_id])
            new_idx += 1
            loggerExt.warning(f"item:{item_id_to_name[item_id]} start_idx: {start_index}, new_idx {new_idx}, recv_idx: {recv_index}")
            if recv_index >= new_idx:
                #loggerExt.warning(f"Skipping {item_id_to_name[item_id]}")
                continue
            #loggerExt.warning(f"Getting {item_id_to_name[item_id]}")
            if item_id in story_flag_items:
                item_data = item_data_table[story_flag_items[item_id]]

                if item_data.set_byte is not None:
                    pc_set_bit(ctx.pm, ctx.game_flags + item_data.set_byte, item_data.set_bit)
                    if item_id == 0x1C3B01: # Obsidian Bridge
                        pc_set_bit(ctx.pm, ctx.game_flags + 0x209, 2)
                        pc_set_bit(ctx.pm, ctx.game_flags + 0x209, 1, reset=True)
                if item_data.reset_byte is not None:
                    pc_set_bit(ctx.pm, ctx.game_flags + item_data.reset_byte, item_data.reset_bit, reset=True)
                # Handle Airship flags
                airship_base = ctx.ExpGainAd + 0x2C
                if story_flag_items[item_id] in airship_flags:
                    if ctx.open_airship:
                        set_airship_flags(ctx, airship_base, story_flag_items[item_id])
                    else:
                        #loggerExt.warning(f"items_recieved:{ctx.recieved_items}\n airship_connections_ladder:{airship_connections_ladder}")
                        for airship_item in airship_flags:
                            if airship_item in ctx.recieved_items:
                                if airship_connections[airship_item]:
                                    #loggerExt.warning(f"airship data:\nairship_connections[airship_item]:{airship_connections[airship_item]}\n airship_item:{airship_item}")
                                    if set(airship_connections[airship_item]).issubset(ctx.recieved_items):
                                        set_airship_flags(ctx, airship_base, airship_item)
                                    # elif set(airship_connections_ladder).issubset(ctx.recieved_items):
                                    #     set_airship_flags(ctx, airship_base, airship_item)
                                else:
                                    set_airship_flags(ctx, airship_base, airship_item)

            elif item_id in order_flag_items:
                match item_id:
                    case 0x1C3B11: #"Forging License":
                        give_furniture(ctx.pm, ctx.processes_base, "Forge",0x42,299,146)
                    case 0x1C3B12: # "Chemistry License":
                        give_furniture(ctx.pm, ctx.processes_base, "Chemistry Set",0x42,307,334)
                    case 0x1C3B13: # "Crafting License":
                        give_furniture(ctx.pm, ctx.processes_base, "Crafting Table",0x42,206,147)
                    case 0x1C3B10: # "EZ Cooking License":
                        give_furniture(ctx.pm, ctx.processes_base, "Mixer",0x42,99,251)
                        give_furniture(ctx.pm, ctx.processes_base, "Knife",0x42,99,297)
                        give_furniture(ctx.pm, ctx.processes_base, "Frying Pan",0x42,99,274)
                    case 0x1C3B14: # "Pro Cooking":
                        give_furniture(ctx.pm, ctx.processes_base, "Oven",0x42,99,221)
                        give_furniture(ctx.pm, ctx.processes_base, "Steamer",0x42,99,198)
                        give_furniture(ctx.pm, ctx.processes_base, "Pot",0x42,99,175)
                    case 0x1C3B2D: # Pandoras Mandate
                        pc_set_bit(ctx.pm, ctx.ExpGainAd + 26, 0)
                        pc_writeb(ctx.pm,ctx.processes_base+0x971EF, 0x1F)
                item_data = item_data_table[order_flag_items[item_id]]
                if item_data.set_byte is not None:
                    pc_set_bit(ctx.pm, ctx.ExpGainAd + item_data.set_byte, item_data.set_bit)
                if item_data.reset_byte is not None:
                    pc_set_bit(ctx.pm, ctx.ExpGainAd + item_data.reset_byte, item_data.reset_bit, reset=True)
            elif item_id in special_items:
                #try:
                #game_flags = pc_read_bytes(ctx.pm, ctx.game_flags, 0x33F)
                name = special_items[item_id]
                #loggerExt.warning(f"{name}")
                match name:
                    case "Forging Level Up" | "Chemistry Level Up"| "Cooking Level Up"| "Crafting Level Up":
                        skill_level = pc_read(ctx.pm, ctx.skill_base + crafting_level_offsets[name])
                        pc_write(ctx.pm, ctx.skill_base + crafting_level_offsets[name], skill_level + 5)
                    
                    #case "EZ Cooking License" | "Forging License" | "Chemistry License" | "Crafting License" | "Pro Cooking License":
                        #match name:
                    
                    case "Lucky Charm":
                        luck_level = pc_read(ctx.pm, ctx.ExpGainAd + 0x28) & 0xFFFF
                        luck_level += 100
                        if luck_level >= 1000:
                            luck_level = 1000

                        pc_writeb(ctx.pm, ctx.ExpGainAd + 0x28, luck_level & 0xFF)
                        pc_writeb(ctx.pm, ctx.ExpGainAd + 0x29, (luck_level & 0xFF00)>>8)
                        
                    
                    case "Progressive Farm":
                        farm_org = pc_read(ctx.pm, ctx.game_flags + 0x7E)
                        current_farms = reverse_bits(((farm_org & 0x1C) >> 2), 3)
                        current_farms += 1
                        if current_farms > 4:
                            current_farms = 4
                        new_farms = reverse_bits((current_farms), 3)
                        farm_bits = new_farms << 2
                        farm_byte = (farm_org & 0xE3) | farm_bits
                        pc_writeb(ctx.pm, ctx.game_flags + 0x7E, farm_byte)

                    case "Progressive Barn":
                        barn_int = pc_read(ctx.pm, ctx.game_flags + 0x66)
                        #barn_int = struct.unpack_from('<I', game_flags, 0x66)[0]
                        new_barns = expand_barns(barn_int)
                        pc_write(ctx.pm, ctx.game_flags + 0x66, new_barns)
                        
                    case "Popularity":
                        friend_levels = check_friendship_level(ctx.pm, ctx.friend_ptr)
                        for name, data in friend_levels.items():
                            friend_level = data[0]
                            friend_ptr = data[1]
                            if friend_level < 10:
                                friend_new_exp = friendship_ranks[friend_level + 1]
                                pc_write(ctx.pm, friend_ptr, friend_new_exp)
                    
                    case "Tabitha's Fodder Bin":
                        pc_write(ctx.pm, ctx.fodder_ptr,0xC350) # Give 50000 fodder
                        pc_write(ctx.pm, ctx.moneyPtr + 0xC, 0xC350) # Give 50000 fertilizer
                    
                    case "King's Order":
                        pc_set_bit(ctx.pm, ctx.game_flags + 0x254,0)
                        pc_write_bytes(ctx.pm,ctx.processes_base+0x21CE92,bytes([0xE9, 0xBC,0x00,0x00,0x00, 0x90])) # jmp +0xBC
                    
                    case "Iris's Song":
                        pc_set_bit(ctx.pm, ctx.game_flags + 0x254,1)
                        pc_write_bytes(ctx.pm,ctx.processes_base+0xED0A3,bytes([0xBE,0x00,0x00,0x00,0x00,0x90,0x90]))

                    
                        #pc_writeb(p, ctx.processes_base + 0x21CE13, 0x00)
                    case "Rune Sphere":
                        sphere_have = pc_readb(ctx.pm, ctx.game_flags + 0x1F8)
                        sphere_have += 1
                        ctx.rune_spheres = sphere_have
                        #loggerExt.warning(f"sphere_have: {sphere_have}, sphere_need: {ctx.fortress_sphere_need}")
                        pc_writeb(ctx.pm, ctx.game_flags + 0x1F8, sphere_have)
                        if sphere_have >= ctx.fortress_sphere_need:
                            pc_set_bit(ctx.pm, ctx.ExpGainAd + 0x2D, 3) # Floating Fortress
                        if sphere_have >= ctx.prana_sphere_need:
                            pc_set_bit(ctx.pm, ctx.game_flags + 0x21E, 4, reset=True)
            
            elif item_id in trap_items:
                name = trap_items[item_id]
                match name:
                    case "Strange Curse":
                        if ctx.acc_eff_ptr:
                            pc_set_bit(ctx.pm, ctx.acc_eff_ptr + 0xB, 2)
                    case "Status Trap":
                        pc_set_bit(ctx.pm, ctx.playerObj + 0xB4, random.randint(0,5))
            
            elif item_id in progressive_items:
                name = progressive_items[item_id]
                match name:
                    case "Progressive Weapon":
                        try:
                            ctx.wep_prog += 1
                            #loggerExt.warning(f"wep_prog: {ctx.wep_prog}")
                            if ctx.progressive_weapon == 1:
                                wep_type = ctx.start_weapon
                            else:
                                wep_type = random.choice(wep_cats)
                            #loggerExt.warning(f"wep_type: {wep_type}")
                            if wep_type.lower() == "random":
                                wep_type = random.choice(wep_cats)
                            give_progressive_item(ctx, wep_type, 0, 2)
                        except Exception as e:
                            loggerExt.critical(f"Error processing progressive weapon {e}\n{traceback.format_exc()}")
                    case "Progressive Armor":
                        ctx.armor_prog += 1
                        give_progressive_item(ctx, "Armor", 1, 2)
                    case "Progressive Shield":
                        ctx.shield_prog += 1
                        give_progressive_item(ctx, "Shield", 2, 0)
                    case "Progressive Shoes":
                        ctx.shoe_prog += 1
                        give_progressive_item(ctx, "Shoes", 3, 0)
                    case "Progressive Headgear":
                        ctx.head_prog += 1
                        give_progressive_item(ctx, "Headgear", 4, 0)
                    case "Progressive Accessory":
                        ctx.acc_prog += 1
                        give_progressive_item(ctx, "Accessories", 5, 0)

            elif item_id in physical_items:
                item_data = item_data_table[physical_items[item_id]]
                match item_data.item_type:
                    case "Bread" | "Crop" | "Dish" | "Fish":
                        inv_ptr = ctx.fridge_ptr
                    case "Spell":
                        inv_ptr = ctx.rune_abilites_ptr
                    case _:
                        inv_ptr = ctx.storage_box_ptr

                inv_bytes = get_inv_bytes(ctx.pm, inv_ptr)
                free_slot = find_free_inv_slot(inv_bytes, inv_ptr)
                        
                #try:
                #    
                #except Exception as e:
                #    loggerExt.critical(f"Error: {e}\n{traceback.format_exc()}")
                #loggerExt.warning(f"free slot: {free_slot}")
                if free_slot:
                    item_idx = item_data.item_id
                    item_amount = item_data.amount
                    if not item_amount:
                        item_amount = 1
                    amount_mask = item_amount << 11
                    item_write = item_idx | amount_mask
                    #loggerExt.warning(f"Getting item, storage base {hex(inv_ptr)}, free-slot: {hex(free_slot)}, item_idx: {hex(item_idx)}, amount: {hex(item_amount)}, amount_mask: {hex(amount_mask)}, item_write: {hex(item_write)}")
                    pc_write(ctx.pm, free_slot, item_write)
                else: # Free slot not found
                    pass
                #recv_index += 1
                #start_index += 1
            #loggerExt.warning(f"writing outport:{recv_index} -> {new_idx}")
            outport = (ap_port & 0xFFFF0000) | new_idx
            #loggerExt.warning(f"Finished items: new_idx: {new_idx}, recv_idx: {recv_index}, start_idx: {start_index}")
            pc_write(ctx.pm, ctx.game_flags + RECV_INDEX, outport)
    except Exception as e:
        loggerExt.critical(f"Error processing items {e}\n{traceback.format_exc()}")
