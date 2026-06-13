import hashlib
import math
import os
import struct
#import random

from settings import get_settings
import Utils
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes

from worlds.AutoWorld import World
import logging

MD5Hash = [
    "34681b1bb27d999aacd505fa04ac6198", # Steam Executable
]

ROM_DATA_FREESPACE = 0xCA8000
ROM_NAME_ADR = ROM_DATA_FREESPACE + 0x10
PLAYER_NAME_ADR = ROM_DATA_FREESPACE + 0x30
OPTION_ADR = ROM_DATA_FREESPACE
logger = logging.getLogger("Rune Factory 4 Rom")

class RF4ProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Rune Factory 4"
    hash = MD5Hash
    patch_file_ending = ".aprune4"
    result_file_ending = ".exe"

    @classmethod
    def get_source_data(cls) -> bytes:
        from . import RF4World
        with open(RF4World.settings.exe_file, "rb") as infile:
            base_rom_bytes = bytes(infile.read())

        return base_rom_bytes
    
def write_tokens(world:World, patch:RF4ProcedurePatch):
    for j, b in enumerate(world.romName):
        patch.write_token(APTokenTypes.WRITE, ROM_NAME_ADR + j, struct.pack("<B", b))
    for j, b in enumerate(world.playerName):
        patch.write_token(APTokenTypes.WRITE, PLAYER_NAME_ADR + j, struct.pack("<B", b))
    patch.write_token(APTokenTypes.WRITE, OPTION_ADR + 0x0, bytes([world.options.game_goal.value]))
    patch.write_token(APTokenTypes.WRITE, OPTION_ADR + 0x1, bytes([world.options.death_link.value]))
    
    if world.options.death_link:
        patch.write_token(APTokenTypes.WRITE, OPTION_ADR + 0x2, bytes([0x01]))
    # if world.options.accept_multiple_requests:
    #     patch.write_token(APTokenTypes.WRITE, 0x1EB8A5, bytes([0x90, 0x90, 0x90]))
 

    patch.write_file("token_data.bin", patch.get_token_binary())


def get_base_rom_path(file_name: str="")-> str:
    if not file_name:
        file_name = get_settings().rf4_settings.exe_file
    if not os.path.exists(file_name):
        file_name= Utils.user_path(file_name)
    return file_name