from typing import TYPE_CHECKING, NamedTuple
import logging
import tkinter as tk
from tkinter import filedialog
import json
import traceback
import os
from .game_data import bundle_manifest


if TYPE_CHECKING:
    from .Launch import SeedFileInfo

class TrupinHint(NamedTuple):
    hint_bytes: bytes = None
    hint_size: int = None
    hint_offset: int = None
    hint_index: int = None

loggerDebug = logging.getLogger("Rune Factory 4 Debug")

hint_appends = {
    0x709f: ["Volkanon Axe"," should "],
    0x70a2: ["Obsidian Bridge"," decides to "],
    0x70a4: ["Chipsqueek Guide"," to "],
    0x70c8: ["Etherlink"," should "],
    0x70b4: ["Autumn Bridge"," must "],
    0x70bb: ["Cerezo Bridge"," has to "],
    0x70bd: ["Maya Bridge"," is supposed to "],
    0x70bf: ["Winters Grasp"," who should "],
    0x70a9: ["Forging License"," should "],
    0x70b9: ["Crafting License", " must "],
    0x70ac: ["EZ Cooking License", " needs to "],
    0x70ad: ["Pro Cooking License"," is required to "],
    0x70a6: ["Chemistry License", " should "],
    0x70c2: ["Fiersome Sun", " is to ", "\""],
    0x70c3: ["Aquaticus Rain", " achieves ", "\""]
    }


hint_data = {
    0x709f:	b'I\'ve heard to get \xEF\xBC\x8BVolkanon\'s Axe\xEF\xBC\x8B ',
    0x70a0:	b'What a strange place to leave your axe.',
	
    0x70a1:	b'Some travellers were talking about a bridge to a \xEF\xBC\x8Bscary place\xEF\xBC\x8B that appears if you fulfill a certain condition...',
    0x70a2:	b'They said it happens when ',
	
    0x70a3:	b'There was a really friendly \xEF\xBC\x8Bchipsqueak\xEF\xBC\x8B on the road today.',
    0x70a4:	b'It seemed to be waiting for ',
	
    0x70a5:	b'I came here hoping to find a medicine that can cure amnesia, but no one had any.',
    0x70a6:	b'I was told if I want to try making some, ',
    0x70a7:	b'I wonder if you can make medicine out of \xEF\xBC\x8BTurnips\xEF\xBC\x8B ?',
	
    0x70a8:	b'They say it\'s good luck to give travelers \xEF\xBC\x8Bturnips\xEF\xBC\x8B as presents.',
	
    0x70a9:	b'It seems to get a \xEF\xBC\x8BForging License\xEF\xBC\x8B in this town, ',
    0x70aa:	b'I wonder what that has to do with forging?',
	
    0x70ab:	b'I\'ve heard it requires a license to cook in this town. They say the exams are very strange.',
    0x70ac:	b'For the \xEF\xBC\x8BEZ Cooking License\xEF\xBC\x8B ',
    0x70ad:	b'For the \xEF\xBC\x8BPro version\xEF\xBC\x8B, ',
	
    0x70ae:	b'Welcome to the \xEF\xBC\x8BArchipelago Randomizer\xEF\xBC\x8B !',
    0x70af:	b'I wonder why it\'s called that? There don\'t seem to be any \xEF\xBC\x8Bislands\xEF\xBC\x8B here...',
    0x70b0:	b'I\'m told your win condition is ',
    0x70b1:	b'What could it mean?',
    0x70b2:	b'Anyway, good Luck!',
	
    0x70b3:	b'Have you heard of a place called \xEF\xBC\x8BAutumn Road\xEF\xBC\x8B ?',
    0x70b4:	b'To get there ',
    0x70b5:	b'How did I hear about this?',
    0x70b6:	b'I\'m not really sure either.',
    0x70b7:	b'How mysterious...',
	
    0x70b8:	b'Rumor has it to be a \xEF\xBC\x8Bgood craftsman\xEF\xBC\x8B, there\'s a special requirement you must fulfill.',
    0x70b9:	b' ',
	
    0x70ba:	b'I hear there\'s a special requirement to reach a place called \xEF\xBC\x8BSercerezo Hill\xEF\xBC\x8B .',
    0x70bb:	b'They say ',
	
    0x70bc:	b'There\'s an old legend about a \xEF\xBC\x8Bstrange place\xEF\xBC\x8B with monsters that grow stronger when hit.',
    0x70bd:	b'To reach it, ',
	
    0x70be:	b'When travelling today, I ran into some soldiers on the road.',
    0x70bf:	b'They said something about ',
    0x70c0:	b'They appeared to be building \xEF\xBC\x8Bsnowmen\xEF\xBC\x8B. How fun!',
	
    0x70c1:	b'If you close your eyes and listen closely, you can hear the Turnips\' voices.',
    0x70c2:	b'The voices whisper \"To find \xEF\xBC\x8BFiersome Sun\xEF\xBC\x8B ',
    0x70c3:	b'It seems \" \xEF\xBC\x8BAquaticus Rain\xEF\xBC\x8B will be yours if ',
	
    0x70c7:	b'Did you know there\'s a ritual needed to reach a place called \xEF\xBC\x8BLeon Karnak\xEF\xBC\x8B?',
    0x70c8:	b'Supposedly ',
    0x70c9:	b'I wonder why that is?'
}

def get_trupin_hint_file(seed_f:"SeedFileInfo"):
    try:
        file_split = seed_f.save_file_name.split("rf4")[0]
        seed_f.hint_file_path = f"{seed_f.install_path}//Archipelago//{file_split}rf4_hints.json"
    except Exception as e:
        loggerDebug.error(f"Error: {e}\n{traceback.format_exc()}")

def build_trupin_hint(seed_f:"SeedFileInfo",index, trupin_bytes, hint_json):
    from .Locations import location_table, ship_loc_list, chest_loc_list, request_loc_list, friend_loc_list, \
        tame_loc_list, outfit_loc_list, chest_data_table, shipment_data_table, tame_data_table
    # returns bytes for hint dialog
    chest_loc_to_reg = {data.loc_name: data.region for name, data in chest_data_table.items()}
    ship_loc_to_reg = {data.loc_name: data.region for name, data in shipment_data_table.items()}
    tame_loc_to_reg = {data.loc_name: data.region for name, data in tame_data_table.items()}
    hl = b'\xEF\xBC\x8B'
    if index in hint_appends:
        hint_item = hint_appends[index][0]
        conjuction = (hint_appends[index][1]).encode("utf-8")
        suffix = b""
        if len(hint_appends[index]) > 2:
            suffix = (hint_appends[index][2]).encode("utf-8")
        if hint_item in hint_json:
            hint_player = hint_json[hint_item][0]
            hint_location = hint_json[hint_item][1]
            if hint_player == seed_f.player_name:
                player_txt = (f"{seed_f.player_name}").encode("utf-8")
            else:
                player_txt = hint_player.encode("utf-8")
            if hint_location in location_table:
                loc_split = hint_location.split(" - ")
                loc_split_0 = (loc_split[0]).encode("utf-8")
                loc_split_1 = (loc_split[1]).encode("utf-8")
                hint_location_bytes = hint_location.encode("utf-8")
                if hint_location in ship_loc_list:
                    ship_region = ship_loc_to_reg[hint_location].encode("utf-8")
                    diagetic = b"ship something from "+hl+ship_region+hl
                elif hint_location in chest_loc_list:
                    chest_region = chest_loc_to_reg[hint_location].encode("utf-8")
                    diagetic = b"search for treasure in "+hl+chest_region+hl
                elif hint_location in request_loc_list:
                    diagetic = b"fulfill the request "+hl+loc_split_1+hl
                elif hint_location in friend_loc_list:
                    villager = (loc_split[1].split(" ")[0]).encode("utf-8")
                    diagetic = b"become friends with "+hl+villager+hl
                elif hint_location in tame_loc_list:
                    tame_region = tame_loc_to_reg[hint_location].encode("utf-8")
                    diagetic = b"become friends with a monster from "+hl+tame_region+hl
                elif hint_location in outfit_loc_list:
                    diagetic = b"buy an "+hl+b"outfit"+hl
                else:
                    diagetic = hl+hint_location_bytes+hl
                hint_text = player_txt+conjuction+diagetic+suffix+b"."
            else:
                hint_text = player_txt+ conjuction +hl+hint_location_bytes+hl +suffix+b"."
        else:
            hint_text = b"you check your pockets."
        #hint_bytes = hint_text.encode()
        trupin_bytes += hint_text + b'\x00'
    elif index == 0x70b0:
        hint_text = hint_json["goal"]
        hint_bytes = hint_text.encode()
        trupin_bytes += hint_bytes + b'\x00'
    else:
        trupin_bytes +=  b'\x00'
    trupin_size = len(trupin_bytes)
    
    if trupin_size >= 64:
        try:
            offset = 64
            while trupin_bytes[offset] != 0x20 and offset < trupin_size-1:
                offset+= 1
            if offset < trupin_size - 2:
                mod_trupin_bytes = bytearray(trupin_bytes)
                mod_trupin_bytes[offset] = 0xA
                trupin_bytes = bytes(mod_trupin_bytes)
        except Exception as e:
            loggerDebug.warning(f"offset: {hex(offset)}, trupin_size:{trupin_size}\ntrupin_bytes:{trupin_bytes}\n{e}")
    #return [index, trupin_bytes]
    return trupin_bytes
    
    

def write_trupin_hints(seed_f:"SeedFileInfo"):
    try:
        if seed_f.hint_file_path:
            working_json_path = seed_f.hint_file_path
        else:
            root = tk.Tk()
            root.withdraw()
            working_json_path = filedialog.askopenfilename(title="Select AP generated hint .json file", filetypes=[("RF4 hint json", "*.json")])
            seed_f.hint_file_path = working_json_path
            root.destroy()
        with open(working_json_path,'r') as f:
            hint_json = json.load(f)
        dialog_end = bundle_manifest["rf3mc.eng"][1] + 1
        dialog_offset = dialog_end
        trupin_dialog = b''
        #trupin_dialog = {}
        trupin_dialog_data = []
        for index, trupin_bytes in hint_data.items():
            trupin_hint = build_trupin_hint(seed_f, index, trupin_bytes, hint_json)
            trupin_dialog += trupin_hint
            trupin_size = len(trupin_hint)
            trupin_dialog_data.append(TrupinHint(hint_bytes=trupin_hint,hint_index=index,hint_size=trupin_size, hint_offset=dialog_offset ))
            dialog_offset += trupin_size
            #trupin_dialog[dialog_offset] = build_trupin_hint(seed_f, index, trupin_bytes, hint_json)
            #trupin_size = len(trupin_dialog[dialog_offset][1])
            

        return trupin_dialog, trupin_dialog_data
    except Exception as e:
        loggerDebug.error(f"Error: {e}\n{traceback.format_exc()}")