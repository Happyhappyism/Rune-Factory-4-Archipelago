
from typing import TYPE_CHECKING, Set, Optional, Dict, Any, NamedTuple
class MusicData(NamedTuple):
    id: int = None
    name: str = None
    type: str = None
    format: str = None
    group: Optional[str] = None
    game: Optional[str] = None
    description: Optional[str] = None
    length: Optional[float] = None

music_data_table = {
0xAB: MusicData(
id=0xAB,
name='ANOTHER_SCNARIO_SELECT.ogg',
type='Unknown',
game='RF4',
group='ANOTHER',
format='ogg',
length=0),

0xAD: MusicData(
id=0xAD,
name='JUSTM_BEST_END_KOHAKU.ogg',
type='Unknown',
game='RF4',
group='JUSTM',
format='ogg',
length=0),

0xAE: MusicData(
id=0xAE,
name='JUSTM_BEST_END_MARGARET.ogg',
type='Unknown',
game='RF4',
group='JUSTM',
format='ogg',
length=0),

0xAC: MusicData(
id=0xAC,
name='JUSTM_BEST_END.ogg',
type='Unknown',
game='RF4',
group='JUSTM',
format='ogg',
length=0),

0xAF: MusicData(
id=0xAF,
name='JUSTM_SCNARIO_SELECT.ogg',
type='Unknown',
game='RF4',
group='JUSTM',
format='ogg',
length=0),

0xB0: MusicData(
id=0xB0,
name='NX_COMMENT.ogg',
type='DemoBGM',
game='RF4',
group='NX',
format='ogg',
length=0),

0xB1: MusicData(
id=0xB1,
name='NX_STUFFROLL.ogg',
type='DemoBGM',
game='RF4',
group='NX',
format='ogg',
length=0),

0x0: MusicData(
id=0x0,
name='STRM_F_OP.ogg',
type='BGM',
game='RFF',
group='STRM',
format='ogg',
length=0.308125),

0x1: MusicData(
id=0x1,
name='STRM_F_SPRING.ogg',
type='BGM',
game='RFF',
group='STRM',
format='ogg',
length=0.31),

0x10: MusicData(
id=0x10,
name='STRM_F_DGN_TURUKUSA.ogg',
type='BGM',
game='RFF',
group='STRM',
format='ogg',
length=0.55),

0x100: MusicData(
id=0x100,
name='STRM_DOOR_STONE.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=1.2),

0x101: MusicData(
id=0x101,
name='STRM_ACTIVESEED_2.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=1.31),

0x102: MusicData(
id=0x102,
name='STRM_BS30_SHOUT.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=1.315),

0x103: MusicData(
id=0x103,
name='STRM_BS30_SCREAM.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.27),

0x104: MusicData(
id=0x104,
name='STRM_BS31_SHOUT.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.655),

0x105: MusicData(
id=0x105,
name='STRM_BS31_SCREAM.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.479645833333333),

0x106: MusicData(
id=0x106,
name='STRM_BS32_SHOUT.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=1.735),

0x107: MusicData(
id=0x107,
name='STRM_BS32_SCREAM.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.681396484375),

0x108: MusicData(
id=0x108,
name='STRM_BS33_SHOUT.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=1.315),

0x109: MusicData(
id=0x109,
name='STRM_BS33_SCREAM.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=4.99),

0x10A: MusicData(
id=0x10A,
name='STRM_BS34_SHOUT.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.47),

0x10B: MusicData(
id=0x10B,
name='STRM_BS34_SCREAM.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=1.985),

0x10C: MusicData(
id=0x10C,
name='STRM_BATH_1.ogg',
type='SFXL',
game='RF4',
group='STRM',
format='ogg',
length=0.39),

0x10D: MusicData(
id=0x10D,
name='STRM_BATH_2.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.8),

0x10E: MusicData(
id=0x10E,
name='STRM_FISH_HIT.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.55),

0x10F: MusicData(
id=0x10F,
name='STRM_HIT_ZANGEKI.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.91),

0x11: MusicData(
id=0x11,
name='STRM_F_DGN_YUKIKUSA.ogg',
type='BGM',
game='RFF',
group='STRM',
format='ogg',
length=1.43),

0x110: MusicData(
id=0x110,
name='STRM_HIT_YARI.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.875),

0x111: MusicData(
id=0x111,
name='STRM_HIT_HAMMER.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.79),

0x112: MusicData(
id=0x112,
name='STRM_HIT_FIRE.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=1.31),

0x113: MusicData(
id=0x113,
name='STRM_HIT_WATER.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.32470703125),

0x114: MusicData(
id=0x114,
name='STRM_KANSEI_A.ogg',
type='SFXL',
game='RF4',
group='STRM',
format='ogg',
length=0.39),

0x115: MusicData(
id=0x115,
name='STRM_KANSEI_B.ogg',
type='SFXL',
game='RF4',
group='STRM',
format='ogg',
length=0.43),

0x116: MusicData(
id=0x116,
name='STRM_WIND_PYU.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=1.3),

0x117: MusicData(
id=0x117,
name='STRM_GAAAN.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=1.195),

0x118: MusicData(
id=0x118,
name='STRM_DENGEKI.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.39),

0x119: MusicData(
id=0x119,
name='STRM_BM40_2_SANAGI_SHOUT.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=1.13),

0x11A: MusicData(
id=0x11A,
name='STRM_BM40_2_SHOUT.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=1.31),

0x11B: MusicData(
id=0x11B,
name='STRM_BM40_2_SCREAM.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=1.43),

0x11C: MusicData(
id=0x11C,
name='STRM_BM41_1_SHOUT.ogg',
type='SFXL',
game='RF4',
group='STRM',
format='ogg',
length=0.385),

0x11D: MusicData(
id=0x11D,
name='STRM_BM41_1_SCREAM.ogg',
type='SFXL',
game='RF4',
group='STRM',
format='ogg',
length=1.13),

0x11E: MusicData(
id=0x11E,
name='STRM_BM42_1_SCREAM1.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=1.305),

0x11F: MusicData(
id=0x11F,
name='STRM_BM42_1_SCREAM2.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.395),

0x12: MusicData(
id=0x12,
name='STRM_F_PINCH.ogg',
type='BGM',
game='RFF',
group='STRM',
format='ogg',
length=0.585),

0x120: MusicData(
id=0x120,
name='STRM_BM43_1_SHOUT.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.99),

0x121: MusicData(
id=0x121,
name='STRM_BM43_1_SCREAM.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.39),

0x122: MusicData(
id=0x122,
name='STRM_BM43_2_SHOUT.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.895),

0x123: MusicData(
id=0x123,
name='STRM_BM43_2_SCREAM.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.38),

0x124: MusicData(
id=0x124,
name='STRM_BM44_1_SHOUT.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=1.19),

0x125: MusicData(
id=0x125,
name='STRM_BM44_1_SCREAM.ogg',
type='SFXL',
game='RF4',
group='STRM',
format='ogg',
length=0.9),

0x126: MusicData(
id=0x126,
name='STRM_BM44_2_SHOUT.ogg',
type='SFXL',
game='RF4',
group='STRM',
format='ogg',
length=1.29),

0x127: MusicData(
id=0x127,
name='STRM_BM44_2_SCREAM.ogg',
type='SFXL',
game='RF4',
group='STRM',
format='ogg',
length=0.395),

0x128: MusicData(
id=0x128,
name='STRM_HIT_LASTBOOS.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.965),

0x129: MusicData(
id=0x129,
name='STRM_HIT_KUSA.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=2.97),

0x12A: MusicData(
id=0x12A,
name='STRM_HIT_WATER2.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=4.485),

0x12B: MusicData(
id=0x12B,
name='STRM_HIT_EARTH.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.78),

0x12C: MusicData(
id=0x12C,
name='STRM_HIT_WIND.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.8),

0x12D: MusicData(
id=0x12D,
name='STRM_HIT_DARK.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.23),

0x12E: MusicData(
id=0x12E,
name='STRM_HIT_LOVE.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.135),

0x12F: MusicData(
id=0x12F,
name='STRM_HIT_CRITICAL.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=2.41066666666666),

0x13: MusicData(
id=0x13,
name='STRM_F_VS_BOSS_NIWATORI.ogg',
type='BGM',
game='RFF',
group='STRM',
format='ogg',
length=0.94),

0x130: MusicData(
id=0x130,
name='STRM_DOOR_AKANAI.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.945),

0x131: MusicData(
id=0x131,
name='STRM_DOOR_LOCK.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.785),

0x132: MusicData(
id=0x132,
name='STRM_FUUSHA.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.785),

0x133: MusicData(
id=0x133,
name='STRM_GAANPIANO.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.785),

0x134: MusicData(
id=0x134,
name='STRM_WINDOW_CLASH.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.785),

0x135: MusicData(
id=0x135,
name='STRM_WIND_PYU_2.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.785),

0x136: MusicData(
id=0x136,
name='STRM_HIKOUSEN_TAKEOFF.ogg',
type='SFXL',
game='RF4',
group='STRM',
format='ogg',
length=0.785),

0x137: MusicData(
id=0x137,
name='STRM_ROONEY_EFFECT.ogg',
type='SFXL',
game='RF4',
group='STRM',
format='ogg',
length=0.785),

0x138: MusicData(
id=0x138,
name='SE_HAMMER_HIT.ogg',
type='SFX',
game='RF4',
group='SE',
format='ogg',
length=4.165),

0x139: MusicData(
id=0x139,
name='SE_DOOROPEN_2.ogg',
type='SFX',
game='RF4',
group='SE',
format='ogg',
length=0.885),

0x13B: MusicData(
id=0x13B,
name='SE_WORDS_M.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.815),

0x13C: MusicData(
id=0x13C,
name='SE_WORDS_F.ogg',
type='SFX',
game='RF4',
group='SE',
format='ogg',
length=0.095),

0x13D: MusicData(
id=0x13D,
name='SE_WORDS_O.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.36),

0x13E: MusicData(
id=0x13E,
name='SE_SWING00.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.36),

0x13F: MusicData(
id=0x13F,
name='SE_SWING01.ogg',
type='SFX',
game='RF4',
group='SE',
format='ogg',
length=0.235),

0x14: MusicData(
id=0x14,
name='STRM_F_VS_BOSS_SLIME.ogg',
type='BGM',
game='RFF',
group='STRM',
format='ogg',
length=0.285),

0x140: MusicData(
id=0x140,
name='SE_SWING01.ogg',
type='SFX',
game='RF4',
group='SE',
format='ogg',
length=0.31768798828125),

0x141: MusicData(
id=0x141,
name='SE_SWING03.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.61041259765625),

0x142: MusicData(
id=0x142,
name='SE_SWING03.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.765),

0x143: MusicData(
id=0x143,
name='SE_SWING00.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.255),

0x144: MusicData(
id=0x144,
name='SE_WALK_L.ogg',
type='SFX',
game='RF4',
group='SE',
format='ogg',
length=1.99),

0x145: MusicData(
id=0x145,
name='SE_WALK_R.ogg',
type='SFX',
game='RF4',
group='SE',
format='ogg',
length=1),

0x146: MusicData(
id=0x146,
name='SE_RUN_L.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.19),

0x147: MusicData(
id=0x147,
name='SE_RUN_R.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.95),

0x148: MusicData(
id=0x148,
name='SE_WALK_01_L.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=1.35),

0x149: MusicData(
id=0x149,
name='SE_WALK_01_L.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.99),

0x14A: MusicData(
id=0x14A,
name='SE_WALK_01_L.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=1.08),

0x14B: MusicData(
id=0x14B,
name='SE_WALK_01_L.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.3348388671875),

0x14C: MusicData(
id=0x14C,
name='SE_WALK_02_L.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.3348388671875),

0x14D: MusicData(
id=0x14D,
name='SE_WALK_02_L.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=3.11),

0x14E: MusicData(
id=0x14E,
name='SE_WALK_02_L.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=2.39),

0x14F: MusicData(
id=0x14F,
name='SE_WALK_02_L.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.465),

0x15: MusicData(
id=0x15,
name='STRM_F_VS_BOSS_ERIS.ogg',
type='BGM',
game='RFF',
group='STRM',
format='ogg',
length=2.335),

0x150: MusicData(
id=0x150,
name='SE_WALK_03_L.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.22503662109375),

0x151: MusicData(
id=0x151,
name='SE_WALK_03_L.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.275),

0x152: MusicData(
id=0x152,
name='SE_WALK_03_L.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0),

0x153: MusicData(
id=0x153,
name='SE_WALK_03_L.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0),

0x154: MusicData(
id=0x154,
name='SE_WALK_04_L.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.36444091796875),

0x155: MusicData(
id=0x155,
name='SE_WALK_04_L.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.300048828125),

0x156: MusicData(
id=0x156,
name='SE_WALK_04_L.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=7.56),

0x157: MusicData(
id=0x157,
name='SE_WALK_04_L.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.64),

0x158: MusicData(
id=0x158,
name='SE_WALK_05_L.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=1.225),

0x159: MusicData(
id=0x159,
name='SE_WALK_05_L.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.195),

0x15A: MusicData(
id=0x15A,
name='SE_WALK_05_L.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=1.400146484375),

0x15B: MusicData(
id=0x15B,
name='SE_WALK_05_L.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=1.66),

0x15C: MusicData(
id=0x15C,
name='SE_HORSE_L.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=3.215),

0x15D: MusicData(
id=0x15D,
name='SE_HORSE_L.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.995),

0x15E: MusicData(
id=0x15E,
name='SE_SWING01.ogg',
type='SFX',
game='RF4',
group='SE',
format='ogg',
length=1.19),

0x15F: MusicData(
id=0x15F,
name='SE_SWING00.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.87),

0x16: MusicData(
id=0x16,
name='STRM_F_VS_BOSS_WAGNER.ogg',
type='BGM',
game='RFF',
group='STRM',
format='ogg',
length=2.09),

0x160: MusicData(
id=0x160,
name='SE_HIT.ogg',
type='SFX',
game='RF4',
group='SE',
format='ogg',
length=2.01),

0x161: MusicData(
id=0x161,
name='SE_DOORCLOSE.ogg',
type='SFX',
game='RF4',
group='SE',
format='ogg',
length=1.63),

0x162: MusicData(
id=0x162,
name='SE_BS01_GUARD.ogg',
type='SFX',
game='RF4',
group='SE',
format='ogg',
length=1.355),

0x163: MusicData(
id=0x163,
name='SE_HUSUMA_OPEN.ogg',
type='SFX',
game='RF4',
group='SE',
format='ogg',
length=0.89),

0x164: MusicData(
id=0x164,
name='SE_HUSUMA_CLOSE.ogg',
type='SFX',
game='RF4',
group='SE',
format='ogg',
length=0.79),

0x165: MusicData(
id=0x165,
name='SE_SKILL_AUTOGUARD.ogg',
type='SFX',
game='RF4',
group='SE',
format='ogg',
length=1.39),

0x166: MusicData(
id=0x166,
name='SE_RUN_R.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=3.39),

0x167: MusicData(
id=0x167,
name='SE_NPC_HIT.ogg',
type='SFX',
game='RF4',
group='SE',
format='ogg',
length=0.16),

0x168: MusicData(
id=0x168,
name='SE_HAMMER_HIT.ogg',
type='SFX',
game='RF4',
group='SE',
format='ogg',
length=1.8),

0x169: MusicData(
id=0x169,
name='SE_ACTIVESEED_1.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=2.01),

0x16A: MusicData(
id=0x16A,
name='SE_PIYO_STEP.ogg',
type='SFX',
game='RF4',
group='SE',
format='ogg',
length=1.295),

0x16B: MusicData(
id=0x16B,
name='SE_BOKE2.ogg',
type='SFX',
game='RF4',
group='SE',
format='ogg',
length=0.185),

0x16C: MusicData(
id=0x16C,
name='SE_SHOP_END.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=2.585),

0x16D: MusicData(
id=0x16D,
name='SE_KISHIMI_DOOROPEN.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=2.585),

0x16E: MusicData(
id=0x16E,
name='SE_WALK_KISHIMI_L.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=1.43),

0x16F: MusicData(
id=0x16F,
name='SE_WALK_KISHIMI_R.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=1.61),

0x17: MusicData(
id=0x17,
name='STRM_F_VS_BOSS_KURAGE.ogg',
type='BGM',
game='RFF',
group='STRM',
format='ogg',
length=1.175),

0x170: MusicData(
id=0x170,
name='SE_WALK_KISHIMI_L.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=3.14),

0x171: MusicData(
id=0x171,
name='SE_WALK_KISHIMI_R.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.995),

0x172: MusicData(
id=0x172,
name='SE_WALK_WOOD_L.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.001007080078125),

0x173: MusicData(
id=0x173,
name='SE_WALK_WOOD_R.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.001007080078125),

0x174: MusicData(
id=0x174,
name='SE_WALK_WOOD_L.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.155),

0x175: MusicData(
id=0x175,
name='SE_WALK_WOOD_R.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.55),

0x176: MusicData(
id=0x176,
name='SE_WORDS_D.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=2.65),

0x177: MusicData(
id=0x177,
name='SE_WALK_FLOWER_L1.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.14801025390625),

0x178: MusicData(
id=0x178,
name='SE_WALK_FLOWER_R1.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.65),

0x179: MusicData(
id=0x179,
name='SE_WALK_FLOWER_L2.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.59),

0x17A: MusicData(
id=0x17A,
name='SE_WALK_FLOWER_R2.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.17816162109375),

0x17B: MusicData(
id=0x17B,
name='SE_WALK_FLOWER_L3.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=1.555),

0x17C: MusicData(
id=0x17C,
name='SE_WALK_FLOWER_R3.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=1.185),

0x17D: MusicData(
id=0x17D,
name='SE_CURSOR.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.9),

0x17E: MusicData(
id=0x17E,
name='SE_DECISION.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=1.12),

0x17F: MusicData(
id=0x17F,
name='SE_CANCEL.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=1.115),

0x18: MusicData(
id=0x18,
name='STRM_F_VS_BOSS_SNAKE.ogg',
type='BGM',
game='RFF',
group='STRM',
format='ogg',
length=1.17),

0x180: MusicData(
id=0x180,
name='SE_BAN.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.2),

0x181: MusicData(
id=0x181,
name='SE_CAMPOPEN.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=2.09),

0x182: MusicData(
id=0x182,
name='SE_CAMPCLOSE.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=2.72),

0x183: MusicData(
id=0x183,
name='SE_CAMPTAB.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.14),

0x184: MusicData(
id=0x184,
name='SE_CHATOPEN.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.41),

0x185: MusicData(
id=0x185,
name='SE_CHATCLOSE.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.2780625),

0x186: MusicData(
id=0x186,
name='SE_RINGOPEN.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.300375),

0x188: MusicData(
id=0x188,
name='SE_CHARGE_L.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.300375),

0x189: MusicData(
id=0x189,
name='SE_HOLD.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=4.875),

0x18A: MusicData(
id=0x18A,
name='SE_SET.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=1.03),

0x18B: MusicData(
id=0x18B,
name='SE_PUT.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.32),

0x18C: MusicData(
id=0x18C,
name='SE_TAKE.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.76318359375),

0x18D: MusicData(
id=0x18D,
name='SE_EAT.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.49072265625),

0x18E: MusicData(
id=0x18E,
name='SE_JUMP.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.47),

0x18F: MusicData(
id=0x18F,
name='SE_CRITICAL.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.995),

0x19: MusicData(
id=0x19,
name='STRM_F_LASTBOSS1.ogg',
type='BGM',
game='RFF',
group='STRM',
format='ogg',
length=0.11),

0x190: MusicData(
id=0x190,
name='SE_PIYORI.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.405),

0x191: MusicData(
id=0x191,
name='SE_DAMAGE.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.83),

0x192: MusicData(
id=0x192,
name='SE_ENEMY_DEAD.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.47),

0x193: MusicData(
id=0x193,
name='SE_CHGATK_SWORD.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.565),

0x194: MusicData(
id=0x194,
name='SE_MAGIC_FBALL.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=1.775),

0x195: MusicData(
id=0x195,
name='SE_MAGIC_FBALL_HIT.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.705),

0x196: MusicData(
id=0x196,
name='SE_MAGIC_EXPLOSION.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=1.95),

0x197: MusicData(
id=0x197,
name='SE_MAGIC_CRIMSON.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=1.05),

0x198: MusicData(
id=0x198,
name='SE_MAGIC_INFERNO.wav',
type='SFXL',
game='RF4',
group='SE',
format='wav',
length=0.89),

0x199: MusicData(
id=0x199,
name='SE_MAGIC_WLASER.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.695),

0x19A: MusicData(
id=0x19A,
name='SE_MAGIC_ABSORB.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.705),

0x19B: MusicData(
id=0x19B,
name='SE_MAGIC_ABSORB_HIT.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=2.575),

0x19C: MusicData(
id=0x19C,
name='SE_MAGIC_CURE.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=1.315),

0x19D: MusicData(
id=0x19D,
name='SE_MAGIC_STONE.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=2.05983333333333),

0x19E: MusicData(
id=0x19E,
name='SE_MAGIC_QUAKE.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.395),

0x19F: MusicData(
id=0x19F,
name='SE_MAGIC_METEA.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.885),

0x1A: MusicData(
id=0x1A,
name='STRM_F_LASTBOSS2.ogg',
type='BGM',
game='RFF',
group='STRM',
format='ogg',
length=1.005),

0x1A0: MusicData(
id=0x1A0,
name='SE_MAGIC_LMESSER.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.31),

0x1A1: MusicData(
id=0x1A1,
name='SE_MAGIC_LMESSER_HIT.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.30575),

0x1A2: MusicData(
id=0x1A2,
name='SE_MAGIC_MEDICATION.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.30575),

0x1A3: MusicData(
id=0x1A3,
name='SE_MAGIC_STURM.wav',
type='SFXL',
game='RF4',
group='SE',
format='wav',
length=0.30575),

0x1A4: MusicData(
id=0x1A4,
name='SE_CHGATK_SWORD.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.27581787109375),

0x1A5: MusicData(
id=0x1A5,
name='SE_CHGATK_SWORD.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.27581787109375),

0x1A6: MusicData(
id=0x1A6,
name='SE_CHGATK_SWORD.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.27581787109375),

0x1A7: MusicData(
id=0x1A7,
name='SE_CHGATK_SWORD.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.5449375),

0x1A8: MusicData(
id=0x1A8,
name='SE_CHGATK_SWORD.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.5449375),

0x1A9: MusicData(
id=0x1A9,
name='SE_CHGATK_SWORD.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=1.415),

0x1AA: MusicData(
id=0x1AA,
name='SE_LEVELUP.wav',
type='SFXL',
game='RF4',
group='SE',
format='wav',
length=1.43),

0x1AB: MusicData(
id=0x1AB,
name='SE_SKILLUP.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=2.425),

0x1AC: MusicData(
id=0x1AC,
name='SE_SYN_SUCCESS.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.19),

0x1AD: MusicData(
id=0x1AD,
name='SE_SYN_MISS.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.715),

0x1AE: MusicData(
id=0x1AE,
name='SE_RAGNA_SPIN.wav',
type='SFXL',
game='RF4',
group='SE',
format='wav',
length=0.29),

0x1AF: MusicData(
id=0x1AF,
name='SE_RADAR.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=2.72),

0x1B: MusicData(
id=0x1B,
name='STRM_F_ENDING.ogg',
type='BGM',
game='RFF',
group='STRM',
format='ogg',
length=1.405),

0x1B0: MusicData(
id=0x1B0,
name='SE_YAWN.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.295),

0x1B1: MusicData(
id=0x1B1,
name='SE_INN.wav',
type='SFXL',
game='RF4',
group='SE',
format='wav',
length=1.4),

0x1B2: MusicData(
id=0x1B2,
name='SE_BOSS_VANISH.wav',
type='SFXL',
game='RF4',
group='SE',
format='wav',
length=0.23),

0x1B3: MusicData(
id=0x1B3,
name='SE_MAGIC_QUAKE.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.18829345703125),

0x1B4: MusicData(
id=0x1B4,
name='SE_FLOWER.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.18829345703125),

0x1B5: MusicData(
id=0x1B5,
name='SE_SUMMON.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.18829345703125),

0x1B6: MusicData(
id=0x1B6,
name='SE_SPAWN.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.18829345703125),

0x1B7: MusicData(
id=0x1B7,
name='SE_DRAGON_FLAP.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.2607421875),

0x1B8: MusicData(
id=0x1B8,
name='SE_ATTACK_01.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.2607421875),

0x1B9: MusicData(
id=0x1B9,
name='SE_ATTACK_02.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.2607421875),

0x1BA: MusicData(
id=0x1BA,
name='SE_ATTACK_03.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.2607421875),

0x1BB: MusicData(
id=0x1BB,
name='SE_ATTACK_04.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.32415771484375),

0x1BC: MusicData(
id=0x1BC,
name='SE_MAGIC_SHINE.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.32415771484375),

0x1BD: MusicData(
id=0x1BD,
name='SE_MAGIC_ESCAPE.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.32415771484375),

0x1BE: MusicData(
id=0x1BE,
name='SE_MAGIC_ESCAPE_ARRV.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.32415771484375),

0x1BF: MusicData(
id=0x1BF,
name='SE_SKILL_POWERWAVE.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.44879150390625),

0x1C: MusicData(
id=0x1C,
name='STRM_O_OP.ogg',
type='BGM',
game='RFT',
group='STRM',
format='ogg',
length=0.44879150390625),

0x1C0: MusicData(
id=0x1C0,
name='SE_SKILL_SLASH.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.44879150390625),

0x1C1: MusicData(
id=0x1C1,
name='SE_SKILL_RUSHATTACK.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.44879150390625),

0x1C2: MusicData(
id=0x1C2,
name='SE_SKILL_SPIN.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.457763671875),

0x1C3: MusicData(
id=0x1C3,
name='SE_SKILL_RUSH.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.457763671875),

0x1C4: MusicData(
id=0x1C4,
name='SE_SKILL_STAB.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.457763671875),

0x1C5: MusicData(
id=0x1C5,
name='SE_SKILL_SPLASH.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.457763671875),

0x1C6: MusicData(
id=0x1C6,
name='SE_SKILL_SPINTOP.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.8070068359375),

0x1C7: MusicData(
id=0x1C7,
name='SE_SKILL_DHARMA.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.80792236328125),

0x1C8: MusicData(
id=0x1C8,
name='SE_PLAY_RUSH.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.8070068359375),

0x1C9: MusicData(
id=0x1C9,
name='SE_PLAY_COMMAND.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.8070068359375),

0x1CA: MusicData(
id=0x1CA,
name='SE_PLAY_SEARCH.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.8070068359375),

0x1CB: MusicData(
id=0x1CB,
name='SE_PLAY_SEARCH_SUCCESS.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.8070068359375),

0x1CC: MusicData(
id=0x1CC,
name='SE_PLAY_SEARCH_MISSTAKE.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.40869140625),

0x1CD: MusicData(
id=0x1CD,
name='SE_SUGOROKU_DICE_ROLL_00.wav',
type='SFXL',
game='RF4',
group='SE',
format='wav',
length=0.40869140625),

0x1CE: MusicData(
id=0x1CE,
name='SE_SUGOROKU_DICE_ROLL_01.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.421112060546875),

0x1CF: MusicData(
id=0x1CF,
name='SE_CRASH.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.421112060546875),

0x1D: MusicData(
id=0x1D,
name='STRM_O_TOWN_AM.ogg',
type='BGM',
game='RFT',
group='STRM',
format='ogg',
length=0.274),

0x1D0: MusicData(
id=0x1D0,
name='SE_SPAWN_SIGN.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.314875),

0x1D1: MusicData(
id=0x1D1,
name='SE_ATTACK_BREATH.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.222747802734375),

0x1D2: MusicData(
id=0x1D2,
name='SE_MAGIC_ROCKICE.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.222747802734375),

0x1D3: MusicData(
id=0x1D3,
name='SE_MAGIC_BOMB.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.253326416015625),

0x1D4: MusicData(
id=0x1D4,
name='SE_MAGIC_MISSILE.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.253326416015625),

0x1D5: MusicData(
id=0x1D5,
name='SE_SMOKY.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.36),

0x1D6: MusicData(
id=0x1D6,
name='SE_BS00_RINGO_POP.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.534058956916099),

0x1D7: MusicData(
id=0x1D7,
name='SE_BS00_RINGO_ROUND.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.07080078125),

0x1D8: MusicData(
id=0x1D8,
name='SE_BS00_RINGO_ATK.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.0637708333333333),

0x1D9: MusicData(
id=0x1D9,
name='SE_BS00_PUNCH.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.0136875),

0x13A: MusicData(
id=0x13A,
name='SE_WORDS_SEND.ogg',
type='Unknown',
game='RF4',
group='SE',
format='ogg',
length=0.03472900390625),

0x1DA: MusicData(
id=0x1DA,
name='SE_BS00_CATCH.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=1.195),

0x1DB: MusicData(
id=0x1DB,
name='SE_BS00_ATK.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.905),

0x1DC: MusicData(
id=0x1DC,
name='SE_BS00_TACKLE.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=28.7229375),

0x1DD: MusicData(
id=0x1DD,
name='SE_BS01_THRUST.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=70.2522291666666),

0x1DE: MusicData(
id=0x1DE,
name='SE_BS01_WALK.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=47.160375),

0x1DF: MusicData(
id=0x1DF,
name='SE_BS01_AMMO_UNI.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=57.9629791666666),

0x1E: MusicData(
id=0x1E,
name='STRM_O_TOWN_PM.ogg',
type='BGM',
game='RFT',
group='STRM',
format='ogg',
length=61.3177916666666),

0x1E0: MusicData(
id=0x1E0,
name='SE_BS01_AMMO_TARU.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=57.0190416666666),

0x1E1: MusicData(
id=0x1E1,
name='SE_BS01_BREATH.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=47.4666666666666),

0x1E2: MusicData(
id=0x1E2,
name='SE_BS02_TACKLE.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=63.145375),

0x1E3: MusicData(
id=0x1E3,
name='SE_BS02_BREATH.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=51.7859583333333),

0x1E4: MusicData(
id=0x1E4,
name='SE_BS02_PULL.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=65.0711666666666),

0x1E5: MusicData(
id=0x1E5,
name='SE_BS02_INVISI.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=55.8602291666666),

0x1E6: MusicData(
id=0x1E6,
name='SE_BS03_RUSH.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=84.0142291666666),

0x1E7: MusicData(
id=0x1E7,
name='SE_BS03_BREATHE.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=85.0251875),

0x1E8: MusicData(
id=0x1E8,
name='SE_BS04_PUNCH.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=69.2254583333333),

0x1E9: MusicData(
id=0x1E9,
name='SE_BS04_RUSH.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=63.2205833333333),

0x1EA: MusicData(
id=0x1EA,
name='SE_BS05_SCRATCH.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=82.864875),

0x1EB: MusicData(
id=0x1EB,
name='SE_BS05_BREATH.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=91.7850625),

0x1EC: MusicData(
id=0x1EC,
name='SE_BS06_ROUND.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=114.436354166666),

0x1ED: MusicData(
id=0x1ED,
name='SE_BS06_SEARCH.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=103.357833333333),

0x1EE: MusicData(
id=0x1EE,
name='SE_BS07_TAIL.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=144.9898125),

0x1EF: MusicData(
id=0x1EF,
name='SE_BS07_WING.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=69.8745),

0x1F: MusicData(
id=0x1F,
name='STRM_O_TOWN_HOKORA.ogg',
type='BGM',
game='RFT',
group='STRM',
format='ogg',
length=158.048479166666),

0x1F0: MusicData(
id=0x1F0,
name='SE_BS07_MOVE.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=112.638416666666),

0x1F1: MusicData(
id=0x1F1,
name='SE_BS07_PARSER.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=111.540375),

0x1F2: MusicData(
id=0x1F2,
name='SE_BS09_STAIL.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=100.686770833333),

0x1F3: MusicData(
id=0x1F3,
name='SE_BS09_FIRE.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=95.0603333333333),

0x1F4: MusicData(
id=0x1F4,
name='SE_BS09_SPECIAL.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=167.505833333333),

0x1F5: MusicData(
id=0x1F5,
name='SE_BOSS_HYPER.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=127.442145833333),

0x1F6: MusicData(
id=0x1F6,
name='SE_IREKAWARI.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=111.668541666666),

0x1F7: MusicData(
id=0x1F7,
name='SE_YOI.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=149.634020833333),

0x1F8: MusicData(
id=0x1F8,
name='SE_SUGOKUYOI.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=93.9213541666666),

0x1F9: MusicData(
id=0x1F9,
name='SE_START.wav',
type='SFXL',
game='RF4',
group='SE',
format='wav',
length=139.024166666666),

0x1FA: MusicData(
id=0x1FA,
name='SE_SYUURYOU.wav',
type='SFXL',
game='RF4',
group='SE',
format='wav',
length=99.3613541666666),

0x1FB: MusicData(
id=0x1FB,
name='SE_THROW.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=220.129770833333),

0x1FC: MusicData(
id=0x1FC,
name='SE_RAKKA.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=100.835895833333),

0x1FD: MusicData(
id=0x1FD,
name='SE_DASH.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=120.9109375),

0x1FE: MusicData(
id=0x1FE,
name='SE_TRANSFORM.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=96.1453541666666),

0x1FF: MusicData(
id=0x1FF,
name='SE_TRANSFORM_1.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=106.097270833333),

0x2: MusicData(
id=0x2,
name='STRM_F_SUMMER.ogg',
type='BGM',
game='RFF',
group='STRM',
format='ogg',
length=65.6853125),

0x20: MusicData(
id=0x20,
name='STRM_O_BAR.ogg',
type='BGM',
game='RFT',
group='STRM',
format='ogg',
length=61.1360625),

0x200: MusicData(
id=0x200,
name='SE_TRANSFORM_2.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=145.904020833333),

0x201: MusicData(
id=0x201,
name='SE_MOCO_ROLLING.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=96.8395416666666),

0x202: MusicData(
id=0x202,
name='SE_MIAGE_START.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=300.989979166666),

0x203: MusicData(
id=0x203,
name='SE_MIAGE_START.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=57.4002083333333),

0x204: MusicData(
id=0x204,
name='SE_HASU.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=42.5867083333333),

0x205: MusicData(
id=0x205,
name='SE_BIKKURI.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=105.0294375),

0x206: MusicData(
id=0x206,
name='SE_ONPU.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=107.708708333333),

0x207: MusicData(
id=0x207,
name='SE_ISSEN.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=104.2),

0x208: MusicData(
id=0x208,
name='SE_STAB.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=76.4526041666666),

0x209: MusicData(
id=0x209,
name='SE_SUPERSAIYAJIN.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=87.7825625),

0x20A: MusicData(
id=0x20A,
name='SE_FUKUROU.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=68.6347083333333),

0xB4: MusicData(
id=0xB4,
name='SEQ_FOUNTAIN.wav',
type='Enviroment',
game='RF4',
group='SEQ',
format='wav',
length=5.001),

0x20B: MusicData(
id=0x20B,
name='SE_SAVE.wav',
type='SFXL',
game='RF4',
group='SE',
format='wav',
length=1.795),

0x20C: MusicData(
id=0x20C,
name='SE_MONGET_OK.wav',
type='SFXL',
game='RF4',
group='SE',
format='wav',
length=62.0906875),

0x20D: MusicData(
id=0x20D,
name='SE_MONGET_NG.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=64.7520833333333),

0x20E: MusicData(
id=0x20E,
name='SE_WHEEL.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=96.022875),

0x20F: MusicData(
id=0x20F,
name='SE_TANUKI_DOWN.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=68.81425),

0x21: MusicData(
id=0x21,
name='STRM_O_MYROOMA.ogg',
type='BGM',
game='RFT',
group='STRM',
format='ogg',
length=100.5),

0x210: MusicData(
id=0x210,
name='SE_BS32_HOWL.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=78.654375),

0x211: MusicData(
id=0x211,
name='SE_BS34_WAVE.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=68.884625),

0x212: MusicData(
id=0x212,
name='SE_BS34_BIGBEAM.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=58.04125),

0x213: MusicData(
id=0x213,
name='SE_FROG_SEED.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=80.7753333333333),

0x214: MusicData(
id=0x214,
name='SE_GAAAN.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=117.729333333333),

0x215: MusicData(
id=0x215,
name='SE_BOKE.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=80.4224583333333),

0x216: MusicData(
id=0x216,
name='SE_TSUKKOMI.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=97.7216666666666),

0x217: MusicData(
id=0x217,
name='SE_TOHOHO.wav',
type='SFXL',
game='RF4',
group='SE',
format='wav',
length=126.0418125),

0x218: MusicData(
id=0x218,
name='SE_LEVELUP_OUJI.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=143.274708333333),

0x219: MusicData(
id=0x219,
name='SE_ONPU_2.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=79.2571458333333),

0x21A: MusicData(
id=0x21A,
name='SE_CLOCK.wav',
type='SFXL',
game='RF4',
group='SE',
format='wav',
length=35.07425),

0x21B: MusicData(
id=0x21B,
name='SE_FIRESTORM.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=63.4422916666666),

0x21C: MusicData(
id=0x21C,
name='SE_DAMAGE_2.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=81.0263541666666),

0x22: MusicData(
id=0x22,
name='STRM_O_MYROOMB.ogg',
type='BGM',
game='RFT',
group='STRM',
format='ogg',
length=78.549),

0x23: MusicData(
id=0x23,
name='STRM_O_SPRING.ogg',
type='BGM',
game='RFT',
group='STRM',
format='ogg',
length=98.5276875),

0x24: MusicData(
id=0x24,
name='STRM_O_SUMMER.ogg',
type='BGM',
game='RFT',
group='STRM',
format='ogg',
length=52.19975),

0x25: MusicData(
id=0x25,
name='STRM_O_FALL.ogg',
type='BGM',
game='RFT',
group='STRM',
format='ogg',
length=59.064375),

0xBA: MusicData(
id=0xBA,
name='SEQ_RAIN.wav',
type='Enviroment',
game='RF4',
group='SEQ',
format='wav',
length=4.01347916666666),

0xB6: MusicData(
id=0xB6,
name='SEQ_RIVER.wav',
type='Enviroment',
game='RF4',
group='SEQ',
format='wav',
length=3.43370833333333),

0x26: MusicData(
id=0x26,
name='STRM_O_WINTER.ogg',
type='BGM',
game='RFT',
group='STRM',
format='ogg',
length=96.195),

0x27: MusicData(
id=0x27,
name='STRM_O_GOBLIN.ogg',
type='BGM',
game='RFT',
group='STRM',
format='ogg',
length=136.711791666666),

0x28: MusicData(
id=0x28,
name='STRM_O_DGN_JUNGLE.ogg',
type='BGM',
game='RFT',
group='STRM',
format='ogg',
length=10.23),

0xB5: MusicData(
id=0xB5,
name='SEQ_SHORE.wav',
type='Enviroment',
game='RF4',
group='SEQ',
format='wav',
length=18.2243541666666),

0xB9: MusicData(
id=0xB9,
name='SEQ_SNOW.wav',
type='Enviroment',
game='RF4',
group='SEQ',
format='wav',
length=15.559625),

0x29: MusicData(
id=0x29,
name='STRM_O_DGN_FIREISLAND.ogg',
type='BGM',
game='RFT',
group='STRM',
format='ogg',
length=65.3162708333333),

0x2A: MusicData(
id=0x2A,
name='STRM_O_DGN_EARTH.ogg',
type='BGM',
game='RFT',
group='STRM',
format='ogg',
length=71.0000625),

0x2B: MusicData(
id=0x2B,
name='STRM_O_DGN_FIRE.ogg',
type='BGM',
game='RFT',
group='STRM',
format='ogg',
length=134.59375),

0x2C: MusicData(
id=0x2C,
name='STRM_O_DGN_WATER.ogg',
type='BGM',
game='RFT',
group='STRM',
format='ogg',
length=71.730875),

0x2D: MusicData(
id=0x2D,
name='STRM_O_DGN_WIND.ogg',
type='BGM',
game='RFT',
group='STRM',
format='ogg',
length=82.9087291666666),

0x2E: MusicData(
id=0x2E,
name='STRM_O_BATTLE_GIANT.ogg',
type='BGM',
game='RFT',
group='STRM',
format='ogg',
length=65.676),

0x2F: MusicData(
id=0x2F,
name='STRM_O_BOSS1.ogg',
type='BGM',
game='RFT',
group='STRM',
format='ogg',
length=65.7996041666666),

0x3: MusicData(
id=0x3,
name='STRM_F_FALL.ogg',
type='BGM',
game='RFF',
group='STRM',
format='ogg',
length=47.5933958333333),

0x30: MusicData(
id=0x30,
name='STRM_O_BOSS2.ogg',
type='BGM',
game='RFT',
group='STRM',
format='ogg',
length=85.7721875),

0x31: MusicData(
id=0x31,
name='STRM_O_LASTBOSS.ogg',
type='BGM',
game='RFT',
group='STRM',
format='ogg',
length=103.363229166666),

0x4: MusicData(
id=0x4,
name='STRM_F_WINTER.ogg',
type='BGM',
game='RFF',
group='STRM',
format='ogg',
length=119.224895833333),

0x4E: MusicData(
id=0x4E,
name='SEQ_MYROOM_A.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=159.591333333333),

0x4F: MusicData(
id=0x4F,
name='SEQ_MYROOM_B.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=117.344104166666),

0x5: MusicData(
id=0x5,
name='STRM_F_SNOW.ogg',
type='BGM',
game='RFF',
group='STRM',
format='ogg',
length=146.94275),

0xB8: MusicData(
id=0xB8,
name='SEQ_TYPHOON.wav',
type='Enviroment',
game='RF4',
group='SEQ',
format='wav',
length=9.98979166666666),

0x50: MusicData(
id=0x50,
name='SEQ_TOWN_SPRING.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=261.297791666666),

0x51: MusicData(
id=0x51,
name='SEQ_TOWN_SUMMER.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=129.364895833333),

0x52: MusicData(
id=0x52,
name='SEQ_TOWN_FALL.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=66.9396041666666),

0x53: MusicData(
id=0x53,
name='SEQ_TOWN_WINTER.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=84.8815416666666),

0x54: MusicData(
id=0x54,
name='SEQ_TOWN_NIGHT.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=105.113166666666),

0x55: MusicData(
id=0x55,
name='SEQ_DRAGON.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=2.66127083333333),

0x187: MusicData(
id=0x187,
name='SMF_charge_s_Begin.ogg',
type='Unknown',
game='RF4',
group='SMF',
format='ogg',
length=0),

0x56: MusicData(
id=0x56,
name='SEQ_DRAGON_PIANO.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=0.19659423828125),

0x32: MusicData(
id=0x32,
name='STRM_AIRSHIP_WIND.ogg',
type='ENV',
game='RF4',
group='STRM',
format='ogg',
length=53.1887301587301),

0x57: MusicData(
id=0x57,
name='SEQ_DRAGON_COMEDY.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=3.53033333333333),

0x58: MusicData(
id=0x58,
name='SEQ_DRAGON_OP.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=1.35223388671875),

0x59: MusicData(
id=0x59,
name='SEQ_EVENT_BATTLE.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=2.26747738939134),

0x5A: MusicData(
id=0x5A,
name='SEQ_BOSS_4.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=1.16081632653061),

0x5B: MusicData(
id=0x5B,
name='SEQ_LASTBOSS_4_1.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=0.660589569160997),

0x5C: MusicData(
id=0x5C,
name='SEQ_LASTBOSS_4_2.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=0.899727891156462),

0x5D: MusicData(
id=0x5D,
name='SEQ_EMPIRE.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=2.16684807256235),

0x5E: MusicData(
id=0x5E,
name='SEQ_ROOM.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=3.11065759637188),

0x5F: MusicData(
id=0x5F,
name='SEQ_PROTAGONIST.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=0.300045351473922),

0x6: MusicData(
id=0x6,
name='STRM_F_MYROOMA.ogg',
type='BGM',
game='RFF',
group='STRM',
format='ogg',
length=0.630929705215419),

0x60: MusicData(
id=0x60,
name='SEQ_PROTAGONIST_SKIP.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=2.78399092970521),

0x61: MusicData(
id=0x61,
name='SEQ_SAD_B.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=1.78081632653061),

0x62: MusicData(
id=0x62,
name='SEQ_FUN_A.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=1.36845804988662),

0x63: MusicData(
id=0x63,
name='SEQ_FUN_B.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=1.90086167800453),

0x64: MusicData(
id=0x64,
name='SEQ_COMICAL_A.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=2.97580498866213),

0x65: MusicData(
id=0x65,
name='SEQ_COMICAL_B.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=1.84435374149659),

0x66: MusicData(
id=0x66,
name='SEQ_EXCITING.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=3.80514739229024),

0x67: MusicData(
id=0x67,
name='SEQ_GENTLE_A.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=3.30115646258503),

0x68: MusicData(
id=0x68,
name='SEQ_GENTLE_B.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=1.459875),

0x69: MusicData(
id=0x69,
name='SEQ_PINCH_B.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=1.9715),

0x6A: MusicData(
id=0x6A,
name='SEQ_SUSPICIOUS.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=0.6106875),

0x6B: MusicData(
id=0x6B,
name='SEQ_FIELD.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=0.60225),

0x6C: MusicData(
id=0x6C,
name='SEQ_DGN_A.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=1.340625),

0x6D: MusicData(
id=0x6D,
name='SEQ_DGN_B.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=0.962478611586409),

0x6E: MusicData(
id=0x6E,
name='SEQ_DGN_C.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=1.48750305548765),

0x6F: MusicData(
id=0x6F,
name='SEQ_DGN_D.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=0.38163040821315),

0x7: MusicData(
id=0x7,
name='STRM_F_MYROOMB.ogg',
type='BGM',
game='RFF',
group='STRM',
format='ogg',
length=1.32492055732094),

0x70: MusicData(
id=0x70,
name='SEQ_DGN_F.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=0.877197265625),

0x71: MusicData(
id=0x71,
name='SEQ_DGN_GENERAL.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=1.796142578125),

0x72: MusicData(
id=0x72,
name='SEQ_FESTIVAL.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=2.0435791015625),

0x73: MusicData(
id=0x73,
name='SEQ_FESTIVAL_SKIP.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=2.4537353515625),

0x74: MusicData(
id=0x74,
name='SEQ_DATE.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=0.805419921875),

0x75: MusicData(
id=0x75,
name='SEQ_ENDING.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=1.3564453125),

0x76: MusicData(
id=0x76,
name='SEQ_WEDDING.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=2.2357177734375),

0x77: MusicData(
id=0x77,
name='SEQ_SPRING_1.ogg',
type='BGM',
game='RF1',
group='SEQ',
format='ogg',
length=1.9998779296875),

0x78: MusicData(
id=0x78,
name='SEQ_SUMMER_1.ogg',
type='BGM',
game='RF1',
group='SEQ',
format='ogg',
length=2.23736572265625),

0x79: MusicData(
id=0x79,
name='SEQ_FALL_1.ogg',
type='BGM',
game='RF1',
group='SEQ',
format='ogg',
length=2.2119140625),

0x7A: MusicData(
id=0x7A,
name='SEQ_WINTER_1.ogg',
type='BGM',
game='RF1',
group='SEQ',
format='ogg',
length=0.5085625),

0x7B: MusicData(
id=0x7B,
name='SEQ_DGN_C_1.ogg',
type='BGM',
game='RF1',
group='SEQ',
format='ogg',
length=2.32344671201814),

0x7C: MusicData(
id=0x7C,
name='SEQ_DGN_E_1.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=1.1796875),

0x7D: MusicData(
id=0x7D,
name='SEQ_DGN_G_1.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=1.64730505988755),

0x7E: MusicData(
id=0x7E,
name='SEQ_BOSS_F.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=1.47807256235827),

0x7F: MusicData(
id=0x7F,
name='SEQ_BOSS_F2.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=0.772471655328798),

0x8: MusicData(
id=0x8,
name='STRM_F_TOWN.ogg',
type='BGM',
game='RFF',
group='STRM',
format='ogg',
length=1.12020874023437),

0x80: MusicData(
id=0x80,
name='SEQ_LASTBOSS1.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=1.37008666992187),

0x81: MusicData(
id=0x81,
name='SEQ_SPRING_2.ogg',
type='BGM',
game='RF2',
group='SEQ',
format='ogg',
length=1.3203125),

0x82: MusicData(
id=0x82,
name='SEQ_SUMMER_2.ogg',
type='BGM',
game='RF2',
group='SEQ',
format='ogg',
length=2.9614375),

0x83: MusicData(
id=0x83,
name='SEQ_FALL_2.ogg',
type='BGM',
game='RF2',
group='SEQ',
format='ogg',
length=2.9614375),

0x84: MusicData(
id=0x84,
name='SEQ_WINTER_2.ogg',
type='BGM',
game='RF2',
group='SEQ',
format='ogg',
length=4.8405),

0x85: MusicData(
id=0x85,
name='SEQ_LOVE2.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=1.5087890625),

0x86: MusicData(
id=0x86,
name='SEQ_DGN_D_2.ogg',
type='BGM',
game='RF2',
group='SEQ',
format='ogg',
length=0.23065185546875),

0x87: MusicData(
id=0x87,
name='SEQ_DGN_E_2.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=67.1915588378906),

0x88: MusicData(
id=0x88,
name='SEQ_BOSS1.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=148.770629882812),

0x89: MusicData(
id=0x89,
name='SEQ_BOSS2.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=100.914489746093),

0x8A: MusicData(
id=0x8A,
name='SEQ_BOSS3.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=147.126953125),

0x8B: MusicData(
id=0x8B,
name='SEQ_BOSS4.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=227.919128417968),

0x8C: MusicData(
id=0x8C,
name='SEQ_LASTBOSS2.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=100.177307128906),

0x8D: MusicData(
id=0x8D,
name='SEQ_TITLE_3.ogg',
type='BGM',
game='RF3',
group='SEQ',
format='ogg',
length=120.611419677734),

0x8E: MusicData(
id=0x8E,
name='SEQ_SPRING_3.ogg',
type='BGM',
game='RF3',
group='SEQ',
format='ogg',
length=123.798034667968),

0x8F: MusicData(
id=0x8F,
name='SEQ_SUMMER_3.ogg',
type='BGM',
game='RF3',
group='SEQ',
format='ogg',
length=131.87954711914),

0x9: MusicData(
id=0x9,
name='STRM_F_BAR.ogg',
type='BGM',
game='RFF',
group='STRM',
format='ogg',
length=156.812133789062),

0x90: MusicData(
id=0x90,
name='SEQ_FALL_3.ogg',
type='BGM',
game='RF3',
group='SEQ',
format='ogg',
length=174.371063232421),

0x91: MusicData(
id=0x91,
name='SEQ_WINTER_3.ogg',
type='BGM',
game='RF3',
group='SEQ',
format='ogg',
length=109.912933349609),

0x92: MusicData(
id=0x92,
name='SEQ_TOWN_3.ogg',
type='BGM',
game='RF3',
group='SEQ',
format='ogg',
length=120.500610351562),

0x93: MusicData(
id=0x93,
name='SEQ_BAR2.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=109.26626586914),

0x94: MusicData(
id=0x94,
name='SEQ_BAR_3.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=50.6617126464843),

0x95: MusicData(
id=0x95,
name='SEQ_MYHOME_3.ogg',
type='BGM',
game='RF3',
group='SEQ',
format='ogg',
length=145.403198242187),

0x96: MusicData(
id=0x96,
name='SEQ_HOME_3.ogg',
type='BGM',
game='RF3',
group='SEQ',
format='ogg',
length=103.605804443359),

0x97: MusicData(
id=0x97,
name='SEQ_HOME_2_3.ogg',
type='BGM',
game='RF3',
group='SEQ',
format='ogg',
length=117.688903808593),

0x98: MusicData(
id=0x98,
name='SEQ_MOKOMOKO.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=78.4141235351562),

0x99: MusicData(
id=0x99,
name='SEQ_IKUZO.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=113.295288085937),

0x9A: MusicData(
id=0x9A,
name='SEQ_COMMU_3.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=122.102416992187),

0x9B: MusicData(
id=0x9B,
name='SEQ_ALCHEMY_3.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=166.829498291015),

0x9C: MusicData(
id=0x9C,
name='SEQ_DGN_A_3.ogg',
type='BGM',
game='RF3',
group='SEQ',
format='ogg',
length=81.1889038085937),

0x9D: MusicData(
id=0x9D,
name='SEQ_DGN_B_3.ogg',
type='BGM',
game='RF3',
group='SEQ',
format='ogg',
length=87.8123474121093),

0x9E: MusicData(
id=0x9E,
name='SEQ_DGN_B_2_3.ogg',
type='BGM',
game='RF3',
group='SEQ',
format='ogg',
length=131.315521240234),

0x9F: MusicData(
id=0x9F,
name='SEQ_DGN_C_3.ogg',
type='BGM',
game='RF3',
group='SEQ',
format='ogg',
length=119.490234375),

0xA: MusicData(
id=0xA,
name='STRM_F_ROOM_CROSS.ogg',
type='BGM',
game='RFF',
group='STRM',
format='ogg',
length=122.875),

0xA0: MusicData(
id=0xA0,
name='SEQ_DGN_D_3.ogg',
type='BGM',
game='RF3',
group='SEQ',
format='ogg',
length=89.6247863769531),

0xA1: MusicData(
id=0xA1,
name='SEQ_DGN_E_3.ogg',
type='BGM',
game='RF3',
group='SEQ',
format='ogg',
length=0.99475),

0xA2: MusicData(
id=0xA2,
name='SEQ_DGN_F_3.ogg',
type='BGM',
game='RF3',
group='SEQ',
format='ogg',
length=1.1069375),

0xA3: MusicData(
id=0xA3,
name='SEQ_DAIZA_3.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=0.517625),

0xA4: MusicData(
id=0xA4,
name='SEQ_WEDDING_3.ogg',
type='BGM',
game='RF3',
group='SEQ',
format='ogg',
length=0.7376875),

0xA5: MusicData(
id=0xA5,
name='SEQ_HANABATAKE_3.ogg',
type='BGM',
game='RF3',
group='SEQ',
format='ogg',
length=2.46244805670985),

0xA6: MusicData(
id=0xA6,
name='SEQ_BOSS3_1.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=1.4318125),

0xA7: MusicData(
id=0xA7,
name='SEQ_BOSS3_2.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=0.697784423828125),

0xA8: MusicData(
id=0xA8,
name='SEQ_BOSS3_3.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=2.3156462585034),

0xA9: MusicData(
id=0xA9,
name='SEQ_BOSS3_4.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=0.847625732421875),

0xAA: MusicData(
id=0xAA,
name='SEQ_LASTBOSS.ogg',
type='BGM',
game='RF4',
group='SEQ',
format='ogg',
length=0.8446044921875),

0xB: MusicData(
id=0xB,
name='STRM_F_ROOM_ERIS.ogg',
type='BGM',
game='RFF',
group='STRM',
format='ogg',
length=0.71710205078125),

0xF7: MusicData(
id=0xF7,
name='STRM_GOAL.ogg',
type='Fanfair',
game='RF4',
group='STRM',
format='ogg',
length=3.30886840820312),

0xB2: MusicData(
id=0xB2,
name='SEQ_MARGARET.wav',
type='BGM',
game='RF4',
group='SEQ',
format='wav',
length=0.4976875),

0xB3: MusicData(
id=0xB3,
name='SEQ_SAVE.wav',
type='SFXL',
game='RF4',
group='SEQ',
format='wav',
length=0.4698125),

0xB7: MusicData(
id=0xB7,
name='SEQ_YOUSUIRO.wav',
type='SFXL',
game='RF4',
group='SEQ',
format='wav',
length=1.298231292517),

0xED: MusicData(
id=0xED,
name='STRM_HANDMADE.ogg',
type='Fanfair',
game='RF4',
group='STRM',
format='ogg',
length=2.31434857003177),

0xBB: MusicData(
id=0xBB,
name='SE_BIRD.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=5.48028564453125),

0xBC: MusicData(
id=0xBC,
name='SE_SEMI.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.5000625),

0xBD: MusicData(
id=0xBD,
name='SE_HIGURASHI.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.45),

0xBE: MusicData(
id=0xBE,
name='SE_FROG.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.6154375),

0xBF: MusicData(
id=0xBF,
name='SE_SUZU.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.55),

0xC: MusicData(
id=0xC,
name='STRM_F_KUJIRA_1.ogg',
type='BGM',
game='RFF',
group='STRM',
format='ogg',
length=0.36109375),

0xC0: MusicData(
id=0xC0,
name='SE_HANABI_S.wav',
type='SFX',
game='RF4',
group='SE',
format='wav',
length=0.25678125),

0xC1: MusicData(
id=0xC1,
name='SE_HANABI_L.wav',
type='SFXL',
game='RF4',
group='SE',
format='wav',
length=1.1040625),

0xC2: MusicData(
id=0xC2,
name='SEQ_FUKUROU.wav',
type='SFX',
game='RF4',
group='SEQ',
format='wav',
length=0.871),

0xC3: MusicData(
id=0xC3,
name='STRM_FISH_MISS.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.6278125),

0xC4: MusicData(
id=0xC4,
name='STRM_FISH_SPLASH.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.561),

0xC5: MusicData(
id=0xC5,
name='STRM_FISH_BEND.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.5155),

0xC6: MusicData(
id=0xC6,
name='STRM_BRUSH.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.48053125),

0xC7: MusicData(
id=0xC7,
name='STRM_SCISSOR.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.4676875),

0xC8: MusicData(
id=0xC8,
name='STRM_MILK.ogg',
type='SFXL',
game='RF4',
group='STRM',
format='ogg',
length=0.382879818594104),

0xC9: MusicData(
id=0xC9,
name='STRM_SEED.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.406625),

0xCA: MusicData(
id=0xCA,
name='STRM_FUMBLE.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=2.23462585034013),

0xCB: MusicData(
id=0xCB,
name='STRM_DRAGON_HOWL.ogg',
type='SFXL',
game='RF4',
group='STRM',
format='ogg',
length=3.50004535147392),

0xCC: MusicData(
id=0xCC,
name='STRM_DRAGON_BREATH.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=2.38526643852358),

0xCD: MusicData(
id=0xCD,
name='STRM_VINE.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.4385625),

0xCE: MusicData(
id=0xCE,
name='STRM_CAMERA.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=2.9656875),

0x33: MusicData(
id=0x33,
name='STRM_MOVIE_OP_1.ogg',
type='Unknown',
game='RF4',
group='STRM',
format='ogg',
length=0.001007080078125),

0x34: MusicData(
id=0x34,
name='STRM_MOVIE_OP_1.ogg',
type='Unknown',
game='RF4',
group='STRM',
format='ogg',
length=0.001007080078125),

0x35: MusicData(
id=0x35,
name='STRM_MOVIE_OP_1.ogg',
type='Unknown',
game='RF4',
group='STRM',
format='ogg',
length=0.001007080078125),

0x36: MusicData(
id=0x36,
name='STRM_MOVIE_OP_1.ogg',
type='Unknown',
game='RF4',
group='STRM',
format='ogg',
length=0.001007080078125),

0x37: MusicData(
id=0x37,
name='STRM_MOVIE_OP_1.ogg',
type='Unknown',
game='RF4',
group='STRM',
format='ogg',
length=0.001007080078125),

0x38: MusicData(
id=0x38,
name='STRM_MOVIE_OP_1.ogg',
type='Unknown',
game='RF4',
group='STRM',
format='ogg',
length=0.001007080078125),

0x39: MusicData(
id=0x39,
name='STRM_MOVIE_OP_1.ogg',
type='Unknown',
game='RF4',
group='STRM',
format='ogg',
length=0.001007080078125),

0x3A: MusicData(
id=0x3A,
name='STRM_MOVIE_OP_1.ogg',
type='Unknown',
game='RF4',
group='STRM',
format='ogg',
length=0.001007080078125),

0x3B: MusicData(
id=0x3B,
name='STRM_MOVIE_OP_1.ogg',
type='Unknown',
game='RF4',
group='STRM',
format='ogg',
length=0.001007080078125),

0x3C: MusicData(
id=0x3C,
name='STRM_MOVIE_OP_1.ogg',
type='Unknown',
game='RF4',
group='STRM',
format='ogg',
length=0.001007080078125),

0x3D: MusicData(
id=0x3D,
name='STRM_MOVIE_OP_1.ogg',
type='Unknown',
game='RF4',
group='STRM',
format='ogg',
length=0.001007080078125),

0x3E: MusicData(
id=0x3E,
name='STRM_MOVIE_OP_1.ogg',
type='Unknown',
game='RF4',
group='STRM',
format='ogg',
length=0.001007080078125),

0x3F: MusicData(
id=0x3F,
name='STRM_MOVIE_OP_1.ogg',
type='Unknown',
game='RF4',
group='STRM',
format='ogg',
length=0.001007080078125),

0x40: MusicData(
id=0x40,
name='STRM_MOVIE_OP_1.ogg',
type='Unknown',
game='RF4',
group='STRM',
format='ogg',
length=0.001007080078125),

0x41: MusicData(
id=0x41,
name='STRM_MOVIE_OP_1.ogg',
type='Unknown',
game='RF4',
group='STRM',
format='ogg',
length=0.001007080078125),

0x42: MusicData(
id=0x42,
name='STRM_MOVIE_OP_1.ogg',
type='Unknown',
game='RF4',
group='STRM',
format='ogg',
length=0.001007080078125),

0x43: MusicData(
id=0x43,
name='STRM_MOVIE_OP_1.ogg',
type='Unknown',
game='RF4',
group='STRM',
format='ogg',
length=0.001007080078125),

0x44: MusicData(
id=0x44,
name='STRM_MOVIE_OP_1.ogg',
type='Unknown',
game='RF4',
group='STRM',
format='ogg',
length=0.001007080078125),

0x45: MusicData(
id=0x45,
name='STRM_MOVIE_OP_1.ogg',
type='Unknown',
game='RF4',
group='STRM',
format='ogg',
length=0.001007080078125),

0x46: MusicData(
id=0x46,
name='STRM_MOVIE_OP_1.ogg',
type='Unknown',
game='RF4',
group='STRM',
format='ogg',
length=0.001007080078125),

0x47: MusicData(
id=0x47,
name='STRM_MOVIE_OP_1.ogg',
type='Unknown',
game='RF4',
group='STRM',
format='ogg',
length=0.001007080078125),

0x48: MusicData(
id=0x48,
name='STRM_MOVIE_OP_1.ogg',
type='Unknown',
game='RF4',
group='STRM',
format='ogg',
length=0.001007080078125),

0x49: MusicData(
id=0x49,
name='STRM_MOVIE_OP_1.ogg',
type='Unknown',
game='RF4',
group='STRM',
format='ogg',
length=0.001007080078125),

0x4A: MusicData(
id=0x4A,
name='STRM_MOVIE_OP_1.ogg',
type='Unknown',
game='RF4',
group='STRM',
format='ogg',
length=0.001007080078125),

0x4B: MusicData(
id=0x4B,
name='STRM_MOVIE_OP_1.ogg',
type='Unknown',
game='RF4',
group='STRM',
format='ogg',
length=0.001007080078125),

0x4C: MusicData(
id=0x4C,
name='STRM_MOVIE_OP_1.ogg',
type='Unknown',
game='RF4',
group='STRM',
format='ogg',
length=0.001007080078125),

0x4D: MusicData(
id=0x4D,
name='STRM_MOVIE_OP_1.ogg',
type='Unknown',
game='RF4',
group='STRM',
format='ogg',
length=0.001007080078125),

0xCF: MusicData(
id=0xCF,
name='STRM_RAGNA_DOWN.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=117.106140136718),

0xD: MusicData(
id=0xD,
name='STRM_F_KUJIRA_2.ogg',
type='BGM',
game='RFF',
group='STRM',
format='ogg',
length=103.400299072265),

0xD0: MusicData(
id=0xD0,
name='STRM_WATER_DRAW.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=65.8975219726562),

0xD1: MusicData(
id=0xD1,
name='STRM_BOSS_DEAD.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=56.7743530273437),

0xD2: MusicData(
id=0xD2,
name='STRM_BOSS_DOWN.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=138.872955322265),

0xD3: MusicData(
id=0xD3,
name='STRM_GOLEMFOOT_L.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=89.875),

0xD4: MusicData(
id=0xD4,
name='STRM_GOLEMFOOT_R.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=87.5722045898437),

0xD5: MusicData(
id=0xD5,
name='STRM_BOSSFOOT_L.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=68.7708740234375),

0xD6: MusicData(
id=0xD6,
name='STRM_BOSSFOOT_R.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=134.165374755859),

0xD7: MusicData(
id=0xD7,
name='STRM_SEIRENFOOT.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=184.968994140625),

0xD8: MusicData(
id=0xD8,
name='STRM_DEMON_HOWL.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=138.061859130859),

0xD9: MusicData(
id=0xD9,
name='STRM_CHIMERA_HOWL.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=82.4089965820312),

0xDA: MusicData(
id=0xDA,
name='STRM_GOLEM_HOWL.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=156.727447509765),

0xDB: MusicData(
id=0xDB,
name='STRM_SEIREN_HOWL.ogg',
type='SFXL',
game='RF4',
group='STRM',
format='ogg',
length=62.8644104003906),

0xDC: MusicData(
id=0xDC,
name='STRM_OGREEATER_HOWL.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=59.751220703125),

0xDD: MusicData(
id=0xDD,
name='STRM_TANK_HOWL.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=52.1489868164062),

0xDE: MusicData(
id=0xDE,
name='STRM_SEIREN_HOWL.ogg',
type='SFXL',
game='RF4',
group='STRM',
format='ogg',
length=92.3904724121093),

0xDF: MusicData(
id=0xDF,
name='STRM_DRAGON_BREATH.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=66.375),

0xE: MusicData(
id=0xE,
name='STRM_F_KUJIRA_3.ogg',
type='BGM',
game='RFF',
group='STRM',
format='ogg',
length=120.571258544921),

0xE0: MusicData(
id=0xE0,
name='STRM_WATER.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=127.556610107421),

0xE1: MusicData(
id=0xE1,
name='STRM_WATER_EMPTY.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=110.217041015625),

0xE2: MusicData(
id=0xE2,
name='STRM_KUWA.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=134.046112060546),

0xE3: MusicData(
id=0xE3,
name='STRM_HIT_ROCK.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0),

0xE4: MusicData(
id=0xE4,
name='STRM_HIT_WOOD.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0),

0xE5: MusicData(
id=0xE5,
name='STRM_SKILL_AUTOGUARD.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=2.78409924223906),

0xE6: MusicData(
id=0xE6,
name='STRM_BS03_STEP.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=3.64950501099975),

0xE7: MusicData(
id=0xE7,
name='STRM_BS03_ICE.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.6835625),

0xE8: MusicData(
id=0xE8,
name='STRM_BS05_BITE.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=4.53204345703125),

0xE9: MusicData(
id=0xE9,
name='STRM_BS07_LANDING.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.279913224150574),

0xEA: MusicData(
id=0xEA,
name='STRM_PHARMACY.ogg',
type='SFXL',
game='RF4',
group='STRM',
format='ogg',
length=1.3298125),

0xEB: MusicData(
id=0xEB,
name='STRM_SMITH.ogg',
type='SFXL',
game='RF4',
group='STRM',
format='ogg',
length=1.2655625),

0xEC: MusicData(
id=0xEC,
name='STRM_DECORATION.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=2.614375),

0xEE: MusicData(
id=0xEE,
name='STRM_KITCHENKNIFE.ogg',
type='SFXL',
game='RF4',
group='STRM',
format='ogg',
length=2.614375),

0xEF: MusicData(
id=0xEF,
name='STRM_FRYINGPAN.ogg',
type='SFXL',
game='RF4',
group='STRM',
format='ogg',
length=0.5865625),

0xF: MusicData(
id=0xF,
name='STRM_F_DGN_WAKAKUSA.ogg',
type='BGM',
game='RFF',
group='STRM',
format='ogg',
length=0.60467529296875),

0xF0: MusicData(
id=0xF0,
name='STRM_PAN.ogg',
type='SFXL',
game='RF4',
group='STRM',
format='ogg',
length=0.78759765625),

0xF1: MusicData(
id=0xF1,
name='STRM_OVEN.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.474822781715961),

0xF2: MusicData(
id=0xF2,
name='STRM_BLENDER.ogg',
type='SFXL',
game='RF4',
group='STRM',
format='ogg',
length=2.68879858225372),

0xF3: MusicData(
id=0xF3,
name='STRM_STEAMER.ogg',
type='SFXL',
game='RF4',
group='STRM',
format='ogg',
length=2.63282204839892),

0xF4: MusicData(
id=0xF4,
name='STRM_SCHOOL_CHECK.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=1.76373291015625),

0xF5: MusicData(
id=0xF5,
name='STRM_WARUI.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=2.84825),

0xF6: MusicData(
id=0xF6,
name='STRM_SUGOKUWARUI.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=5.61846923828125),

0xF8: MusicData(
id=0xF8,
name='STRM_EQUIP.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=4.124625),

0xF9: MusicData(
id=0xF9,
name='STRM_SHOP.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=1.51919555664062),

0xFA: MusicData(
id=0xFA,
name='STRM_SHIPMENT.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.871125),

0xFB: MusicData(
id=0xFB,
name='STRM_THUNDER.ogg',
type='SFXL',
game='RF4',
group='STRM',
format='ogg',
length=0.4589375),

0xFC: MusicData(
id=0xFC,
name='STRM_GAMESTART.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=1.052),

0xFD: MusicData(
id=0xFD,
name='STRM_GAMEOVER.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=0.532379150390625),

0xFE: MusicData(
id=0xFE,
name='STRM_DRUMROLL.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=2.07081632653061),

0xFF: MusicData(
id=0xFF,
name='STRM_CYMBAL.ogg',
type='SFX',
game='RF4',
group='STRM',
format='ogg',
length=1.94784545898437),

}

sfx_list = list(dict.fromkeys([data.name for id, data in music_data_table.items() if data.type == "SFX" or data.type == "SFXL"]))
bgm_list = list(dict.fromkeys([data.name for id, data in music_data_table.items() if data.type == "BGM"]))

music_ids = {
0x0:"STRM_F_OP.ogg",
0x1:"STRM_F_SPRING.ogg",
0x2:"STRM_F_SUMMER.ogg",
0x3:"STRM_F_FALL.ogg",
0x4:"STRM_F_WINTER.ogg",
0x5:"STRM_F_SNOW.ogg",
0x6:"STRM_F_MYROOMA.ogg",
0x7:"STRM_F_MYROOMB.ogg",
0x8:"STRM_F_TOWN.ogg",
0x9:"STRM_F_BAR.ogg",
0xA:"STRM_F_ROOM_CROSS.ogg",
0xB:"STRM_F_ROOM_ERIS.ogg",
0xC:"STRM_F_KUJIRA_1.ogg",
0xD:"STRM_F_KUJIRA_2.ogg",
0xE:"STRM_F_KUJIRA_3.ogg",
0xF:"STRM_F_DGN_WAKAKUSA.ogg",
0x10:"STRM_F_DGN_TURUKUSA.ogg",
0x11:"STRM_F_DGN_YUKIKUSA.ogg",
0x12:"STRM_F_PINCH.ogg",
0x13:"STRM_F_VS_BOSS_NIWATORI.ogg",
0x14:"STRM_F_VS_BOSS_SLIME.ogg",
0x15:"STRM_F_VS_BOSS_ERIS.ogg",
0x16:"STRM_F_VS_BOSS_WAGNER.ogg",
0x17:"STRM_F_VS_BOSS_KURAGE.ogg",
0x18:"STRM_F_VS_BOSS_SNAKE.ogg",
0x19:"STRM_F_LASTBOSS1.ogg",
0x1A:"STRM_F_LASTBOSS2.ogg",
0x1B:"STRM_F_ENDING.ogg",
0x1C:"STRM_O_OP.ogg",
0x1D:"STRM_O_TOWN_AM.ogg",
0x1E:"STRM_O_TOWN_PM.ogg",
0x1F:"STRM_O_TOWN_HOKORA.ogg",
0x20:"STRM_O_BAR.ogg",
0x21:"STRM_O_MYROOMA.ogg",
0x22:"STRM_O_MYROOMB.ogg",
0x23:"STRM_O_SPRING.ogg",
0x24:"STRM_O_SUMMER.ogg",
0x25:"STRM_O_FALL.ogg",
0x26:"STRM_O_WINTER.ogg",
0x27:"STRM_O_GOBLIN.ogg",
0x28:"STRM_O_DGN_JUNGLE.ogg",
0x29:"STRM_O_DGN_FIREISLAND.ogg",
0x2A:"STRM_O_DGN_EARTH.ogg",
0x2B:"STRM_O_DGN_FIRE.ogg",
0x2C:"STRM_O_DGN_WATER.ogg",
0x2D:"STRM_O_DGN_WIND.ogg",
0x2E:"STRM_O_BATTLE_GIANT.ogg",
0x2F:"STRM_O_BOSS1.ogg",
0x30:"STRM_O_BOSS2.ogg",
0x31:"STRM_O_LASTBOSS.ogg",
0x32:"STRM_AIRSHIP_WIND.ogg",
0x33:"STRM_MOVIE_OP_1.ogg",
0x34:"STRM_MOVIE_OP_1.ogg",
0x35:"STRM_MOVIE_OP_1.ogg",
0x36:"STRM_MOVIE_OP_1.ogg",
0x37:"STRM_MOVIE_OP_1.ogg",
0x38:"STRM_MOVIE_OP_1.ogg",
0x39:"STRM_MOVIE_OP_1.ogg",
0x3A:"STRM_MOVIE_OP_1.ogg",
0x3B:"STRM_MOVIE_OP_1.ogg",
0x3C:"STRM_MOVIE_OP_1.ogg",
0x3D:"STRM_MOVIE_OP_1.ogg",
0x3E:"STRM_MOVIE_OP_1.ogg",
0x3F:"STRM_MOVIE_OP_1.ogg",
0x40:"STRM_MOVIE_OP_1.ogg",
0x41:"STRM_MOVIE_OP_1.ogg",
0x42:"STRM_MOVIE_OP_1.ogg",
0x43:"STRM_MOVIE_OP_1.ogg",
0x44:"STRM_MOVIE_OP_1.ogg",
0x45:"STRM_MOVIE_OP_1.ogg",
0x46:"STRM_MOVIE_OP_1.ogg",
0x47:"STRM_MOVIE_OP_1.ogg",
0x48:"STRM_MOVIE_OP_1.ogg",
0x49:"STRM_MOVIE_OP_1.ogg",
0x4A:"STRM_MOVIE_OP_1.ogg",
0x4B:"STRM_MOVIE_OP_1.ogg",
0x4C:"STRM_MOVIE_OP_1.ogg",
0x4D:"STRM_MOVIE_OP_1.ogg",
0x4E:"SEQ_MYROOM_A.ogg",
0x4F:"SEQ_MYROOM_B.ogg",
0x50:"SEQ_TOWN_SPRING.ogg",
0x51:"SEQ_TOWN_SUMMER.ogg",
0x52:"SEQ_TOWN_FALL.ogg",
0x53:"SEQ_TOWN_WINTER.ogg",
0x54:"SEQ_TOWN_NIGHT.ogg",
0x55:"SEQ_DRAGON.ogg",
0x56:"SEQ_DRAGON_PIANO.ogg",
0x57:"SEQ_DRAGON_COMEDY.ogg",
0x58:"SEQ_DRAGON_OP.ogg",
0x59:"SEQ_EVENT_BATTLE.ogg",
0x5A:"SEQ_BOSS_4.ogg",
0x5B:"SEQ_LASTBOSS_4_1.ogg",
0x5C:"SEQ_LASTBOSS_4_2.ogg",
0x5D:"SEQ_EMPIRE.ogg",
0x5E:"SEQ_ROOM.ogg",
0x5F:"SEQ_PROTAGONIST.ogg",
0x60:"SEQ_PROTAGONIST_SKIP.ogg",
0x61:"SEQ_SAD_B.ogg",
0x62:"SEQ_FUN_A.ogg",
0x63:"SEQ_FUN_B.ogg",
0x64:"SEQ_COMICAL_A.ogg",
0x65:"SEQ_COMICAL_B.ogg",
0x66:"SEQ_EXCITING.ogg",
0x67:"SEQ_GENTLE_A.ogg",
0x68:"SEQ_GENTLE_B.ogg",
0x69:"SEQ_PINCH_B.ogg",
0x6A:"SEQ_SUSPICIOUS.ogg",
0x6B:"SEQ_FIELD.ogg",
0x6C:"SEQ_DGN_A.ogg",
0x6D:"SEQ_DGN_B.ogg",
0x6E:"SEQ_DGN_C.ogg",
0x6F:"SEQ_DGN_D.ogg",
0x70:"SEQ_DGN_F.ogg",
0x71:"SEQ_DGN_GENERAL.ogg",
0x72:"SEQ_FESTIVAL.ogg",
0x73:"SEQ_FESTIVAL_SKIP.ogg",
0x74:"SEQ_DATE.ogg",
0x75:"SEQ_ENDING.ogg",
0x76:"SEQ_WEDDING.ogg",
0x77:"SEQ_SPRING_1.ogg",
0x78:"SEQ_SUMMER_1.ogg",
0x79:"SEQ_FALL_1.ogg",
0x7A:"SEQ_WINTER_1.ogg",
0x7B:"SEQ_DGN_C_1.ogg",
0x7C:"SEQ_DGN_E_1.ogg",
0x7D:"SEQ_DGN_G_1.ogg",
0x7E:"SEQ_BOSS_F.ogg",
0x7F:"SEQ_BOSS_F2.ogg",
0x80:"SEQ_LASTBOSS1.ogg",
0x81:"SEQ_SPRING_2.ogg",
0x82:"SEQ_SUMMER_2.ogg",
0x83:"SEQ_FALL_2.ogg",
0x84:"SEQ_WINTER_2.ogg",
0x85:"SEQ_LOVE2.ogg",
0x86:"SEQ_DGN_D_2.ogg",
0x87:"SEQ_DGN_E_2.ogg",
0x88:"SEQ_BOSS1.ogg",
0x89:"SEQ_BOSS2.ogg",
0x8A:"SEQ_BOSS3.ogg",
0x8B:"SEQ_BOSS4.ogg",
0x8C:"SEQ_LASTBOSS2.ogg",
0x8D:"SEQ_TITLE_3.ogg",
0x8E:"SEQ_SPRING_3.ogg",
0x8F:"SEQ_SUMMER_3.ogg",
0x90:"SEQ_FALL_3.ogg",
0x91:"SEQ_WINTER_3.ogg",
0x92:"SEQ_TOWN_3.ogg",
0x93:"SEQ_BAR2.ogg",
0x94:"SEQ_BAR_3.ogg",
0x95:"SEQ_MYHOME_3.ogg",
0x96:"SEQ_HOME_3.ogg",
0x97:"SEQ_HOME_2_3.ogg",
0x98:"SEQ_MOKOMOKO.ogg",
0x99:"SEQ_IKUZO.ogg",
0x9A:"SEQ_COMMU_3.ogg",
0x9B:"SEQ_ALCHEMY_3.ogg",
0x9C:"SEQ_DGN_A_3.ogg",
0x9D:"SEQ_DGN_B_3.ogg",
0x9E:"SEQ_DGN_B_2_3.ogg",
0x9F:"SEQ_DGN_C_3.ogg",
0xA0:"SEQ_DGN_D_3.ogg",
0xA1:"SEQ_DGN_E_3.ogg",
0xA2:"SEQ_DGN_F_3.ogg",
0xA3:"SEQ_DAIZA_3.ogg",
0xA4:"SEQ_WEDDING_3.ogg",
0xA5:"SEQ_HANABATAKE_3.ogg",
0xA6:"SEQ_BOSS3_1.ogg",
0xA7:"SEQ_BOSS3_2.ogg",
0xA8:"SEQ_BOSS3_3.ogg",
0xA9:"SEQ_BOSS3_4.ogg",
0xAA:"SEQ_LASTBOSS.ogg",
0xAB:"ANOTHER_SCNARIO_SELECT.ogg",
0xAC:"JUSTM_BEST_END.ogg",
0xAD:"JUSTM_BEST_END_KOHAKU.ogg",
0xAE:"JUSTM_BEST_END_MARGARET.ogg",
0xAF:"JUSTM_SCNARIO_SELECT.ogg",
0xB0:"NX_COMMENT.ogg",
0xB1:"NX_STUFFROLL.ogg",
0xB2:"SEQ_MARGARET.wav",
0xB3:"SEQ_SAVE.wav",
0xB4:"SEQ_FOUNTAIN.wav",
0xB5:"SEQ_SHORE.wav",
0xB6:"SEQ_RIVER.wav",
0xB7:"SEQ_YOUSUIRO.wav",
0xB8:"SEQ_TYPHOON.wav",
0xB9:"SEQ_SNOW.wav",
0xBA:"SEQ_RAIN.wav",
0xBB:"SE_BIRD.wav",
0xBC:"SE_SEMI.wav",
0xBD:"SE_HIGURASHI.wav",
0xBE:"SE_FROG.wav",
0xBF:"SE_SUZU.wav",
0xC0:"SE_HANABI_S.wav",
0xC1:"SE_HANABI_L.wav",
0xC2:"SEQ_FUKUROU.wav",
0xC3:"STRM_FISH_MISS.ogg",
0xC4:"STRM_FISH_SPLASH.ogg",
0xC5:"STRM_FISH_BEND.ogg",
0xC6:"STRM_BRUSH.ogg",
0xC7:"STRM_SCISSOR.ogg",
0xC8:"STRM_MILK.ogg",
0xC9:"STRM_SEED.ogg",
0xCA:"STRM_FUMBLE.ogg",
0xCB:"STRM_DRAGON_HOWL.ogg",
0xCC:"STRM_DRAGON_BREATH.ogg",
0xCD:"STRM_VINE.ogg",
0xCE:"STRM_CAMERA.ogg",
0xCF:"STRM_RAGNA_DOWN.ogg",
0xD0:"STRM_WATER_DRAW.ogg",
0xD1:"STRM_BOSS_DEAD.ogg",
0xD2:"STRM_BOSS_DOWN.ogg",
0xD3:"STRM_GOLEMFOOT_L.ogg",
0xD4:"STRM_GOLEMFOOT_R.ogg",
0xD5:"STRM_BOSSFOOT_L.ogg",
0xD6:"STRM_BOSSFOOT_R.ogg",
0xD7:"STRM_SEIRENFOOT.ogg",
0xD8:"STRM_DEMON_HOWL.ogg",
0xD9:"STRM_CHIMERA_HOWL.ogg",
0xDA:"STRM_GOLEM_HOWL.ogg",
0xDB:"STRM_SEIREN_HOWL.ogg",
0xDC:"STRM_OGREEATER_HOWL.ogg",
0xDD:"STRM_TANK_HOWL.ogg",
0xDE:"STRM_SEIREN_HOWL.ogg",
0xDF:"STRM_DRAGON_BREATH.ogg",
0xE0:"STRM_WATER.ogg",
0xE1:"STRM_WATER_EMPTY.ogg",
0xE2:"STRM_KUWA.ogg",
0xE3:"STRM_HIT_ROCK.ogg",
0xE4:"STRM_HIT_WOOD.ogg",
0xE5:"STRM_SKILL_AUTOGUARD.ogg",
0xE6:"STRM_BS03_STEP.ogg",
0xE7:"STRM_BS03_ICE.ogg",
0xE8:"STRM_BS05_BITE.ogg",
0xE9:"STRM_BS07_LANDING.ogg",
0xEA:"STRM_PHARMACY.ogg",
0xEB:"STRM_SMITH.ogg",
0xEC:"STRM_DECORATION.ogg",
0xED:"STRM_HANDMADE.ogg",
0xEE:"STRM_KITCHENKNIFE.ogg",
0xEF:"STRM_FRYINGPAN.ogg",
0xF0:"STRM_PAN.ogg",
0xF1:"STRM_OVEN.ogg",
0xF2:"STRM_BLENDER.ogg",
0xF3:"STRM_STEAMER.ogg",
0xF4:"STRM_SCHOOL_CHECK.ogg",
0xF5:"STRM_WARUI.ogg",
0xF6:"STRM_SUGOKUWARUI.ogg",
0xF7:"STRM_GOAL.ogg",
0xF8:"STRM_EQUIP.ogg",
0xF9:"STRM_SHOP.ogg",
0xFA:"STRM_SHIPMENT.ogg",
0xFB:"STRM_THUNDER.ogg",
0xFC:"STRM_GAMESTART.ogg",
0xFD:"STRM_GAMEOVER.ogg",
0xFE:"STRM_DRUMROLL.ogg",
0xFF:"STRM_CYMBAL.ogg",
0x100:"STRM_DOOR_STONE.ogg",
0x101:"STRM_ACTIVESEED_2.ogg",
0x102:"STRM_BS30_SHOUT.ogg",
0x103:"STRM_BS30_SCREAM.ogg",
0x104:"STRM_BS31_SHOUT.ogg",
0x105:"STRM_BS31_SCREAM.ogg",
0x106:"STRM_BS32_SHOUT.ogg",
0x107:"STRM_BS32_SCREAM.ogg",
0x108:"STRM_BS33_SHOUT.ogg",
0x109:"STRM_BS33_SCREAM.ogg",
0x10A:"STRM_BS34_SHOUT.ogg",
0x10B:"STRM_BS34_SCREAM.ogg",
0x10C:"STRM_BATH_1.ogg",
0x10D:"STRM_BATH_2.ogg",
0x10E:"STRM_FISH_HIT.ogg",
0x10F:"STRM_HIT_ZANGEKI.ogg",
0x110:"STRM_HIT_YARI.ogg",
0x111:"STRM_HIT_HAMMER.ogg",
0x112:"STRM_HIT_FIRE.ogg",
0x113:"STRM_HIT_WATER.ogg",
0x114:"STRM_KANSEI_A.ogg",
0x115:"STRM_KANSEI_B.ogg",
0x116:"STRM_WIND_PYU.ogg",
0x117:"STRM_GAAAN.ogg",
0x118:"STRM_DENGEKI.ogg",
0x119:"STRM_BM40_2_SANAGI_SHOUT.ogg",
0x11A:"STRM_BM40_2_SHOUT.ogg",
0x11B:"STRM_BM40_2_SCREAM.ogg",
0x11C:"STRM_BM41_1_SHOUT.ogg",
0x11D:"STRM_BM41_1_SCREAM.ogg",
0x11E:"STRM_BM42_1_SCREAM1.ogg",
0x11F:"STRM_BM42_1_SCREAM2.ogg",
0x120:"STRM_BM43_1_SHOUT.ogg",
0x121:"STRM_BM43_1_SCREAM.ogg",
0x122:"STRM_BM43_2_SHOUT.ogg",
0x123:"STRM_BM43_2_SCREAM.ogg",
0x124:"STRM_BM44_1_SHOUT.ogg",
0x125:"STRM_BM44_1_SCREAM.ogg",
0x126:"STRM_BM44_2_SHOUT.ogg",
0x127:"STRM_BM44_2_SCREAM.ogg",
0x128:"STRM_HIT_LASTBOOS.ogg",
0x129:"STRM_HIT_KUSA.ogg",
0x12A:"STRM_HIT_WATER2.ogg",
0x12B:"STRM_HIT_EARTH.ogg",
0x12C:"STRM_HIT_WIND.ogg",
0x12D:"STRM_HIT_DARK.ogg",
0x12E:"STRM_HIT_LOVE.ogg",
0x12F:"STRM_HIT_CRITICAL.ogg",
0x130:"STRM_DOOR_AKANAI.ogg",
0x131:"STRM_DOOR_LOCK.ogg",
0x132:"STRM_FUUSHA.ogg",
0x133:"STRM_GAANPIANO.ogg",
0x134:"STRM_WINDOW_CLASH.ogg",
0x135:"STRM_WIND_PYU_2.ogg",
0x136:"STRM_HIKOUSEN_TAKEOFF.ogg",
0x137:"STRM_ROONEY_EFFECT.ogg",
0x138:"SE_HAMMER_HIT.ogg",
0x139:"SE_DOOROPEN_2.ogg",
0x13A:"SE_WORDS_SEND.ogg",
0x13B:"SE_WORDS_M.wav",
0x13C:"SE_WORDS_F.ogg",
0x13D:"SE_WORDS_O.wav",
0x13E:"SE_SWING00.wav",
0x13F:"SE_SWING01.ogg",
0x140:"SE_SWING01.ogg",
0x141:"SE_SWING03.wav",
0x142:"SE_SWING03.wav",
0x143:"SE_SWING00.wav",
0x144:"SE_WALK_L.ogg",
0x145:"SE_WALK_R.ogg",
0x146:"SE_RUN_L.wav",
0x147:"SE_RUN_R.wav",
0x148:"SE_WALK_01_L.wav",
0x149:"SE_WALK_01_L.wav",
0x14A:"SE_WALK_01_L.wav",
0x14B:"SE_WALK_01_L.wav",
0x14C:"SE_WALK_02_L.wav",
0x14D:"SE_WALK_02_L.wav",
0x14E:"SE_WALK_02_L.wav",
0x14F:"SE_WALK_02_L.wav",
0x150:"SE_WALK_03_L.wav",
0x151:"SE_WALK_03_L.wav",
0x152:"SE_WALK_03_L.wav",
0x153:"SE_WALK_03_L.wav",
0x154:"SE_WALK_04_L.wav",
0x155:"SE_WALK_04_L.wav",
0x156:"SE_WALK_04_L.wav",
0x157:"SE_WALK_04_L.wav",
0x158:"SE_WALK_05_L.wav",
0x159:"SE_WALK_05_L.wav",
0x15A:"SE_WALK_05_L.wav",
0x15B:"SE_WALK_05_L.wav",
0x15C:"SE_HORSE_L.wav",
0x15D:"SE_HORSE_L.wav",
0x15E:"SE_SWING01.ogg",
0x15F:"SE_SWING00.wav",
0x160:"SE_HIT.ogg",
0x161:"SE_DOORCLOSE.ogg",
0x162:"SE_BS01_GUARD.ogg",
0x163:"SE_HUSUMA_OPEN.ogg",
0x164:"SE_HUSUMA_CLOSE.ogg",
0x165:"SE_SKILL_AUTOGUARD.ogg",
0x166:"SE_RUN_R.wav",
0x167:"SE_NPC_HIT.ogg",
0x168:"SE_HAMMER_HIT.ogg",
0x169:"SE_ACTIVESEED_1.wav",
0x16A:"SE_PIYO_STEP.ogg",
0x16B:"SE_BOKE2.ogg",
0x16C:"SE_SHOP_END.wav",
0x16D:"SE_KISHIMI_DOOROPEN.wav",
0x16E:"SE_WALK_KISHIMI_L.wav",
0x16F:"SE_WALK_KISHIMI_R.wav",
0x170:"SE_WALK_KISHIMI_L.wav",
0x171:"SE_WALK_KISHIMI_R.wav",
0x172:"SE_WALK_WOOD_L.wav",
0x173:"SE_WALK_WOOD_R.wav",
0x174:"SE_WALK_WOOD_L.wav",
0x175:"SE_WALK_WOOD_R.wav",
0x176:"SE_WORDS_D.wav",
0x177:"SE_WALK_FLOWER_L1.wav",
0x178:"SE_WALK_FLOWER_R1.wav",
0x179:"SE_WALK_FLOWER_L2.wav",
0x17A:"SE_WALK_FLOWER_R2.wav",
0x17B:"SE_WALK_FLOWER_L3.wav",
0x17C:"SE_WALK_FLOWER_R3.wav",
0x17D:"SE_CURSOR.wav",
0x17E:"SE_DECISION.wav",
0x17F:"SE_CANCEL.wav",
0x180:"SE_BAN.wav",
0x181:"SE_CAMPOPEN.wav",
0x182:"SE_CAMPCLOSE.wav",
0x183:"SE_CAMPTAB.wav",
0x184:"SE_CHATOPEN.wav",
0x185:"SE_CHATCLOSE.wav",
0x186:"SE_RINGOPEN.wav",
0x187:"SMF_charge_s_Begin.ogg",
0x188:"SE_CHARGE_L.wav",
0x189:"SE_HOLD.wav",
0x18A:"SE_SET.wav",
0x18B:"SE_PUT.wav",
0x18C:"SE_TAKE.wav",
0x18D:"SE_EAT.wav",
0x18E:"SE_JUMP.wav",
0x18F:"SE_CRITICAL.wav",
0x190:"SE_PIYORI.wav",
0x191:"SE_DAMAGE.wav",
0x192:"SE_ENEMY_DEAD.wav",
0x193:"SE_CHGATK_SWORD.wav",
0x194:"SE_MAGIC_FBALL.wav",
0x195:"SE_MAGIC_FBALL_HIT.wav",
0x196:"SE_MAGIC_EXPLOSION.wav",
0x197:"SE_MAGIC_CRIMSON.wav",
0x198:"SE_MAGIC_INFERNO.wav",
0x199:"SE_MAGIC_WLASER.wav",
0x19A:"SE_MAGIC_ABSORB.wav",
0x19B:"SE_MAGIC_ABSORB_HIT.wav",
0x19C:"SE_MAGIC_CURE.wav",
0x19D:"SE_MAGIC_STONE.wav",
0x19E:"SE_MAGIC_QUAKE.wav",
0x19F:"SE_MAGIC_METEA.wav",
0x1A0:"SE_MAGIC_LMESSER.wav",
0x1A1:"SE_MAGIC_LMESSER_HIT.wav",
0x1A2:"SE_MAGIC_MEDICATION.wav",
0x1A3:"SE_MAGIC_STURM.wav",
0x1A4:"SE_CHGATK_SWORD.wav",
0x1A5:"SE_CHGATK_SWORD.wav",
0x1A6:"SE_CHGATK_SWORD.wav",
0x1A7:"SE_CHGATK_SWORD.wav",
0x1A8:"SE_CHGATK_SWORD.wav",
0x1A9:"SE_CHGATK_SWORD.wav",
0x1AA:"SE_LEVELUP.wav",
0x1AB:"SE_SKILLUP.wav",
0x1AC:"SE_SYN_SUCCESS.wav",
0x1AD:"SE_SYN_MISS.wav",
0x1AE:"SE_RAGNA_SPIN.wav",
0x1AF:"SE_RADAR.wav",
0x1B0:"SE_YAWN.wav",
0x1B1:"SE_INN.wav",
0x1B2:"SE_BOSS_VANISH.wav",
0x1B3:"SE_MAGIC_QUAKE.wav",
0x1B4:"SE_FLOWER.wav",
0x1B5:"SE_SUMMON.wav",
0x1B6:"SE_SPAWN.wav",
0x1B7:"SE_DRAGON_FLAP.wav",
0x1B8:"SE_ATTACK_01.wav",
0x1B9:"SE_ATTACK_02.wav",
0x1BA:"SE_ATTACK_03.wav",
0x1BB:"SE_ATTACK_04.wav",
0x1BC:"SE_MAGIC_SHINE.wav",
0x1BD:"SE_MAGIC_ESCAPE.wav",
0x1BE:"SE_MAGIC_ESCAPE_ARRV.wav",
0x1BF:"SE_SKILL_POWERWAVE.wav",
0x1C0:"SE_SKILL_SLASH.wav",
0x1C1:"SE_SKILL_RUSHATTACK.wav",
0x1C2:"SE_SKILL_SPIN.wav",
0x1C3:"SE_SKILL_RUSH.wav",
0x1C4:"SE_SKILL_STAB.wav",
0x1C5:"SE_SKILL_SPLASH.wav",
0x1C6:"SE_SKILL_SPINTOP.wav",
0x1C7:"SE_SKILL_DHARMA.wav",
0x1C8:"SE_PLAY_RUSH.wav",
0x1C9:"SE_PLAY_COMMAND.wav",
0x1CA:"SE_PLAY_SEARCH.wav",
0x1CB:"SE_PLAY_SEARCH_SUCCESS.wav",
0x1CC:"SE_PLAY_SEARCH_MISSTAKE.wav",
0x1CD:"SE_SUGOROKU_DICE_ROLL_00.wav",
0x1CE:"SE_SUGOROKU_DICE_ROLL_01.wav",
0x1CF:"SE_CRASH.wav",
0x1D0:"SE_SPAWN_SIGN.wav",
0x1D1:"SE_ATTACK_BREATH.wav",
0x1D2:"SE_MAGIC_ROCKICE.wav",
0x1D3:"SE_MAGIC_BOMB.wav",
0x1D4:"SE_MAGIC_MISSILE.wav",
0x1D5:"SE_SMOKY.wav",
0x1D6:"SE_BS00_RINGO_POP.wav",
0x1D7:"SE_BS00_RINGO_ROUND.wav",
0x1D8:"SE_BS00_RINGO_ATK.wav",
0x1D9:"SE_BS00_PUNCH.wav",
0x1DA:"SE_BS00_CATCH.wav",
0x1DB:"SE_BS00_ATK.wav",
0x1DC:"SE_BS00_TACKLE.wav",
0x1DD:"SE_BS01_THRUST.wav",
0x1DE:"SE_BS01_WALK.wav",
0x1DF:"SE_BS01_AMMO_UNI.wav",
0x1E0:"SE_BS01_AMMO_TARU.wav",
0x1E1:"SE_BS01_BREATH.wav",
0x1E2:"SE_BS02_TACKLE.wav",
0x1E3:"SE_BS02_BREATH.wav",
0x1E4:"SE_BS02_PULL.wav",
0x1E5:"SE_BS02_INVISI.wav",
0x1E6:"SE_BS03_RUSH.wav",
0x1E7:"SE_BS03_BREATHE.wav",
0x1E8:"SE_BS04_PUNCH.wav",
0x1E9:"SE_BS04_RUSH.wav",
0x1EA:"SE_BS05_SCRATCH.wav",
0x1EB:"SE_BS05_BREATH.wav",
0x1EC:"SE_BS06_ROUND.wav",
0x1ED:"SE_BS06_SEARCH.wav",
0x1EE:"SE_BS07_TAIL.wav",
0x1EF:"SE_BS07_WING.wav",
0x1F0:"SE_BS07_MOVE.wav",
0x1F1:"SE_BS07_PARSER.wav",
0x1F2:"SE_BS09_STAIL.wav",
0x1F3:"SE_BS09_FIRE.wav",
0x1F4:"SE_BS09_SPECIAL.wav",
0x1F5:"SE_BOSS_HYPER.wav",
0x1F6:"SE_IREKAWARI.wav",
0x1F7:"SE_YOI.wav",
0x1F8:"SE_SUGOKUYOI.wav",
0x1F9:"SE_START.wav",
0x1FA:"SE_SYUURYOU.wav",
0x1FB:"SE_THROW.wav",
0x1FC:"SE_RAKKA.wav",
0x1FD:"SE_DASH.wav",
0x1FE:"SE_TRANSFORM.wav",
0x1FF:"SE_TRANSFORM_1.wav",
0x200:"SE_TRANSFORM_2.wav",
0x201:"SE_MOCO_ROLLING.wav",
0x202:"SE_MIAGE_START.wav",
0x203:"SE_MIAGE_START.wav",
0x204:"SE_HASU.wav",
0x205:"SE_BIKKURI.wav",
0x206:"SE_ONPU.wav",
0x207:"SE_ISSEN.wav",
0x208:"SE_STAB.wav",
0x209:"SE_SUPERSAIYAJIN.wav",
0x20A:"SE_FUKUROU.wav",
0x20B:"SE_SAVE.wav",
0x20C:"SE_MONGET_OK.wav",
0x20D:"SE_MONGET_NG.wav",
0x20E:"SE_WHEEL.wav",
0x20F:"SE_TANUKI_DOWN.wav",
0x210:"SE_BS32_HOWL.wav",
0x211:"SE_BS34_WAVE.wav",
0x212:"SE_BS34_BIGBEAM.wav",
0x213:"SE_FROG_SEED.wav",
0x214:"SE_GAAAN.wav",
0x215:"SE_BOKE.wav",
0x216:"SE_TSUKKOMI.wav",
0x217:"SE_TOHOHO.wav",
0x218:"SE_LEVELUP_OUJI.wav",
0x219:"SE_ONPU_2.wav",
0x21A:"SE_CLOCK.wav",
0x21B:"SE_FIRESTORM.wav",
0x21C:"SE_DAMAGE_2.wav",

}