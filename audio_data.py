
from typing import TYPE_CHECKING, Set, Optional, List, Dict, Any, NamedTuple
import logging
import traceback
from .process_csv import parse_csv
class MusicData(NamedTuple):
    id: int = None
    name: str = None
    type: str = None
    format: str = None
    alias: str = None
    tags: list = None
    group: Optional[str] = None
    game: Optional[str] = None
    description: Optional[str] = None
    length: Optional[float] = None

logger = logging.getLogger("Rune Factory 4 Audio")

try:
    music_data_table = parse_csv("Rune Factory 4 AP - Audio")
    music_ids = {data.id: data.name for name, data in music_data_table.items() if data.name is not None}
    sfx_list = list(dict.fromkeys([data.name for id, data in music_data_table.items() if data.type == "SFX" or data.type == "SFXL"]))
    bgm_list = list(dict.fromkeys([data.name for id, data in music_data_table.items() if data.type == "BGM"]))
    valid_track_names = list(dict.fromkeys([data.name for id, data in music_data_table.items()]))
    audio_alias_list = {data.alias: data.name for id, data in music_data_table.items()}
    #logger.info(f"music_data_table: {music_data_table}\n\nmusic_ids: {music_ids}\n\nsfx_list:{sfx_list}\n\nbgm_list: {bgm_list}")
except Exception as e:
    logger.warning(f"Error parsing csv: {e}\n{traceback.format_exc()}")