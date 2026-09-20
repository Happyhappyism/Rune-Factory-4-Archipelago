from typing import TYPE_CHECKING
import logging
import tkinter as tk
from tkinter import filedialog
import json
import traceback
import os
from .game_data import bundle_manifest

if TYPE_CHECKING:
    from .Launch import SeedFileInfo

loggerDebug = logging.getLogger("Rune Factory 4 Debug")

hint_appends = {
    0x709f: ["Volkanon Axe"," should "],
    0x70a2: ["Obsidian Bridge"," does soemthing with "],
    0x70a4: ["Chipsqueek Guide"," to "],
    0x70c8: ["Etherlink"," should "],
    0x70b4: ["Autumn Bridge"," must "],
    0x70bb: ["Cerezo Bridge"," has to "],
    0x70bd: ["Maya Bridge"," is supposed to "],
    0x70bf: ["Winters Grasp"," and "],
    0x70a9: ["Forging License"," should "],
    0x70b9: ["Crafting License", " must "],
    0x70ac: ["EZ Cooking License", " needs to "],
    0x70ad: ["Pro Cooking License"," must "],
    0x70a6: ["Chemistry License", " should "],
    0x70c2: ["Fiersome Sun", " is to ", "\""],
    0x70c3: ["Aquaticus Rain", ' performs ', "\""]
    }


hint_data = {
    0x709f:	b'I\'ve heard to get + Volkanon\'s Axe + ',
    0x70a0:	b'What a strange place to leave your axe.',
	
    0x70a1:	b'Some travellers were talking about a bridge to a + scary place + that appears if you fulfill a certain condition...',
    0x70a2:	b'They say it happens when',
	
    0x70a3:	b'There was a really friendly + chipsqueak + on the road today.',
    0x70a4:	b'It was waiting for',
	
    0x70a5:	b'I came here hoping to find a medicine that can cure amnesia, but no one had any.',
    0x70a6:	b'I was told if I want to try making some,',
    0x70a7:	b'I wonder if you can make medicine out of + Turnips + ?',
	
    0x70a8:	b'They say it\'s good luck to give travelers + turnips + as presents.',
	
    0x70a9:	b'It seems to get a + Forging License + in this town,',
    0x70aa:	b'I wonder what that has to do with forging?',
	
    0x70ab:	b'Apparently it requires a license to cook in this town. I\'ve heard the exams are very strange.',
    0x70ac:	b'For the + EZ Cooking License + they make ',
    0x70ad:	b'For the Pro version,',
	
    0x70ae:	b'Welcome to the + Archipelago Randomizer + !',
    0x70af:	b'I wonder why it\'s called that? There don\'t seem to be any + islands + here...',
    0x70b0:	b'I\'m told your win condition is [Wincon]',
    0x70b1:	b'What could it mean?',
    0x70b2:	b'Anyway, good Luck!',
	
    0x70b3:	b'Have you heard of a place called + Autumn Road + ?',
    0x70b4:	b'Apparently, to get there',
    0x70b5:	b'How did I hear about this?',
    0x70b6:	b'That\'s a really good question.',
    0x70b7:	b'How mystical...',
	
    0x70b8:	b'I\'ve heard to be a good craftsman, there\'s a special requirement you must fulfill.',
    0x70b9:	b'Apparently it is',
	
    0x70ba:	b'Did you know there\'s a ritual needed to reach a place called + Sercerezo Hill + ?',
    0x70bb:	b'Apparently',
	
    0x70bc:	b'Legends say there is a strange place with monsters that grow stronger when hit.',
    0x70bd:	b'To reach it,',
	
    0x70be:	b'When travelling today, I ran into some soldiers on the field.',
    0x70bf:	b'They said something about',
    0x70c0:	b'It seemed they were building snowmen. How fun!',
	
    0x70c1:	b'If you close your eyes and listen closely, you can hear the Turnips\' voices.',
    0x70c2:	b'They say \"To find + Fiersome Sun +',
    0x70c3:	b'It seems \" + Aquaticus Rain + will be yours if',
	
    0x70c7:	b'Did you know there\'s a ritual needed to reach a place called + Leon Karnak +?',
    0x70c8:	b'Apparently',
    0x70c9:	b'I wonder why that is?'
}

def get_trupin_hint_file(seed_f:"SeedFileInfo"):
    try:
        file_split = seed_f.save_file_name.split("rf4")[0]
        seed_f.hint_file_path = f"{seed_f.install_path}//Archipelago//{file_split}rf4_hints.json"
    except Exception as e:
        loggerDebug.error(f"Error: {e}\n{traceback.format_exc()}")



def write_trupin_hints(seed_f:"SeedFileInfo"):
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
        trupin_count = 0
        trupin_dialog = {}
        hl = f"\xEF\xBC\x90"
        for index, trupin_bytes in hint_data.items():
            if index in hint_appends:
                hint_item = hint_appends[index][0]
                conjuction = hint_appends[index][1]
                suffix = ""
                if len(hint_appends) > 2:
                    suffix = hint_appends[index][1]
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
                        hint_text = f"{player_txt}{conjuction}{diagetic}{suffix}."
                    else:
                        hint_text = f"{player_txt}{conjuction}{hl}{hint_location}{hl}{suffix}."
                else:
                    hint_text = f"check your pockets."
                hint_bytes = hint_text.encode()
                trupin_bytes += hint_bytes + b'\x00'
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
            trupin_dialog[dialog_end + dialog_offset] = [index, trupin_bytes, trupin_size - 1]
            dialog_offset += trupin_size
            trupin_count += 1
        return trupin_dialog, trupin_count
    except Exception as e:
        loggerDebug.error(f"Error: {e}\n{traceback.format_exc()}")