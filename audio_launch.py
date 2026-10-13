from pathlib import Path
from .game_data import bundle_manifest
from .com_ap_methods import shuffle_dict

import struct
import logging
import json
import os
import traceback
import shutil
import random

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .Launch import SeedFileInfo

loggerDebug = logging.getLogger("Rune Factory 4 Debug")

def pick_random_cust_sound(audio_path:Path, audio_list:list, cmusic_plist_dict:dict):
    try:
        cust_track_list = []
        for track in audio_path.iterdir():
            if track.suffix == ".ogg" or track.suffix == ".wav" or track.suffix == ".mp3":
                cust_track_list.append(track.name)
        random.shuffle(cust_track_list)
        for x in range(min(len(audio_list),len(cust_track_list))):
            picked_track = cust_track_list[x]
            replaced_track = audio_list[x]
            cmusic_plist_dict[picked_track] = replaced_track
    #return cmusic_plist_dict
    except Exception as e:
        loggerDebug.error(f"Error: {e}\n{traceback.format_exc()}")

def move_custom_music(seed_f:"SeedFileInfo", cmusic_plist_dict:dict):
    try:
        if cmusic_plist_dict:
            if not os.path.isdir(f"{seed_f.ap_mod_path}/Audio"):
                os.mkdir(f"{seed_f.ap_mod_path}/Audio")
            for picked_track, replaced_track in cmusic_plist_dict.items():
                picked_path = os.path.join(f"{seed_f.ap_rf4_base}/Music",picked_track)
                sfx_picked_path = os.path.join(f"{seed_f.ap_rf4_base}/SFX",picked_track)
                out_path = os.path.join(f"{seed_f.ap_mod_path}/Audio", replaced_track)
                if Path(picked_path).is_file():
                    shutil.copy(picked_path,out_path)
                elif Path(sfx_picked_path).is_file():
                    shutil.copy(sfx_picked_path,out_path)
                else:
                    loggerDebug.warning(f"Track: {picked_track} not found")
    except Exception as e:
                loggerDebug.error(f"Error: {e}\n{traceback.format_exc()}")


def mix_custom_music(seed_f:"SeedFileInfo"):
    try:
        move_custom_music(seed_f, create_cmusic_json(seed_f))
    except Exception as e:
        loggerDebug.error(f"Error: {e}\n{traceback.format_exc()}")

def create_cmusic_json(seed_f:"SeedFileInfo"):
    from .audio_data import music_data_table
    try:
        cmusic_plist_dict = {}
        exclude_audio_list = get_audio_exclude_file(seed_f)
        if seed_f.custmusic_option:
            custom_music_path = Path(f"{seed_f.ap_rf4_base}//Music")
            bgm_tracks = list(dict.fromkeys([data.name for id, data in music_data_table.items() if data.type == "BGM" and data.game == "RF4" and data.name not in exclude_audio_list]))
            random.shuffle(bgm_tracks)
            pick_random_cust_sound(custom_music_path, bgm_tracks, cmusic_plist_dict)
        if seed_f.custsfx_option:
            custom_sfx_path = Path(f"{seed_f.ap_rf4_base}//SFX")
            custom_fanfair_path = Path(f"{seed_f.ap_rf4_base}//Fanfair")
            sfx_list = list(dict.fromkeys([data.name for id, data in music_data_table.items() if data.type == "SFX" and data.name not in exclude_audio_list]))
            sfxl_list = list(dict.fromkeys([data.name for id, data in music_data_table.items() if data.type == "SFXL" and data.name not in exclude_audio_list]))
            random.shuffle(sfx_list)
            random.shuffle(sfxl_list)
            pick_random_cust_sound(custom_sfx_path, sfx_list, cmusic_plist_dict)
            pick_random_cust_sound(custom_fanfair_path, sfxl_list, cmusic_plist_dict)
        if cmusic_plist_dict:
            with open(f"{seed_f.ap_mod_path}/custom_music.json", "w") as fp:
                json.dump(cmusic_plist_dict, fp)
            return cmusic_plist_dict
        else:
            return None
    except Exception as e:
        loggerDebug.error(f"Error: {e}\n{traceback.format_exc()}")

def get_audio_exclude_file(seed_f:"SeedFileInfo"):
    try:
        file_split = seed_f.save_file_name.split("rf4")[0]
        audexclude_file_path = f"{seed_f.install_path}//Archipelago//{file_split}rf4_audioexclude.json"
        if os.path.isfile(audexclude_file_path):
            #seed_f.audexclude_file_path = audexclude_file_path
            with open(audexclude_file_path, 'r') as file:
                exclude_data = json.load(file)
            #os.remove(audexclude_file_path)
            return exclude_data
        else:
            return []
            #seed_f.audexclude_file_path = None
    except Exception as e:
        loggerDebug.error(f"Error: {e}\n{traceback.format_exc()}")

def build_randomized_base_music_lists():
    from .audio_data import music_data_table
    try:
        pass
    except Exception as e:
        loggerDebug.error(f"Error: {e}\n{traceback.format_exc()}")

def reload_custom_music(seed_f:"SeedFileInfo"):
    try:
        seed_plist = Path(f"{seed_f.seed_path}/custom_music.json")
        if seed_plist.is_file():
            with open(seed_plist, 'r', encoding='utf-8') as fp:
                cmusic_plist_dict = json.load(fp)
            move_custom_music(seed_f, cmusic_plist_dict)
    except Exception as e:
        loggerDebug.error(f"Error: {e}\n{traceback.format_exc()}")

def modify_sound(seed_f:"SeedFileInfo"):
    from .audio_data import music_ids
    from .Launch import get_bundle_bytes
    try:
        if seed_f.custmusic_option or seed_f.custsfx_option:
            mix_custom_music(seed_f)
        bundle_path = f"{seed_f.install_path}/Bundle/bundleMain.mbundle"
        sound_file_offset = bundle_manifest["common_audio_data.bdat"][0]
        sound_file_size = bundle_manifest["common_audio_data.bdat"][1]
        sound_bytes = get_bundle_bytes(bundle_path,sound_file_offset,size=sound_file_size)
        exclude_audio_list = get_audio_exclude_file(seed_f)
        out_sound_bytes = bytearray(sound_bytes)
        music_list = {}
        wav_list = {}
        strm_sfx_list = {}
        strm_other_list = {}
        data_base = 0x1100
        for idx, track_name in music_ids.items():
            #track_name = data[0]
            if music_ids[idx] in exclude_audio_list:
                continue
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