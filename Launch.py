
from worlds.AutoWorld import World
from settings import get_settings
from .ips import parse_ips_file, patch
from .game_data import bundle_manifest, music_ids, hint_data, hint_appends
from .pc_ap_methods import pc_check_process, pc_process_resume
from .com_ap_methods import shuffle_dict

from typing import NamedTuple

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
import zipfile
import winreg

from io import BytesIO
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
import zlib

loggerClient = logging.getLogger("Rune Factory 4 Client")
loggerSeed = logging.getLogger("Rune Factory 4 Seed Info")
loggerDebug = logging.getLogger("Rune Factory 4 Debug")

class SysSavFile(NamedTuple):
    seed: str = ""
    player_name: str = ""
    display_list: str = ""
    goal_str: str = ""
    date: str  = ""
    slot: int = None

class SeedFileInfo:
    install_path: str = None # 'D:/SteamLibrary/steamapps/common/Rune Factory 4 Special'
    ap_rf4_base: str = None # 'install_path//Archipelago'
    old_run_path: str = None # 'D:/SteamLibrary/steamapps/common/Rune Factory 4 Special//Archipelago//Seeds'
    ap_mod_path: str = None # 'D:/SteamLibrary/steamapps/common/Rune Factory 4 Special//Bundle//mods//archipelago'
    ap_save_seed_path: str = None
    seed_name: str = None # '23056638599226981367'
    seed_path: str = None
    save_file_path_raw: str = f"{os.getenv('APPDATA')}\\Rune Factory 4 Special"
    save_file_path: str = None
    new_save: bool = False
    save_file_name: str = None # 'AP_[seed]_P1_[playername]_rf4.sav'
    ap_save_file: str = None
    ap_save_seed_final_path: str = None
    ap_file_info: str = None
    ap_save_dir: str = None
    save_slot: str = None
    ap_sys_save_path: str = None # 'D:/SteamLibrary/steamapps/common/Rune Factory 4 Special/Archipelago/Saves\\rf4_sys.sav'
    sys_file_path: str = None
    hint_file_path: str = None
    save_params: list = None
    player_name: str = None
    player_model: int = None
    drop_increase: int = None
    monster_options: int = None
    sound_options: int = None
    trupin_option: bool = None
    element_option: bool = None
    player_name_bytes = None
    #player_name_from_bytes: str = None
    save_create_date: str = None
    game_goal: int = None
    goal_str: str = None
    process_obj = None
    aprf4s_file_path = None # 'C:\\ProgramData\\Archipelago\\output\\AP_23056638599226981367_P1_It_rf4.aprf4s'

    @property
    def name(self):
        return self._name

    @name.setter  #  The name must match the property name exactly
    def name(self, value):
        self._name = value



def get_save_value(save_file_path, offset, byte_count=1):
    try:
        with open(save_file_path,'rb') as f:
            f.seek(offset)
            value = f.read(byte_count)
            int_value = int.from_bytes(value,"little")
        return int_value
    except Exception as e:
        loggerDebug.error(f"Error: {e}\n{traceback.format_exc()}")

def get_value_from_save(seed_f:SeedFileInfo, offset, size=1, file_path = None):
    try:
        if not file_path:
            read_file = seed_f.save_file_path
        else:
            read_file = file_path
        with open(read_file, "rb") as sf:
            sf.seek(offset)
            valbytes = sf.read(size)
        value = int.from_bytes(valbytes, "little")
        return value
    except Exception as e:
            loggerDebug.error(f"Error reading from save: {e}\n{traceback.format_exc()}")

def get_save_bytes(save_file_path, offset, byte_count=1):
    try:
        with open(save_file_path,'rb') as f:
            f.seek(offset)
            byte_list = f.read(byte_count)
        return byte_list
    except Exception as e:
        loggerDebug.error(f"Error: {e}\n{traceback.format_exc()}")

def compute_crc(file_bytes, start=None, end=None):
    try:
        if (start is not None) and (end is not None):
            crc = zlib.crc32(bytes(file_bytes[start:end])) & 0xFFFFFFFF
        else:
            crc = zlib.crc32(bytes(file_bytes[0:len(file_bytes)])) & 0xFFFFFFFF
        return crc
    except Exception as e:
        loggerDebug.error(f"Error: {e}\n{traceback.format_exc()}")

def set_seed_params(seed_f:SeedFileInfo):
    try:
        seed_f.drop_increase = get_value_from_save(seed_f, 0x1E65B)
        seed_f.monster_options = get_value_from_save(seed_f, 0x1E65C)
        extra_options = get_value_from_save(seed_f, 0x1E65D)
        seed_f.sound_options = extra_options & 0x3
        seed_f.trupin_option = bool(extra_options & 0x4)
        seed_f.element_option = bool(extra_options & 0x8)
    except Exception as e:
        print(f"An unexpected error occurred: {e}\n{traceback.format_exc()}")

def set_seedf_paths(seed_f:SeedFileInfo):
    try:
        seed_f.install_path = get_install_path()
        seed_f.ap_mod_path = f"{seed_f.install_path}//Bundle//mods//archipelago"
        seed_f.ap_rf4_base = f"{seed_f.install_path}//Archipelago"
        seed_f.ap_save_seed_path = f"{seed_f.install_path}/Archipelago/Saves"
        seed_f.old_run_path = f"{seed_f.install_path}//Archipelago//Seeds"
        
    except Exception as e:
        loggerDebug.error(f"Error: {e}\n{traceback.format_exc()}")

def create_missing_paths(seed_f:SeedFileInfo):
    ap_install_path = f"{seed_f.install_path}//Archipelago"
    if not os.path.isdir(ap_install_path):
        os.mkdir(ap_install_path)
    if not os.path.isdir(f"{seed_f.install_path}//Bundle//mods"):
        os.mkdir(f"{seed_f.install_path}//Bundle//mods")
    if not os.path.isdir(seed_f.ap_mod_path):
        os.mkdir(seed_f.ap_mod_path)
    if not os.path.isdir(seed_f.ap_save_seed_path):
        os.mkdir(seed_f.ap_save_seed_path)
    if not os.path.isdir(seed_f.old_run_path):
        os.mkdir(seed_f.old_run_path)
    seed_f.ap_sys_save_path = os.path.join(seed_f.ap_save_seed_path,"rf4_sys.sav")
    if not os.path.isfile(seed_f.ap_sys_save_path):
        sys_file_bytes = pkgutil.get_data(__name__, f"data/rf4_sys.sav")
        with open(seed_f.ap_sys_save_path, "wb") as f:
            f.write(sys_file_bytes)
    #plist_path = seed_f.ap_sys_save_path = os.path.join(seed_f.ap_save_seed_path,"Settings.plist")
    #if not os.path.isfile(plist_path):
    #    plist_org = os.path.join(f"{os.getenv('APPDATA')}\\Rune Factory 4 Special","Settings.plist")
    #    shutil.copy(plist_org,plist_path)

def launch_game_suspended(seed_f:SeedFileInfo):
    path = f"{seed_f.install_path}/RF4S.exe"
    CREATE_SUSPENDED = 0x00000004
    seed_f.process_obj = subprocess.Popen([path], creationflags=CREATE_SUSPENDED)

def get_install_path():
    common_install_paths = [
        "C:/Program Files (x86)/Steam/steamapps/common/Rune Factory 4 Special",
        "C:/Program Files/Steam/steamapps/common/Rune Factory 4 Special"
        "C:/SteamLibrary/steamapps/common/Rune Factory 4 Special",
        "D:/Program Files (x86)/Steam/steamapps/common/Rune Factory 4 Special",
        "D:/SteamLibrary/steamapps/common/Rune Factory 4 Special",
        "E:/SteamLibrary/steamapps/common/Rune Factory 4 Special",
        "Z:/home/deck/.steam/steam/steamapps/common/Rune Factory 4 Special",
        "Z:/home/deck/steam/steam/steamapps/common/Rune Factory 4 Special"
    ]
    for check_path in common_install_paths:
        if os.path.exists(check_path):
            exe_path = os.path.join(check_path, "RF4S.exe")
            if os.path.isfile(exe_path):
                #TODO: Ask user for install directory if not found and try again then raise file not found error
                return check_path

    install_path = get_settings().rf4_settings.rf4s_install_path
    if os.path.exists(install_path):
        return install_path

def get_file_date(file_path):
    from datetime import datetime
    try:
        file_path = Path(file_path)
        file_stat = file_path.stat()
        creation_time = file_stat.st_birthtime
        read_date = datetime.fromtimestamp(creation_time).strftime('%m/%d')
        return read_date
    except Exception as e:
        loggerDebug(f"An unexpected error occurred: {e}\n{traceback.format_exc()}")

def check_files(seed_f:SeedFileInfo):
    try:
        manifest_file = pkgutil.get_data(__name__, f"archipelago.json").decode("utf-8")
        manifest_json = json.loads(manifest_file)
        loggerDebug.info(f"Launching Rune Factory 4 Apworld v{manifest_json["world_version"]}")
        if not seed_f.save_file_path:
            seed_f.save_file_path = os.path.join(seed_f.ap_rf4_base, seed_f.save_file_name)
        loggerDebug.info(f"save name:{seed_f.seed_name}")
        seed_f.player_model = get_save_value(seed_f.save_file_path, 0x20740, 2)
        
        seed_f.game_goal = get_save_value(seed_f.save_file_path, 0x1E65A)
        seed_f.save_create_date = get_file_date(seed_f.save_file_path)
        if not seed_f.player_name:
            seed_f.player_name_bytes = get_save_bytes(seed_f.save_file_path, 0x1D97A, 0x12)
            seed_f.player_name = bytes([byte for byte in seed_f.player_name_bytes if byte != 0]).decode("utf-8")
    except Exception as e:
        loggerDebug(f"An unexpected error occurred: {e}\n{traceback.format_exc()}")

def modify_turpin_dialog(seed_f:SeedFileInfo):
    try:
        file_split = seed_f.save_file_name.split("rf4_")[0]
        seed_f.hint_file_path = f"{seed_f.install_path}//Archipelago//{file_split}rf4_hints.json"
        if os.path.exists(seed_f.hint_file_path):
            modify_dialog(seed_f)
        else:
            modify_dialog(seed_f)
    except Exception as e:
        loggerDebug.error(f"Error: {e}\n{traceback.format_exc()}")


    

def write_turpin_hints(seed_f:SeedFileInfo):
    from .Locations import location_table, ship_loc_list, chest_loc_list, request_loc_list, friend_loc_list, tame_loc_list, outfit_loc_list
    try:
        root = tk.Tk()
        root.withdraw()
        if seed_f.hint_file_path:
            working_json_path = seed_f.hint_file_path
        else:
            working_json_path = filedialog.askopenfilename(title="Select AP generated hint .json file", filetypes=[("RF4 hint json", "*.json")])
            seed_f.hint_file_path = working_json_path
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
                    if hint_player == seed_f.player_name:
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
                    loggerDebug.warning(f"offset: {hex(offset)}, turpin_size:{turpin_size}\nturpin_bytes:{turpin_bytes}\n{e}")
            turpin_dialog[dialog_end + dialog_offset] = [index, turpin_bytes, turpin_size - 1]
            dialog_offset += turpin_size
            turpin_count += 1
        return turpin_dialog, turpin_count
    except Exception as e:
        loggerDebug.error(f"Error: {e}\n{traceback.format_exc()}")


def modify_dialog(seed_f:SeedFileInfo):
    try:
        bundle_path = f"{seed_f.install_path}/Bundle/bundleMain.mbundle"
        dialog_file_offset = bundle_manifest["rf3mc.eng"][0]
        dialog_file_size = bundle_manifest["rf3mc.eng"][1]
        dialog_bytes = get_bundle_bytes(bundle_path,dialog_file_offset,size=dialog_file_size)
        out_dialog_bytes = bytearray(dialog_bytes)
        out_dialog_bytes += b'\x00'

        turpin_hints, turpin_count = write_turpin_hints(seed_f)
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
        with open(os.path.join(f"{seed_f.ap_mod_path}/rf3mc.eng"), "wb") as param_file:
            param_file.write(out_dialog_bytes)
    except Exception as e:
        loggerDebug.critical(f"Error generating dialog mod: {e}\n{traceback.format_exc()}")

def modify_spells(seed_f:SeedFileInfo):
    try:
        bundle_path = f"{seed_f.install_path}/Bundle/bundleMain.mbundle"
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

        with open(os.path.join(f"{seed_f.ap_mod_path}/rf3ParamMagic.bin"), "wb") as param_file:
            param_file.write(out_magic_bytes)
    except Exception as e:
            loggerDebug.error(f"Error: {e}\n{traceback.format_exc()}")


def modify_sound(seed_f:SeedFileInfo):
    try:
        bundle_path = f"{seed_f.install_path}/Bundle/bundleMain.mbundle"
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

        if seed_f.sound_options & 1: # Music shuffle enabled
            shuffled_music = shuffle_dict(music_list)
            for offset, data in shuffled_music.items():
                struct.pack_into('12s', out_sound_bytes, offset, data)

        if seed_f.sound_options & 2:
            shuffled_wav = shuffle_dict(wav_list)
            for offset, data in shuffled_wav.items():
                struct.pack_into('12s', out_sound_bytes, offset, data)
            shuffled_strm = shuffle_dict(strm_sfx_list)
            for offset, data in shuffled_strm.items():
                struct.pack_into('12s', out_sound_bytes, offset, data)

        with open(os.path.join(f"{seed_f.ap_mod_path}/common_audio_data.bdat"), "wb") as param_file:
            param_file.write(out_sound_bytes)
    except Exception as e:
        loggerDebug.error(f"Error: {e}\n{traceback.format_exc()}")

def modify_npc_params(seed_f:SeedFileInfo):
    try:
        # Extract NPC Param bytes from bundle
        bundle_path = f"{seed_f.install_path}/Bundle/bundleMain.mbundle"
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
        if seed_f.player_model:
            exclude_list.append(seed_f.player_model)
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
        if seed_f.monster_options & 1:
            param_shuffle.update({0x110: []})
            boss_params.update({0x110: []})
        if seed_f.monster_options & 2:
            param_shuffle.update({0x118: []})
            boss_params.update({0x118: []})
        if seed_f.monster_options & 4:
            param_shuffle.update({0x10C: []})
            #boss_params.update({0x10C: []})

        # for param in range(0, 0x134, 4):
        #     mask = 1 << (param >> 2)
        #     if monster_params & mask:
        #         param_shuffle.update({param: []})
        #         boss_params.update({param: []})

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
                drop_rate += seed_f.drop_increase
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
                    loggerDebug.warning(f"Error shuffling monsters {e} index:{hex(npc_index)}\n{traceback.format_exc()}")
            else:
                try:
                    for attr_offset, data_list in param_shuffle.items():
                        struct.pack_into('<I', out_param_bytes, npc_offset + attr_offset, data_list.pop(0))
                except Exception as e:
                    loggerDebug.warning(f"Error shuffling monsters {e} index:{hex(npc_index)}\n{traceback.format_exc()}")


        with open(os.path.join(f"{seed_f.ap_mod_path}/rf3NpcParam.bin"), "wb") as param_file:
            param_file.write(out_param_bytes)
    except Exception as e:
        loggerDebug.error(f"Error: {e}\n{traceback.format_exc()}")



def patch_game_and_launch(install_path):
    # Never called, unused
    exe_path = os.path.join(install_path,"RF4S.exe")
    patched_path = os.path.join(install_path,"RF4S_AP.exe")
    patch_bytes = pkgutil.get_data(__name__, f"data/base_patch.ips")
    with open(exe_path, "rb") as ef:
        game_bytes = ef.read()
    with open(patched_path, "wb") as patched_executable:
        patched_executable.write(patch(game_bytes,parse_ips_file(patch_bytes)))
    subprocess.Popen(patched_path)

def get_bundle_bytes(bundle, offset, size=None):
    try:
        with open(bundle, "rb") as bundle_file:
            if not size:
                bundle_file.seek(offset+4)
                file_size = int.from_bytes(bundle_file.read(4),"little")
            else:
                file_size = size
            bundle_file.seek(offset)
            file_bytes = bundle_file.read(file_size)
        return file_bytes
    except Exception as e:
        loggerDebug.error(f"Error: {e}\n{traceback.format_exc()}")

def patch_map_files(seed_f:SeedFileInfo):
    try:
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
        bundle_path = f"{seed_f.install_path}/Bundle/bundleMain.mbundle"
        for map_name, map_offset in map_offset.items():
            map_bytes = get_bundle_bytes(bundle_path,map_offset)
            map_path = f"{seed_f.ap_mod_path}/{map_name}.rf4m"
            patch_bytes = pkgutil.get_data(__name__, f"data/patches/{map_name}.ips")
            with open(map_path, "wb") as map_file:
                map_file.write(patch(map_bytes,parse_ips_file(patch_bytes)))
            pass
    except Exception as e:
        loggerDebug.error(f"Error: {e}\n{traceback.format_exc()}")

def apply_file_patch(seed_f:SeedFileInfo,file_name,bundle="bundleMain.mbundle"):
    try:
        bundle_path = f"{seed_f.install_path}/Bundle/{bundle}"
        file_offset = bundle_manifest[file_name][0]
        file_size = bundle_manifest[file_name][1]
        file_bytes = get_bundle_bytes(bundle_path,file_offset, file_size)
        file_out_path = f"{seed_f.ap_mod_path}/{file_name}"
        file_stem = file_name.split(".")[0]
        patch_bytes = pkgutil.get_data(__name__, f"data/patches/{file_stem}.ips")
        with open(file_out_path, "wb") as patched_file:
            patched_file.write(patch(file_bytes,parse_ips_file(patch_bytes)))
    except Exception as e:
        loggerDebug.error(f"Error patching file {file_name}: {e}\n{traceback.format_exc()}")

def additional_file_patching(seed_f:SeedFileInfo):
    try:
        files_to_patch = [
            "title_header_load_eng.texture"
        ]
        for file in files_to_patch:
            apply_file_patch(seed_f,file)
    except Exception as e:
        loggerDebug.error(f"Error patching file other files: {e}\n{traceback.format_exc()}")



def get_sav_list(path):
    try:
        pobj = Path(path)
        save_list = []
        for file in pobj.glob('*.sav'):
            save_list.append(file)
        return save_list
    except Exception as e:
        loggerDebug.error(f"Error: {e}\n{traceback.format_exc()}")

def prompt_delete_save(seed_f:SeedFileInfo):
    try:
        root = tk.Tk()
        root.withdraw()
        delete_slot = filedialog.askopenfilename(title="Select Delete an old run save file",initialdir=seed_f.ap_save_seed_path, filetypes=[("RF4 Save", "*.sav")])
        root.destroy()
        return int(Path(delete_slot).stem[-2:])
    except Exception as e:
        loggerDebug.error(f"Error: {e}\n{traceback.format_exc()}")

def find_save_slot(seed_f:SeedFileInfo):
    try:
        used_slots= 0
        with open(seed_f.ap_sys_save_path, "r+b") as f:
            f.seek(8)
            used_slots = int.from_bytes((f.read(4)),"little")
        for slot in range(0,20,1):
            if used_slots & (1 << slot) == 0:
                return slot + 1
        return prompt_delete_save(seed_f)
    except Exception as e:
            loggerDebug.error(f"Error processing new save: {e}\n{traceback.format_exc()}")

def process_new_save(seed_f:SeedFileInfo):
    try:
        seed_f.save_slot = find_save_slot(seed_f)
        slot_str = f"{seed_f.save_slot:02}"
        seed_f.ap_save_seed_final_path = os.path.join(seed_f.ap_save_seed_path, f"rf4_s{slot_str}.sav")
        shutil.copy(seed_f.save_file_path,seed_f.ap_save_seed_final_path)
        
    except Exception as e:
        loggerDebug.error(f"Error processing new save: {e}\n{traceback.format_exc()}")

def prompt_for_save(seed_f:SeedFileInfo):
    try:
        basedir = seed_f.ap_rf4_base
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(title="Select AP generated .aprf4s or .sav file",initialdir=basedir, filetypes=[("RF4 AP file", "*.aprf4s")]) # ,("RF4 Sav File", "*.sav")
        path_file = Path(file_path)
        root.destroy()
        # file_name = Path(working_save_path).name
        # ap_file_path = os.path.join(basedir, file_name)
        # if not os.path.isfile(ap_file_path):
        #     shutil.copy(working_save_path,ap_file_path)
        #return Path(working_save_path).name
        if path_file.suffix == ".aprf4s":
            seed_f.aprf4s_file_path = file_path
            process_aprf4s(seed_f)
        elif path_file.suffix == ".sav":
            seed_f.save_file_name = path_file.stem
            seed_f.save_file_path = file_path
            seed_f.seed_name = seed_f.save_file_name.split("_")[1]

    except Exception as e:
        loggerDebug.error(f"Error pormpting save: {e}\n{traceback.format_exc()}")

def get_save_file_extra_info(seed_f:SeedFileInfo):
    try:
        return
    except Exception as e:
        loggerDebug.error(f"Error getting file stats: {e}\n{traceback.format_exc()}")
        seed_f.save_create_date = ""
    return

def process_aprf4s(seed_f:SeedFileInfo):
    try:
        if seed_f.aprf4s_file_path:
            if not os.path.isdir(seed_f.ap_save_seed_path):
                os.mkdir(seed_f.ap_save_seed_path)
            with zipfile.ZipFile(seed_f.aprf4s_file_path, 'r') as archive:
                for file in archive.filelist:
                    if ".sav" in file.filename:
                        sav_file_name = file.filename
                archive.extractall(seed_f.ap_rf4_base)
            if sav_file_name:
                seed_f.save_file_name = sav_file_name
                seed_f.seed_name = seed_f.save_file_name.split("_")[1]
            else:
                prompt_for_save(seed_f)
        else:
            loggerDebug.warning(f"Error finding .aprf4s")
            prompt_for_save(seed_f)
    except Exception as e:
        loggerDebug.error(f"Error processing aprf4s: {e}\n{traceback.format_exc()}")

def get_goal_str(goal_int):
    match goal_int:
        case 0:
            goal_str = "Custom"
        case 1:
            goal_str = "Ethelberd"
        case 2:
            goal_str = "Rune Prana"
        case 3:
            goal_str = "Shipment Percentage"
        case 4:
            goal_str = "Nationized Baths"
        case 5:
            goal_str = "Eliza"
        case 6:
            goal_str = "Mariage"
        case 7:
            goal_str = "Rune Hunt"
        case 8:
            goal_str = "Homeowner"
        case _:
            loggerDebug.warning(f"Goal not found {goal_int}")
            goal_str = "Ethelberd"
    return goal_str

def build_seed_combo(seed_f:SeedFileInfo):
    try:
        save_list = []
        with open(seed_f.ap_sys_save_path, "rb") as sys_f:
            sys_f.seek(8)
            active_saves_bytes = sys_f.read(4)
            active_saves = int.from_bytes(active_saves_bytes, byteorder="little")
            saves_base = 0x4F0
            save_size = 0xA4
            name_offset = 0x14
            date_offset = 0x80
            seed_offset = 0x8B
            goal_offset = 0xA0
            for slot in range(20):
                if active_saves & (1 << slot):
                    slot_base = saves_base + (slot * save_size)
                    sys_f.seek(slot_base + name_offset)
                    player_bytes = sys_f.read(0x13)
                    player_name = bytes([byte for byte in player_bytes if byte != 0]).decode("utf-8")
                    #name_list.append(player_name)

                    sys_f.seek(slot_base + seed_offset)
                    seed_bytes = sys_f.read(0x14)
                    seed_str = bytes([byte for byte in seed_bytes if byte != 0]).decode("utf-8")
                    #seed_list.append(seed_str)

                    sys_f.seek(slot_base + goal_offset)
                    goal_byte = sys_f.read(1)
                    goal_int = int.from_bytes(goal_byte, byteorder="little")
                    goal_str = get_goal_str(goal_int)
                    
                    sys_f.seek(date_offset)
                    date_byte = sys_f.read(5)
                    date_str = date_byte.decode("utf-8")

                    display_str = f"{slot+ 1}: {seed_str} {date_str} {goal_str} {player_name}"
                    save_list.append(SysSavFile(seed=seed_str, player_name=player_name, goal_str=goal_str, slot=slot, date=date_str, display_list=display_str))
                else:
                    save_list.append(SysSavFile(slot=slot))
        return save_list

    except Exception as e:
        loggerDebug.error(f"Error building seed list: {e}\n{traceback.format_exc()}")
        return save_list
    
def prompt_for_seed(seed_f:SeedFileInfo):
    import traceback
    def on_user_close():
        if save_list:
            for save in reversed(save_list):
                if save.seed != "":
                    seed_f.player_name = save.player_name
                    seed_f.seed_name = save.seed
                    sel_idx = save_list.index(save)
                    save_name = f"rf4_s{(sel_idx +1):02d}.sav"
                    seed_f.save_file_name = save_name
                    seed_f.save_file_path = os.path.join(seed_f.ap_save_seed_path, save_name)
                    #root.destroy()
    def pick_seed():
        try:
            selection = listbox.curselection()
            if selection:
                sel_idx = selection[0]
                print(sel_idx)
                sel_seed = listbox.get(sel_idx)
                if sel_seed != "":
                    seed_f.player_name = save_list[sel_idx].player_name
                    seed_f.seed_name = save_list[sel_idx].seed
                    save_name = f"rf4_s{(sel_idx +1):02d}.sav"
                    seed_f.save_file_name = save_name
                    seed_f.save_file_path = os.path.join(seed_f.ap_save_seed_path, save_name)
                    root.destroy()
                    return
                else:
                    loggerDebug.warning(f"selected {sel_seed}")
            else:
                loggerDebug.warning(f"Nothing selected")
        except Exception as e:
                loggerDebug.warning(f"Error pormpting seed: {e}\n{traceback.format_exc()}")

    def new_seed():
        try:
            prompt_for_save(seed_f)
            root.destroy()
            return
        except Exception as e:
            loggerDebug.warning(f"Error pormpting seed: {e}\n{traceback.format_exc()}")
        
    try:
        save_list = build_seed_combo(seed_f)
        if save_list:
            root = tk.Tk()
            root.title("Select a Seed")
            root.geometry("300x425")
            root.protocol("WM_DELETE_WINDOW", on_user_close)
            root['bg'] = "#2E8B57"
            listbox = tk.Listbox(root, selectmode=tk.SINGLE, height=20, width=56, bg="#BAE8CE")
            listbox.pack(pady=10)
            for save in save_list:
                listbox.insert(tk.END, save.display_list)
            button_frame = tk.Frame(root, bg="#3B886F")
            button_frame.pack(pady=5)
            btn_select = tk.Button(button_frame, text="Select Seed", command=pick_seed,height=4,width= 16, bg="#4A9179")
            btn_new = tk.Button(button_frame, text="New Seed", command=new_seed,height=4, width= 16, bg="#4A9179")
            
            btn_select.pack(side=tk.LEFT, padx=5)
            btn_new.pack(side=tk.LEFT, padx=5)
            root.mainloop()
    except Exception as e:
        print(f"Error pormpting seed: {e}\n{traceback.format_exc()}")

def get_save_file(seed_f:SeedFileInfo):
    try:
        if seed_f.aprf4s_file_path:
            process_aprf4s(seed_f)
        else:
            #seed_f.save_file_name = prompt_for_save(seed_f)
            prompt_for_seed(seed_f)
        
    except Exception as e:
            loggerDebug.error(f"Error getting save file: {e}\n{traceback.format_exc()}")

def adjust_plist(seed_f:SeedFileInfo):
    try:
        pass
    except Exception as e:
        loggerDebug.error(f"Error modifying plist file: {e}\n{traceback.format_exc()}")
    

def write_sys_save(seed_f:SeedFileInfo):
    try:
        #seed_f.sys_file_path = os.path.join(seed_f.save_file_path_raw,f"rf4_sys.sav")
        shutil.copy(seed_f.ap_sys_save_path, os.path.join(seed_f.ap_save_seed_path, f"rf4_sys.backup"))
        slot_idx = int(seed_f.save_slot) - 1
        #player_name = seed_f.save_file_name.split("_")[3]
        save_offset = 0x4F0 + (slot_idx * 0xA4)
        name_offset = save_offset + 0x14
        farm_offset = save_offset + 0x27
        seed_name_offset = save_offset + 0x8B # Replace Norad farm name
        goal_offset = save_offset + 0xA0
        date_offset = save_offset + 0x80
        base_save_bytes = bytes([
        0x00, 0x06, 0x02, 0x00, 0x01, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x40, 0x80,
        0x00, 0x00, 0x00, 0x00,])
        farm_name_bytes = bytes([
        0x53, 0x65, 0x6C, 0x70, 0x68, 0x69, 0x61, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
        0x4B, 0x61, 0x72, 0x64, 0x69, 0x61, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
        0x41, 0x6C, 0x76, 0x61, 0x72, 0x6E, 0x61, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
        0x53, 0x68, 0x61, 0x72, 0x61, 0x6E, 0x63, 0x65, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
        0x4E, 0x6F, 0x72, 0x61, 0x64, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        ])
        seed_name_bytes = seed_f.seed_name.encode()
        date_bytes = seed_f.save_create_date.encode()
        player_string = ((seed_f.player_name[0:12]).encode("utf-8")) + b'\x00'
        with open(seed_f.ap_sys_save_path, "r+b") as f:
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
            f.seek(seed_name_offset)
            f.write(seed_name_bytes)
            f.seek(goal_offset)
            f.write(int.to_bytes(seed_f.game_goal))
            f.seek(date_offset)
            f.write(date_bytes)
            f.seek(8)
            file_bytes = f.read()
            crc = compute_crc(file_bytes)
            f.seek(4)
            f.write(crc.to_bytes(4,'little'))
    except Exception as e:
        os.rename(os.path.join(seed_f.ap_save_seed_path, f"rf4_sys.backup"), seed_f.ap_sys_save_path)
        loggerDebug.error(f"Error writing sys save file: {e}\n{traceback.format_exc()}")

def check_new_save(seed_f:SeedFileInfo):
    try:
        seed_list = os.listdir(seed_f.old_run_path)
        if seed_f.seed_name in seed_list:
            # check if run has been started before and if it has then, copy old mod files back into the bundle folder
            seed_f.new_save = False
            seed_f.seed_path = os.path.join(seed_f.old_run_path,seed_f.seed_name)
            shutil.copytree(seed_f.seed_path, seed_f.ap_mod_path, dirs_exist_ok=True)
            return
        else:
            seed_f.new_save = True
            
            return


    except Exception as e:
        loggerDebug.error(f"Error checking for new save: {e}\n{traceback.format_exc()}")
        return False

def set_aprf4s_reg():
    try:
        import winreg

        # .aprf4s -> APRF4SFile
        with winreg.CreateKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Classes\.aprf4s"
        ) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "APRF4SFile")

        # Define the file type
        with winreg.CreateKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Classes\APRF4SFile"
        ) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "APRF4S File")

        with winreg.CreateKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Classes\APRF4SFile\shell\open\command"
        ) as key:
            winreg.SetValueEx(
                key,
                "",
                0,
                winreg.REG_SZ,
                r'"C:\ProgramData\Archipelago\ArchipelagoLauncher.exe" "%1"'
            )
    except Exception as e:
        loggerDebug.critical(f"Error setting registry key {e}\n{traceback.format_exc()}")

def create_run_seed_dir(seed_f:SeedFileInfo):
    try:
        if seed_f.seed_name:
            seed_path = os.path.join(seed_f.old_run_path,seed_f.seed_name)
            if not os.path.isdir(seed_f.old_run_path):
                os.mkdir(seed_f.old_run_path)
            if not os.path.isdir(seed_path):
                os.mkdir(seed_path)
            shutil.copytree(seed_f.ap_mod_path, seed_path, dirs_exist_ok=True)
    except Exception as e:
        loggerDebug.error(f"Error moving seed mod {e}")

def closing_functions(seed_f:SeedFileInfo):
    try:
        if seed_f.seed_name:
            create_run_seed_dir(seed_f)
            shutil.rmtree(seed_f.ap_mod_path)
    except Exception as e:
        loggerDebug.error(f"Error backing up seed mod {e}")

def start_launch(seed_f:SeedFileInfo):
    try:
        set_seedf_paths(seed_f)
        create_missing_paths(seed_f)
        #if seed_f.aprf4s_file_path:
        get_save_file(seed_f)
        check_files(seed_f)
        check_new_save(seed_f)
        set_seed_params(seed_f)
        if seed_f.new_save:
            process_new_save(seed_f)
            create_run_seed_dir(seed_f)
            write_sys_save(seed_f)
            patch_map_files(seed_f)
            additional_file_patching(seed_f)
            modify_npc_params(seed_f)
            modify_sound(seed_f)
            if seed_f.element_option:
                modify_spells(seed_f)
            if seed_f.trupin_option:
                modify_turpin_dialog(seed_f)
            #get_save_file_extra_info(seed_f)
        launch_game_suspended(seed_f)
        set_aprf4s_reg()
    except Exception as e:
        print(f"An unexpected error occurred: {e}\n{traceback.format_exc()}")
    loggerDebug.info(f"seed_f: {vars(seed_f)}")