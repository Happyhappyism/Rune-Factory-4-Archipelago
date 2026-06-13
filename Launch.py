
from worlds.AutoWorld import World
from settings import get_settings
from .ips import parse_ips_file, patch
from .game_data import bundle_manifest, music_ids, hint_data, hint_appends
from .pc_ap_methods import pc_check_process
from .com_ap_methods import shuffle_dict

import Utils
import shutil
import struct
import random
import logging
import os
import pkgutil
import json
import traceback
import subprocess

from io import BytesIO
from pathlib import Path
import tkinter as tk
from tkinter import filedialog

logger = logging.getLogger("Rune Factory 4 Launcher")

def get_save_value(save_file_path, offset, byte_count=1):
    with open(save_file_path,'rb') as f:
        f.seek(offset)
        value = f.read(byte_count)
        int_value = int.from_bytes(value,"little")
    return int_value

def get_save_bytes(save_file_path, offset, byte_count=1):
    with open(save_file_path,'rb') as f:
        f.seek(offset)
        byte_list = f.read(byte_count)
    return byte_list

def check_files():
    install_path = get_settings().rf4_settings.rf4s_install_path
    if not os.path.isdir(install_path):
        install_path= Utils.user_path(install_path)
        while not os.path.exists(f"{install_path}//RF4S.exe"):
            logger.warning(f"RF4S.exe not found")
            install_path= Utils.user_path(install_path)

    ap_install_path = f"{install_path}//Archipelago"
    if not os.path.isdir(ap_install_path):
        os.mkdir(ap_install_path)
        
    bms_path = get_settings().rf4_settings.bms_path
    if not os.path.exists(bms_path):
        bms_path= Utils.user_path(bms_path)
        while not os.path.exists(f"{bms_path}//quickbms.exe"):
            logger.warning(f"quickbms.exe not found")
            bms_path= Utils.user_path(bms_path)
    savetext_path = os.path.join(bms_path, "rf4save.txt")
    if not os.path.exists(savetext_path):
        savetext_bytes = pkgutil.get_data(__name__, f"data/rf4save.txt")
        with open(savetext_path,"wb") as f:
            f.write(savetext_bytes)

    save_file_path = get_settings().rf4_settings.save_file_path
    if not os.path.exists(save_file_path):
        save_file_path = Utils.user_path(save_file_path)
        while not os.path.exists(f"{save_file_path}//rf4_sys.sav"):
            save_file_path= Utils.user_path(save_file_path)

    if not os.path.isdir(f"{install_path}//Bundle//mods"):
        os.mkdir(f"{install_path}//Bundle//mods")
    ap_mod_path = f"{install_path}//Bundle//mods//archipelago"
    if not os.path.isdir(ap_mod_path):
        os.mkdir(ap_mod_path)

    new_save, save_file_name = check_new_save()
    ap_save_path = f"{install_path}//Archipelago"
    save_file_path = os.path.join(ap_save_path,save_file_name)
    # with os.scandir(ap_mod_path) as it:
    #     if not any(it):
    patch_map_files(install_path,ap_mod_path)
    if new_save:
        logger.warning(f"save name:{new_save}")
        save_name = str(new_save)
        player_model = get_save_value(save_file_path, 0x20740, 2)

        save_params = save_name.split('_')
        player_name = save_params[3]
        drop_rate = int(save_params[5])
        monster_options = int(save_params[6])
        sound_options = int(save_params[7]) & 0x3
        trupin_option = int(save_params[7]) & 0x4
        element_option = int(save_params[7]) & 0x8
        modify_npc_params(install_path,ap_mod_path,drop_rate,monster_options, player_model)
        modify_sound(install_path, ap_mod_path, sound_options)
        if trupin_option:
            #ap_save_path = f"{install_path}//Archipelago//{new_save}"
            file_split = new_save.split("rf4_")[0]
            hint_file_path = f"{install_path}//Archipelago//{file_split}rf4_hints.json"
            logger.warning(f"hint_file_path:{hint_file_path}")
            if os.path.exists(hint_file_path):
                logger.warning(f"hint_file_path found")
                modify_dialog(install_path, ap_mod_path, player_name, hint_file_path)
            else:
                modify_dialog(install_path, ap_mod_path, player_name)
        if element_option:
            modify_spells(install_path, ap_mod_path)
        #modify_dialog(install_path, ap_mod_path)
    #patch_game_and_launch(install_path)
    if not pc_check_process("RF4S.exe"):
        subprocess.Popen([f"{install_path}/RF4S.exe"])
    player_name_bytes = get_save_bytes(save_file_path, 0x1D97A, 0x20)
    player_name_text = bytes([byte for byte in player_name_bytes if byte != 0]).decode("utf-8")
    return player_name_text
    

def write_turpin_hints(player_name, json_path= None):
    from .Locations import location_table, ship_loc_list, chest_loc_list, request_loc_list, friend_loc_list, tame_loc_list, outfit_loc_list
    root = tk.Tk()
    root.withdraw()
    if json_path:
        working_json_path = json_path
    else:
        working_json_path = filedialog.askopenfilename(title="Select AP generated hint .json file", filetypes=[("RF4 hint json", "*.json")])
    root.destroy()
    with open(working_json_path,'r') as f:
        hint_json = json.load(f)
    dialog_end = bundle_manifest["rf3mc.eng"][1] + 1
    dialog_offset = 0
    turpin_count = 0
    turpin_dialog = {}
    hl = f"\xEF\xBC\x90"
    for index, turpin_bytes in hint_data.items():
        #turpin_bytes = dialog.encode()
        if index in hint_appends:
            hint_item = hint_appends[index][0]
            conjuction = hint_appends[index][1]
            if hint_item in hint_json:
                hint_player = hint_json[hint_item][0]
                hint_location = hint_json[hint_item][1]
                if hint_player == player_name:
                    player_txt = "you"
                else:
                    player_txt = hint_player
                if hint_location in location_table:
                    loc_split = hint_location.split(" - ")
                    if hint_location in ship_loc_list:
                        diagetic = f"ship at least one [{hl}{loc_split[1]}{hl}]"
                    elif hint_location in chest_loc_list:
                        diagetic = f"search for treasure in {loc_split[0][:-6]}"
                    elif hint_location in request_loc_list:
                        diagetic = f"fulfill the request {hl}{loc_split[1]}{hl}"
                    elif hint_location in friend_loc_list:
                        villager = loc_split[1].split(" ")[0]
                        diagetic = f"become friends with {hl}{villager}{hl}"
                    elif hint_location in tame_loc_list:
                        diagetic = f"become friends with the monster {hl}{loc_split[1]}{hl}"
                    elif hint_location in outfit_loc_list:
                        diagetic = f"buy the outfit {hl}{loc_split[1]}{hl}"
                    else:
                        diagetic = f"{hl}{hint_location}{hl}"
                    hint_text = f"{player_txt}{conjuction}{diagetic}."
                else:
                    hint_text = f"{player_txt}{conjuction}{hl}{hint_location}{hl}."
            else:
                hint_text = f"check your pockets."
            hint_bytes = hint_text.encode()
            turpin_bytes += hint_bytes + b'\x00'
        elif index == 0x70b0:
            hint_text = hint_json["goal"]
            hint_bytes = hint_text.encode()
            turpin_bytes += hint_bytes + b'\x00'
        else:
            turpin_bytes +=  b'\x00'
            
        turpin_size = len(turpin_bytes)
        if turpin_size >= 64:
            try:
                offset = 64
                while turpin_bytes[offset] != 0x20 and offset < turpin_size-1:
                    offset+= 1
                if offset < turpin_size - 2:
                    mod_turpin_bytes = bytearray(turpin_bytes)
                    mod_turpin_bytes[offset] = 0xA
                    turpin_bytes = bytes(mod_turpin_bytes)
                    #struct.pack_into('B', turpin_bytes, offset, 0xA)
            except Exception as e:
                logger.warning(f"offset: {hex(offset)}, turpin_size:{turpin_size}\nturpin_bytes:{turpin_bytes}\n{e}")
        turpin_dialog[dialog_end + dialog_offset] = [index, turpin_bytes, turpin_size - 1]
        dialog_offset += turpin_size
        turpin_count += 1
    return turpin_dialog, turpin_count

        

def modify_dialog(install_path, ap_mod_path, player_name, hint_json=None):
    try:
        bundle_path = f"{install_path}/Bundle/bundleMain.mbundle"
        dialog_file_offset = bundle_manifest["rf3mc.eng"][0]
        dialog_file_size = bundle_manifest["rf3mc.eng"][1]
        dialog_bytes = get_bundle_bytes(bundle_path,dialog_file_offset,size=dialog_file_size)
        out_dialog_bytes = bytearray(dialog_bytes)
        out_dialog_bytes += b'\x00'

        turpin_hints, turpin_count = write_turpin_hints(player_name, hint_json)
        new_dialog_size = 0x1BAC3 + turpin_count
        #struct.pack_into(bytes, out_dialog_bytes, 4, new_dialog_size)
        struct.pack_into('<I', out_dialog_bytes, 4, new_dialog_size)
        for new_offset, data in turpin_hints.items():
            dialog_index = data[0]
            dialog_data_offset = (dialog_index * 0x8) + 0x8
            dialog_byte = data[1]
            dialog_size = data[2]
            struct.pack_into('<I', out_dialog_bytes, dialog_data_offset, dialog_size)
            struct.pack_into('<I', out_dialog_bytes, dialog_data_offset + 4, new_offset)
            out_dialog_bytes += dialog_byte
        with open(os.path.join(f"{ap_mod_path}/rf3mc.eng"), "wb") as param_file:
            param_file.write(out_dialog_bytes)
    except Exception as e:
        logger.critical(f"Error generating dialog mod: {e}\n{traceback.format_exc()}")

def modify_spells(install_path, ap_mod_path):

    bundle_path = f"{install_path}/Bundle/bundleMain.mbundle"
    magic_filename = "rf3ParamMagic.bin"
    magic_bytes = get_bundle_bytes(bundle_path,bundle_manifest[magic_filename][0],size=bundle_manifest[magic_filename][1])
    out_magic_bytes = bytearray(magic_bytes)

    shuffled_magic = shuffle_dict({
        0x81:[0x81, 0x6], # Magic/Fire
        0x82:[0x82, 0x7], # Magic/Water
        0x84:[0x84, 0x8], # Magic/Earth
        0x88:[0x88, 0x9], # Magic/Wind
        0x90:[0x90, 0xA], # Magic/Light
        0xA0:[0xA0, 0xB], # Magic/Dark
    })

    for spell_id in range(434):
        spell_offset = ((spell_id * 0x94) + 0x1C)
        attribute_offset = spell_offset + 0x1C
        type_offset = spell_offset + 0x90
        attribute_val = out_magic_bytes[attribute_offset]
        type_val = out_magic_bytes[type_offset]
        if attribute_val in shuffled_magic:
            out_magic_bytes[attribute_offset] = shuffled_magic[attribute_val][0]
            if type_val < 0xC and type_val > 0x5:
                out_magic_bytes[type_offset] = shuffled_magic[attribute_val][1]

    with open(os.path.join(f"{ap_mod_path}/rf3ParamMagic.bin"), "wb") as param_file:
        param_file.write(out_magic_bytes)


def modify_sound(install_path, ap_mod_path, sound_options):
    bundle_path = f"{install_path}/Bundle/bundleMain.mbundle"
    sound_file_offset = bundle_manifest["common_audio_data.bdat"][0]
    sound_file_size = bundle_manifest["common_audio_data.bdat"][1]
    sound_bytes = get_bundle_bytes(bundle_path,sound_file_offset,size=sound_file_size)

    out_sound_bytes = bytearray(sound_bytes)
    music_list = {}
    wav_list = {}
    strm_sfx_list = {}
    strm_other_list = {}
    data_base = 0x1100
    for idx, track_name in music_ids.items():
        #track_name = data[0]
        data_offset = (idx * 0xC) + data_base
        if track_name[0:3] == "SEQ" and track_name[-4:] == ".ogg":
            music_list[data_offset] = sound_bytes[data_offset:data_offset+0xC]
        elif (track_name[0:6] == "STRM_O" or track_name[0:6] == "STRM_F") and track_name[-4:] == ".ogg":
            strm_other_list[data_offset] = sound_bytes[data_offset:data_offset+0xC]
        elif track_name[0:2] == "SE" and track_name[-4:] == ".wav":
            wav_list[data_offset] = sound_bytes[data_offset:data_offset+0xC]
        elif track_name[0:4] == "STRM" and track_name[-4:] == ".ogg":
            strm_sfx_list[data_offset] = sound_bytes[data_offset:data_offset+0xC]

    if sound_options & 1: # Music shuffle enabled
        shuffled_music = shuffle_dict(music_list)
        for offset, data in shuffled_music.items():
            struct.pack_into('12s', out_sound_bytes, offset, data)

    if sound_options & 2:
        shuffled_wav = shuffle_dict(wav_list)
        for offset, data in shuffled_wav.items():
            struct.pack_into('12s', out_sound_bytes, offset, data)
        shuffled_strm = shuffle_dict(strm_sfx_list)
        for offset, data in shuffled_strm.items():
            struct.pack_into('12s', out_sound_bytes, offset, data)

    #logger.warning(f"music_list: {music_list}, \n\nwav_list:{wav_list}\n\nsound_bytes: {out_sound_bytes}")
    with open(os.path.join(f"{ap_mod_path}/common_audio_data.bdat"), "wb") as param_file:
        param_file.write(out_sound_bytes)

def modify_npc_params(install_path,ap_mod_path,drop_increase,monster_options, player_model):
    # Extract NPC Param bytes from bundle
    bundle_path = f"{install_path}/Bundle/bundleMain.mbundle"
    npc_tbl_offset = bundle_manifest["rf3NpcParam.bin"][0]
    npc_tbl_size = bundle_manifest["rf3NpcParam.bin"][1]
    npc_param_bytes = get_bundle_bytes(bundle_path,npc_tbl_offset,size=npc_tbl_size)
    # Increase base drop rates
    out_param_bytes = bytearray(npc_param_bytes)
    
    boss_list = [
        0xC8,0xC9,0xCA,0xCB,0xCC,0xCD,0xCE,0xCF,
        0xD0,0xD1,0xD2,0xD3,0xD4,0xD5,0xD6,0xD7,0xD8,0xD9,0xDA,0xDB,0xDC,0xDD,0xDF,
        0xE0,0xE1,0xE2,0xE3,0xE4,0xE5,0xE6,0xE7,0xE8,0xE9,0xEA,0xEB,0xEC,0xED,0xEE,0xEF,
        0xF0,0xF1,0xF2,0xF3,0xF4,0xF5,0xF9,0xFA,0xFB,0xFC,0xFD
    ]
    exclude_list = [
        0xDE, # Ancient Bone
        0xF6, # Heaven Gate
        0xF7, 
        0xF8,
        0xFE,0xFF,0x100,0x101,0x102,0x103,0x104,0x105,0x106,0x107,0x108,0x109,0x10A,0x10B,0x10C,0x10D,
        0x10E,0x10F,0x110,0x111,0x112,0x113,0x114,0x115,0x116,0x117,0x118,0x119,0x11A,0x11B,0x11C,0x11D,
        0x11E,0x11F,0x120,0x121,0x122,0x123,0x124,0x125,0x126,0x127,0x128,0x129,0x12A,0x12B,0x12C,0x12D,
        0x12E,0x12F,0x130,0x131,0x132,0x133,0x134,0x135,0x136,0x137,0x138,0x139,0x13A,0x13B,0x13C,0x13D,
        0x13E,0x13F,0x140,0x141,0x142,0x143,0x144,0x145,0x146,0x147,0x148,0x149,0x14A,0x14B,0x14C,0x14D,
        0x14E,0x14F,0x150,0x151,0x152,0x153,0x154,0x155,0x156,0x157,0x158,0x159,0x15A,0x15B,0x15C,0x15D,
        0x15E,0x15F,0x160,0x161,0x162,0x163,0x164,0x165,0x166, # Furniture
    ]
    if player_model:
        exclude_list.append(player_model)
    gate_list = [
        0x167,0x168,0x169,0x16A,0x16B,0x16C,0x16D,0x16E,0x16F,
        0x170,0x171,0x172,0x173,0x174,0x175,0x176,0x177,0x178,0x179,0x17A,0x17B,0x17C,0x17D,0x17E,0x17F,
        0x180,0x181,0x182,0x183,0x184,0x185,0x186,0x187
    ]
    param_shuffle = {
        #0x0: [],
        #0xFC: [],
        #0x100: [],
        #0x104: [],
        #0x108: [],
        #0x10C: [],
        #0x110: [], # Model, Texture
        #0x114: [],
        #0x118: [],
        #0x11C: [], # Speed?
        #0x124: [],
    }
    boss_params = { }
    if monster_options & 1:
        param_shuffle.update({0x110: []})
        boss_params.update({0x110: []})
    if monster_options & 2:
        param_shuffle.update({0x118: []})
        boss_params.update({0x118: []})
    if monster_options & 4:
        param_shuffle.update({0x10C: []})
        #boss_params.update({0x10C: []})

    # for param in range(0, 0x134, 4): 
    #     mask = 1 << (param >> 2)
    #     logger.warning(f"{hex(monster_params)} / {hex(mask)} / {hex(param)}")
    #     if monster_params & mask:
    #         logger.warning(f"monster param {hex(param)} matched")
    #         param_shuffle.update({param: []})
    #         boss_params.update({param: []})

    # Modify Trupin Hat
    #out_param_bytes[]

    for npc_index in range(0x30, 0xFE):
        npc_offset = (npc_index * 0x134) + 0x1C
        base_hp = struct.unpack_from('<I', npc_param_bytes, offset=npc_offset+0x120)[0]
        if base_hp == 0:
            continue
        if npc_index in exclude_list:
            continue
        if npc_index in gate_list:
            continue
        if npc_index in boss_list:
            for attr_offset, data_list in boss_params.items():
                data_list.append(struct.unpack_from('<I', npc_param_bytes, offset=npc_offset + attr_offset)[0])
        else:
            for attr_offset, data_list in param_shuffle.items():
                data_list.append(struct.unpack_from('<I', npc_param_bytes, offset=npc_offset + attr_offset)[0])
            
    for attr_offset, data_list in param_shuffle.items():
        random.shuffle(data_list)
    for attr_offset, data_list in boss_params.items():
        random.shuffle(data_list)

    for npc_index in range(0x30, 0x186):
        npc_offset = (npc_index * 0x134) + 0x1C
        base_hp = struct.unpack_from('<I', npc_param_bytes, offset=npc_offset+0x120)[0]
        if base_hp == 0:
            continue
        
        for x in range(4): # Modify Drop Rates
            drop_offset = npc_offset + 0xEC + (x*4)
            drop_rate = struct.unpack_from('<I', npc_param_bytes, offset=drop_offset)[0]
            if drop_rate == 0:
                continue
            drop_rate += drop_increase
            struct.pack_into('<I', out_param_bytes, drop_offset, drop_rate)
        if npc_index in exclude_list:
            continue
        if npc_index in gate_list:
            continue
        if npc_index in boss_list:
            try:
                for attr_offset, data_list in boss_params.items():
                    struct.pack_into('<I', out_param_bytes, npc_offset + attr_offset, data_list.pop(0))
            except Exception as e:
                logger.warning(f"Error shuffling monsters {e} index:{hex(npc_index)}\n{traceback.format_exc()}")
        else:
            try:
                for attr_offset, data_list in param_shuffle.items():
                    struct.pack_into('<I', out_param_bytes, npc_offset + attr_offset, data_list.pop(0))
            except Exception as e:
                logger.warning(f"Error shuffling monsters {e} index:{hex(npc_index)}\n{traceback.format_exc()}")
       

    with open(os.path.join(f"{ap_mod_path}/rf3NpcParam.bin"), "wb") as param_file:
        param_file.write(out_param_bytes)



def patch_game_and_launch(install_path):
    exe_path = os.path.join(install_path,"RF4S.exe")
    patched_path = os.path.join(install_path,"RF4S_AP.exe")
    patch_bytes = pkgutil.get_data(__name__, f"data/base_patch.ips")
    with open(exe_path, "rb") as ef:
        game_bytes = ef.read()
    with open(patched_path, "wb") as patched_executable:
        patched_executable.write(patch(game_bytes,parse_ips_file(patch_bytes)))
    subprocess.Popen(patched_path)

def get_bundle_bytes(bundle, offset, size=None):
    with open(bundle, "rb") as bundle_file:
        if not size:
            bundle_file.seek(offset+4)
            file_size = int.from_bytes(bundle_file.read(4),"little")
        else:
            file_size = size
        bundle_file.seek(offset)
        file_bytes = bundle_file.read(file_size)
    return file_bytes

def patch_map_files(install_path,ap_mod_path):
    #install_path = f"D:\\SteamLibrary\\steamapps\\common\\Rune Factory 4 Special\\Bundle"
    map_offset = {
        "MAP_DUNG_A01": 0x387DBF0D, # Yokmir Forest Entrance Warp
        "MAP_DUNG_A03": 0x9500654F, # Yokmir Forest Chipsqueek Guide
        "MAP_DUNG_A08": 0x1052EF0D0, # Yokmir Forest End Warp
        "MAP_DUNG_K63": 0x76114BC2, # Sechs Territory
        "MAP_FIELD_01": 0xA89E019,  # Selphia Fields Volkanon Logs
        "MAP_FIELD_19": 0x70D03BDE, # Volkanon Bridge
        "MAP_FIELD_29": 0x63DF9B8E, # Leon Karnak Gate
        "MAP_FIELD_45": 0x9907B694, # Rock Clearing?
        "MAP_FIELD_67": 0xE374D077, # Cerezo Bridge
        "MAP_FIELD_73": 0x157C8354, # # Silver Lake
        # "MAP_FIELD_98": 0x66CB273A, # Maya Bridge, no longer needed
    }
    bundle_path = f"{install_path}/Bundle/bundleMain.mbundle"
    #with open(bundle_path, "rb") as bundle_file:
    for map_name, map_offset in map_offset.items():
        map_bytes = get_bundle_bytes(bundle_path,map_offset)
        #bundle_file.seek(map_offset+4)
        #map_filesize = int.from_bytes(bundle_file.read(4),"little")
        #bundle_file.seek(map_offset)
        #map_bytes = bundle_file.read(map_filesize)
        map_path = f"{ap_mod_path}/{map_name}.rf4m"
        patch_bytes = pkgutil.get_data(__name__, f"data/patches/{map_name}.ips")
        with open(map_path, "wb") as map_file:
            map_file.write(patch(map_bytes,parse_ips_file(patch_bytes)))
        pass


def process_new_save(ap_save_file):
    from datetime import date
    save_file_name = Path(ap_save_file).name
    
    save_file_path = get_settings().rf4_settings.save_file_path
    logger.warning(f"ap_save_file = {ap_save_file}, save_file_path = {save_file_path} ")
    bms_path = get_settings().rf4_settings.bms_path
    save_slot = (ap_save_file.split(".")[0])[-2:]
    shutil.copy(ap_save_file, bms_path)
    command_list = [f"{bms_path}\\quickbms.exe", "-o", "rf4save.txt", save_file_name]
    subprocess.call(command_list, cwd=bms_path, shell=True)
    new_file_name = f"rf4_s{save_slot}.sav"
    os.rename(os.path.join(bms_path, save_file_name),os.path.join(bms_path, new_file_name))
    try:
        today = date.today()
        os.rename(os.path.join(save_file_path, new_file_name), os.path.join(save_file_path, f"{new_file_name}_{today.strftime("%Y-%m-%d")}.savbackup"))
    except Exception as e:
        logger.warning(f"No existing save to backup: {e}")  
    shutil.move(os.path.join(bms_path, new_file_name), os.path.join(save_file_path, new_file_name))
    write_sys_save(bms_path, save_file_name, save_slot, save_file_path)
    
    

def write_sys_save(bms_path, save_file_name, save_slot, save_file_path):
    bms_sys_path = os.path.join(bms_path,"rf4_sys.sav")
    slot_idx = int(save_slot) - 1
    player_name = save_file_name.split("_")[3]
    shutil.copy2(os.path.join(save_file_path,"rf4_sys.sav"), bms_sys_path)
    save_offset = 0x4F0 + (slot_idx * 0xA4)
    name_offset = save_offset + 0x14
    farm_offset = save_offset + 0x27
    base_save_bytes = bytes([
    0x00, 0x06, 0x02, 0x00, 0x01, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x40, 0x80, 
    0x00, 0x00, 0x00, 0x00,])
    farm_name_bytes = bytes([
    0x53, 0x65, 0x6C, 0x70, 0x68, 0x69, 0x61, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x4B, 0x61, 0x72, 0x64, 0x69, 0x61, 0x00, 
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
    0x00, 0x00, 0x41, 0x6C, 0x76, 0x61, 0x72, 0x6E, 0x61, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x53, 0x68, 0x61, 0x72, 0x61, 
    0x6E, 0x63, 0x65, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
    0x00, 0x00, 0x00, 0x00, 0x4E, 0x6F, 0x72, 0x61, 0x64, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
    ])
    player_string = ((player_name[0:12]).encode("utf-8")) + b'\x00'
    with open(bms_sys_path, "r+b") as f:
        f.seek(8)
        used_slots = int.from_bytes((f.read(4)),"little")
        mask = 1 << slot_idx
        new_slots = used_slots | mask
        f.seek(8)
        f.write(new_slots.to_bytes(4,'little'))
        f.seek(save_offset)
        f.write(base_save_bytes)
        f.seek(name_offset)
        f.write(player_string)
        f.seek(farm_offset)
        f.write(farm_name_bytes)
    command_list = [f"{bms_path}\\quickbms.exe", "-o", "rf4save.txt", "rf4_sys.sav"]
    subprocess.call(command_list, cwd=bms_path, shell=True)
    shutil.move(bms_sys_path, os.path.join(save_file_path, "rf4_sys.sav"))

def check_new_save():
    #save_path = get_settings().rf4_settings.save_file
    try:
        install_path = get_settings().rf4_settings.rf4s_install_path
        ap_save_path = f"{install_path}//Archipelago"
        old_run_path = f"{install_path}//Archipelago//Seeds"
        if not os.path.isdir(old_run_path):
            os.mkdir(old_run_path)
        bms_path = get_settings().rf4_settings.bms_path
        if not os.path.exists(bms_path):
            bms_path= Utils.user_path(bms_path)
        else:
            pobj = Path(ap_save_path)
            save_list = []
            for file in pobj.glob('*.sav'):
                save_list.append(file)
            if save_list:
                if len(save_list) == 1:
                    
                    save_file_name = save_list[0].name
                else:
                    root = tk.Tk()
                    root.withdraw()
                    working_save_path = filedialog.askopenfilename(title="Select AP generated .sav file",initialdir=ap_save_path, filetypes=[("RF4 Save", "*.sav")])
                    root.destroy()
                    save_file_name = os.path.basename(working_save_path).split('/')[-1]
                seed_name = save_file_name.split("_")[1]
                seed_list = os.listdir(old_run_path)
                save_file_path = os.path.join(ap_save_path,save_file_name)
                logger.warning(f"Save file found {save_file_path}")
                if seed_name in seed_list:
                    seed_path = os.path.join(old_run_path,seed_name)
                    ap_mod_path = f"{install_path}//Bundle//mods//archipelago"
                    shutil.copytree(seed_path, ap_mod_path, dirs_exist_ok=True)
                    return False, save_file_name 
                else:
                    process_new_save(save_file_path)
                    return save_file_name, save_file_name 
            else:
                logger.warning(f"No new save file found in rune4 directory, continueing run")
                return False, save_file_name 
                    
                    
    except Exception as e:
        logger.critical(f"Error checking for new save: {e}\n{traceback.format_exc()}")
        return False

def closing_functions(seed_name):
    try:
        install_path = get_settings().rf4_settings.rf4s_install_path
        old_run_path = f"{install_path}//Archipelago//Seeds"
        ap_mod_path = f"{install_path}//Bundle//mods//archipelago"
        if seed_name:
            seed_path = os.path.join(old_run_path,seed_name)
            if not os.path.isdir(old_run_path):
                os.mkdir(old_run_path)
            if not os.path.isdir(seed_path):
                os.mkdir(seed_path)
            shutil.copytree(ap_mod_path, seed_path, dirs_exist_ok=True)
        shutil.rmtree(ap_mod_path)
    except Exception as e:
        logger.critical(f"Error backing up seed mod {e}")