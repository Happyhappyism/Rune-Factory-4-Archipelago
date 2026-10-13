from typing import TYPE_CHECKING, List, Dict, Any, ClassVar
from .Save import write_hint_data, write_save_data
from worlds.Files import APPlayerContainer, AutoPatchRegister

import zipfile
import json
import io
import os
import Utils
import logging
logger = logging.getLogger("Rune Factory 4 Generate Output")
if TYPE_CHECKING:
    from . import RF4World

class RF4Container(APPlayerContainer):
    """
    This class defines the container file
    """

    game: str = "Rune Factory 4"
    


    def __init__(self, save_file: bytes, base_path: str, output_directory: str,
                player=None, player_name: str = "", out_file_name:str = None, hint_file: str = None, audio_excludes: str = None, server: str = ""):
        self.patch_data = save_file
        self.hint_file = hint_file
        self.audio_excludes = audio_excludes
        self.file_path = base_path
        self.out_file_name = out_file_name
        container_path = os.path.join(output_directory, base_path)
        self.patch_file_ending: str = ".aprf4s"
        # if "data" in kwargs:
        #     self.data = kwargs["data"]
        #     del kwargs["data"]

        super().__init__(container_path, player, player_name, server)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        """
        Write the contents of the container file.
        """
        save_file_name = f"{self.out_file_name}_rf4.sav"
        
        
        opened_zipfile.writestr(save_file_name, self.patch_data)

        if self.hint_file:
            hint_file_name = f"{self.out_file_name}_rf4_hints.json"
            opened_zipfile.writestr(hint_file_name, self.hint_file)

        if self.audio_excludes:
            excluded_audio_file = f"{self.out_file_name}_rf4_audioexclude.json"
            opened_zipfile.writestr(excluded_audio_file, self.audio_excludes)

        super().write_contents(opened_zipfile)

        # Record the data for the game under the key `plando`.
        #opened_zipfile.writestr("plando", b64encode(bytes(yaml.safe_dump(self.data, sort_keys=False), "utf-8")))


def generate_aprf4s(self:"RF4World", output_directory: str):

    #outfilepname = f"_P{self.player}"
    #outfilepname += f"_{self.multiworld.get_file_safe_player_name(self.player).replace(' ', '').replace('_','')}"

    out_file_name = self.multiworld.get_out_file_name_base(self.player)


    if self.options.start_weapon.value == "Random" or  self.options.start_weapon.value == "random":
        self.starting_weapon = self.random.choice([0x149,0x16A,0x18C,0x1C4,0x1AD,0x1FC,0x21B,0x1D8])
    else:
        self.starting_weapon = self.options.start_weapon.value


    ap_save_bytes = write_save_data(self)
    #save_file_name = f"{out_file_name}_rf4.sav"
    if self.options.trupin_hint:
        #hint_file_name = f"{out_file_name}_rf4_hints.json"
        hint_data = write_hint_data(self)
        hint_json = json.dumps(hint_data)
    else:
        hint_json = None
    #logger.info(f"audio exclude: {self.options.excluded_sfx.value} - {self.options.excluded_sfx}")
    if self.options.excluded_sfx.value:
        #excluded_audio_file = f"{out_file_name}_rf4_audioexclude.json"
        excluded_audio_list = self.options.excluded_sfx.value
        excluded_audio_json = json.dumps(excluded_audio_list)
    else:
        excluded_audio_json = None
    zip_file_name = f"{out_file_name}.aprf4s"
    zip_file_path = os.path.join(output_directory, zip_file_name)

    # zip_buffer = io.BytesIO()
    # with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
    #     zipf.writestr(save_file_name, ap_save_bytes)
    #     if self.options.trupin_hint:
    #         zipf.writestr(hint_file_name, hint_json)
    #     if self.options.excluded_sfx.value:
    #         zipf.writestr(excluded_audio_file, excluded_audio_json)

    # zip_bytes = zip_buffer.getvalue()
    # with open(zip_file_path, "wb") as f:
    #     f.write(zip_bytes)
    #mod_dir = os.path.join(output_directory, mod_name + "_" + Utils.__version__ + ".zip")
    aprf4s = RF4Container(ap_save_bytes, zip_file_path, output_directory, self.player, self.multiworld.get_file_safe_player_name(self.player),out_file_name, hint_json, excluded_audio_json)
    aprf4s.write()