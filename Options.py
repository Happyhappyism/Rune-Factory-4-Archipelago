from dataclasses import dataclass
from Options import Choice, Range, OptionList, OptionGroup, Toggle, DefaultOnToggle, Removed, PerGameCommonOptions, OptionSet, StartInventoryPool, DeathLink, FreeText

class Goal(Choice):
    """Game's Goal
    Ethelberd: Defeat Ethelberd at the end of Floating Empire.
    Rune Prana: Defeat Ragnarok at the end of Rune Prana.
    Shipment Percentage: Ship an amount of the shipment catalogue as set below in shipment_percentage_requirement.
    Nationalized Baths: Issue the Nationalize Bath order.
    Eliza: Finish all of Eliza's requests. (Not implemented) Fair warning this one may not be sync viable time wise.
    Marriage: Get married, have a child, proceed to Sechs Territory and collect and ship a White Stone.
    Runehunt: Collect a configurable number of Rune Spheres out of a total pool.
    Homeowner: Buy the house for 198m G located just above Autumn Field.
    Custom: Set any check in the game to be your goal, can be configured in custom_goal_location below."""
    option_custom = 0
    option_ethelberd = 1
    option_runeprana = 2
    option_shipment_percentage = 3
    option_nationized_baths = 4
    #option_eliza = 5
    option_mariage = 6
    option_runehunt = 7
    option_homeowner = 8
    default = 1
    display_name = "Goal"

class EmpireSpheres(Range):
    """These are used to unlock the Floating Empire and Rune Prana locations, with values set below"""
    range_start = 1
    range_end = 50
    default = 4

class PrenaSpheres(Range):
    """Determines the number of rune spheres needed to get into Rune Prana"""
    range_start = 1
    range_end = 80
    default = 4

class MaxSpheres(Range):
    """Determines the total number of rune spheres added into the item pool
    These are used to unlock the Floating Empire and Rune Prana locations, with values set below"""
    range_start = 1
    range_end = 100
    default = 6

class SphereHuntSpheres(Range):
    """For Sphere hunt goal only, determines the number of runes spheres required to clear the game"""
    range_start = 1
    range_end = 100
    default = 6

class Gender(Choice):
    option_lest = 0
    option_frey = 1
    default = 0

class BirthMonth(Removed):
    option_spring = 0
    option_summer = 1
    option_autumn = 2
    option_winter = 3
    default = 0

class Birthday(Removed):
    range_start = 1
    range_end = 30
    default = 10

class SaveSlot(Range):
    """Determines what save slot the archipelago save will replace, 
    make sure a save file already exists in that slot or it will not load when you boot the game.
    any existing save in that slot will be backed up by the Rune Factory 4 client.
    Be sure to place the .sav file provided by whoever generated the seed 
    to the 'Archipelago' folder in the Rune Factory 4 Special install directory"""
    range_start = 1
    range_end = 20
    default = 1

class MutliRequest(DefaultOnToggle):
    """When enabled will allow you to take as many requests as you want per day"""
    display_name = "Accept Multiple Requests"

class MaxItemTier(Range):
    """Determines the max tier of an item to be included as a shipment
    Item tiers can be viewed on the spreadsheet found at https://shorturl.at/lfVCo"""
    range_start = 5
    range_end = 11
    default = 9

class RoyaltyRank(Range):
    """Determines starting prince(ss) rank offering more orders from the start, """
    range_start = 0
    range_end = 5
    default = 3

class DropRate(Range):
    """Increases the base drop rate for monster drops"""
    range_start = 0
    range_end = 100
    # option_vanilla = 0
    # option_moderate = 10
    # option_decent = 20
    # option_extreme = 50
    default = 20

class MaxSell(Range):
    """Determines the max sell value of an item to be included as a shipment location"""
    range_start = 10000
    range_end = 800000
    default = 500000

class ExpMultiplier(Choice):
    """Increases experience gained from combat"""
    option_vanilla = 0
    option_double = 1
    option_quadruple = 2
    option_octuple = 3
    default = 2

class SkillExpMultiplier(Choice):
    """Increases experience gained from skills and crafting"""
    option_vanilla = 0
    option_double = 1
    option_quadruple = 2
    option_octuple = 3
    default = 2

class FPMultiplier(Choice):
    """Increases Friendship Point gains from talking and giving gifts"""
    option_vanilla = 0
    option_double = 1
    option_quadruple = 2
    option_octuple = 3
    default = 1

class RequireBaths(Removed):
    """Enabling this will require you to have the nationize bath order to open your goal region"""

class ShipmentPercentage(Range):
    """Required shipment percentage needed to goal, this will be rounded down to the nearest 5 percent.
    For Shipment Percentage Goal only."""
    range_start = 0
    range_end = 100
    default = 30

class BGM(Choice):
    """Begin the game with this BGM order passed, changing the game's soundtrack."""
    option_RF1 = 4
    option_RF2 = 2
    option_RF3 = 6
    option_RF4 = 0
    option_RFFrontier = 1
    option_RFToD = 5
    default = 0

class MaxFriend(Range):
    """When friendsanity is enabled as locations will determine the max friendship level to include as locations"""
    range_start = 1
    range_end = 10
    default = 6

class ShopStart(DefaultOnToggle):
    """Start the run with Blossoms Vegetables, Magic Shop, Jewelry Shop and Fish Shop"""
class AxeStart(Toggle):
    """Start the run with Volkanon's Axe opening Selphia Field from the start"""
class RecipeStart(DefaultOnToggle):
    """Start with all recipes already unlocked"""
class FreeDoctor(DefaultOnToggle):
    """Removes Jone's doctor fee"""

class CropSanity(DefaultOnToggle):
    """Include normal Crop shipments as locations"""

class Fishsanity(Toggle):
    """Include Fish shipments as locations"""

class GoldcropSanity(Toggle):
    """Include Gold Crop shipments as locations"""

class Largecropsanity(Toggle):
    """Include Large Crop shipments as locations"""

class DropSanity(DefaultOnToggle):
    """Include Monster Drop shipments as locations"""

class CraftSanity(Toggle):
    """Include Crafting (Armor, accessories, ect) shipments as locations"""

class ForgeSanity(Toggle):
    """Include Forge shipments as locations"""

class DishSanity(Toggle):
    """Include Cooking dish shipments as locations"""

class SpellSanity(Toggle):
    """Include Spell and Rune Ability shipments as locations"""

class ForageSanity(DefaultOnToggle):
    """Include grasses, mushrooms, seeds and other natural shipments as locations"""

class ChemicSanity(DefaultOnToggle):
    """Include Potions, Vitamins and chemicals as shipment locations """

class MineralSanity(DefaultOnToggle):
    """Include minerals and jewels shipments as locations"""

class GrocerySanity (DefaultOnToggle):
    """Include Groceries, Breads, Fruits, Eggs, and Milk as shipments as locations"""

class RequestSanity(Toggle):
    """Include requests as locations (Currently not implemented, do not toggle on)"""

class MusicShuffle(Toggle):
    """Shuffle background music tracks"""

class SfxShuffle(Toggle):
    """Shuffle sound effects"""

class Friendsanity(Choice):
    """Include Friendship levels as locations or items that sets everyone's friendship levels"""
    option_off = 0
    option_locations = 1
    option_items = 2
    default = 0

class OpenAirship(Toggle):
    """Setting this to true will make airship locations appear on the destination list any time you get that area's key, 
    even if you can't logically reach that area. 
    E.G. Winter's Grasp will unlock Sechs Empire, even if you don't have Maya Bridge."""

class Petsanity(Toggle):
    """Include monster tames as locations"""

class OutfitSanity(Toggle):
    """Include clothing store outfits as locations"""

class ShopboxLink(DefaultOnToggle):
    """Allows you to send items between other Rune Factory 4 players with server command /send playername"""

class IncludeTraps(Toggle):
    """Include traps"""

class TrupinHint(Toggle):
    """When enabled will replace some of Mistress Trupin's dialog with world hints, starting from the second time you find her.
    This can dramatically increase speed of play, given it can be difficult to get enough checks for hints with RF4's large check pool.
    Note that for now, this does *not* Autohint it through the tracker, and Trupin doesn't repeat herself until you've found all of her hints."""

class DailyTrupin(Toggle):
    """When enabled will automatically set the Trupin Comes Everyday order.
    This is particularly useful to speed up the game when you have Trupin Hints enabled."""

class ShowEneLevels(DefaultOnToggle):
    """When enabled will automatically set the Show Enemy Levels order"""

class ShowEneHP(DefaultOnToggle):
    """When enabled will automatically set the Show Enemy HP order"""

class GayDating(Toggle):
    """When enabled will allow males to date males and females to date female villagers"""

class ShuffleElements(Toggle):
    """When enabled will shuffle magical elements. This shuffles all player spells of the given element to another. i.e. all water becomes dark. All Dark becomes Earth, etc.
    To figure out what elements they've been shuffled into, look at the color of the shockwaves made when striking an enemy with the spell.
    The elements also change the spell's advance properties, for example a water spell that becomes dark will also make enemies flinch as if it were a dark spell."""

class SharanceStart(Removed):
    """Start with Sharance Maze unlocked, does not effect logic"""

class RandomMonsterModel(Toggle):
    """The features of this section are still very unstable. While testing is appreciated,
    The options in this section can lead to crashes and/or uncompletable seeds. Use at your own risk.

    Shuffles Enemy Models"""

class RanmdomMonsterAI(Toggle):
    """Shuffles Enemy AI"""

class RandomMonsterMoveset(Toggle):
     """Shuffles Monster movesets"""

# DEBUG
class MonsterShuffleParams(Removed):
    """Shuffle specific parameters
    example: ['0x12C', '0x110', '0x7C']"""
    valid_keys = [hex(val) for val in range(0,0x134, 4)]

class LocationLogicCheck(FreeText):
    """Custom Goal Only
    Enter a check below and reaching that check becomes your goal for the seed. 
    You can use randomization to have a random check become your goal. Eg. 
        'Turnip Heaven': 50
        'White Stone': 50
        'Rare Can': 50"""
    
class StartWeapon(Choice):
    option_short_sword = 0x149
    option_long_sword = 0x16A
    option_spear = 0x18C
    option_axe = 0x1C4
    option_hammer = 0x1AD
    option_dual_blades = 0x1FC
    option_gloves = 0x21B
    option_staff = 0x1D8
    option_random = "random"
    default = 0x149
    
class ProgressiveWeapon(Choice):
    """When enabled will include a set of progressive weapons"""
    option_off = 0
    option_starter_weapon = 1
    option_random_weapon = 2

class ProgressiveArmor(Toggle):
    """When enabled will include a set of progressive armors"""

class ProgressiveAccessory(Toggle):
    """When enabled will include a set of progressive accessories"""

class CharaApperance(Choice):
    """Changes your appearance, 
    Do not put on a costume when using one of the monster options, this will crash the game."""
    option_vanilla = 0x0
    option_vishnal = 0x01
    option_clorica = 0x02
    option_volkanon = 0x03
    option_forte = 0x04
    option_kiel = 0x05
    option_bado = 0x06
    option_margaret = 0x07
    option_dylas = 0x08
    option_arthur = 0x09
    option_porcoline = 0x0a
    option_xiao_pai = 0x0b
    option_lin_fa = 0x0c
    option_amber = 0x0d
    option_illuminata = 0x0e
    option_doug = 0x0f
    option_blossom = 0x10
    option_dolce = 0x11
    option_jones = 0x12
    option_nancy = 0x13
    option_leon = 0x14
    option_ventuswill = 0x15
    option_noel = 0x16
    option_luna = 0x17
    option_barrett = 0x18
    option_raven = 0x19
    option_pico = 0x135
    option_ethelberd = 0xEF
    option_trupin = 0x1A
    option_orc = 0x30
    option_goblin = 0x34
    option_minotaur = 0x38
    option_daemon = 0x3A
    option_little_mage = 0x3C
    option_troll = 0x3F
    option_beetle = 0x47
    option_panther = 0x4D
    option_silver_wolf = 0x4F
    option_buffamoo = 0x52
    option_weagle = 0x53
    option_chipsqueek = 0x55
    option_faust = 0x67
    option_fairy = 0x6A
    option_dark_fairy = 0x6B
    option_wooly = 0x6F
    option_dragon = 0x72
    option_pomme = 0x73
    option_duck = 0x7C
    option_penguin = 0x7D
    option_onion_ghost = 0x80
    option_tomato_ghost = 0x81
    option_pepper_ghost = 0x82
    option_turnip_ghost = 0x83
    option_palm_cat = 0xA0
    option_red = 0xA9
    option_green = 0xAA
    option_blue = 0xAB
    option_yellow = 0xAC
    option_chimera = 0xD2
    option_magnuto = 0xDC
    option_ambrosia = 0xE5
    option_thunderbolt = 0xE6
    option_marionetta = 0xE7
    option_random = "random"
    default = 0x0

rf4_options_group = [
    OptionGroup("Goal Options", [
        Goal,
        MaxSpheres,
        EmpireSpheres,
        PrenaSpheres,
        #RequireBaths,
        ShipmentPercentage,
        LocationLogicCheck,
        SphereHuntSpheres,
    ]),
    
    OptionGroup("Shipment Sanities", [
        CropSanity,
        Fishsanity,
        GoldcropSanity,
        Largecropsanity,
        DropSanity,
        ForgeSanity,
        CraftSanity,
        DishSanity,
        SpellSanity,
        MineralSanity,
        ForageSanity,
        ChemicSanity,
        GrocerySanity
    ]),
    OptionGroup("Other Sanities", [
        RequestSanity,
        Friendsanity,
        Petsanity,
        OutfitSanity,
    ]),
    OptionGroup("Location Limitations", [
        MaxItemTier,
        MaxSell,
        MaxFriend
    ]),
    OptionGroup("Save Options", [
        SaveSlot,
        Gender,
        BirthMonth,
        Birthday,
    ]),
    OptionGroup("Gameplay Options", [
        StartWeapon,
        RoyaltyRank,
        CharaApperance,
        BGM,
        MusicShuffle,
        SfxShuffle,
        OpenAirship,
        ProgressiveWeapon,
        ProgressiveArmor,
        ProgressiveAccessory,
        ShuffleElements,
        GayDating
    ]),
    OptionGroup("Server Group Options",[
        DeathLink,
        ShopboxLink,
        IncludeTraps,
        TrupinHint,
    ]),
    OptionGroup("Quality Of Life", [
        ExpMultiplier,
        SkillExpMultiplier,
        DropRate,
        FreeDoctor,
        ShowEneLevels,
        ShowEneHP,
        DailyTrupin,
    ]),
    OptionGroup("Starting Items", [
        ShopStart,
        AxeStart,
        RecipeStart
    ]),
    OptionGroup("Monster Randomizations",[
        RandomMonsterModel,
        RandomMonsterMoveset,
        RanmdomMonsterAI,
    ]),
    # OptionGroup("Debug", [
    #     MonsterShuffleParams
        
    # ])
]

@dataclass
class RF4Options(PerGameCommonOptions):
    game_goal: Goal
    max_runespheres: MaxSpheres

    player_character: Gender
    #birth_month: BirthMonth
    #birthday: Birthday

    fortress_runespheres: EmpireSpheres
    #runeprena_runespheres: PrenaSpheres
    runeprana_runespheres: PrenaSpheres
    #require_nationize_baths: RequireBaths
    shipment_percentage_requirement: ShipmentPercentage
    sphere_hunt_spheres: SphereHuntSpheres

    max_ship_tier: MaxItemTier
    max_sell_value: MaxSell

    cropsanity: CropSanity
    fishsanity: Fishsanity
    craftsanity: CraftSanity
    forgesanity: ForgeSanity
    dishsanity: DishSanity
    goldcropsanity: GoldcropSanity
    largecropsanity: Largecropsanity
    dropsanity: DropSanity
    spellsanity: SpellSanity
    mineralsanity: MineralSanity
    foragesanity: ForageSanity
    chemicsanity: ChemicSanity
    grocerysanity: GrocerySanity

    background_music: BGM
    shuffle_music: MusicShuffle
    shuffle_sound_effects: SfxShuffle

    requestsanity:RequestSanity
    friendsanity: Friendsanity
    tamesanity: Petsanity
    outfitsanity: OutfitSanity

    max_friendship: MaxFriend
    trupin_hint: TrupinHint
    daily_trupin: DailyTrupin
    show_enemy_level: ShowEneLevels
    show_enemy_HP: ShowEneHP
    out_of_logic_airship: OpenAirship

    save_slot: SaveSlot
    drop_rate_increase: DropRate
    death_link: DeathLink
    shopbox_link: ShopboxLink
    start_weapon: StartWeapon

    starting_royalty: RoyaltyRank
    recipe_start: RecipeStart
    no_jones_fee: FreeDoctor
    exp_multiplier: ExpMultiplier
    skill_exp_multiplier: SkillExpMultiplier
    friendship_multiplier: FPMultiplier

    gay_dating: GayDating

    include_traps: IncludeTraps
    progressive_weapon: ProgressiveWeapon
    progressive_armor: ProgressiveArmor
    progressive_accessory: ProgressiveAccessory

    character_appearance: CharaApperance

    shop_start:ShopStart
    axe_start:AxeStart
    #sharance_start: SharanceStart

    shuffle_elements: ShuffleElements
    shuffle_monster_models: RandomMonsterModel
    shuffle_monster_AI: RanmdomMonsterAI
    shuffle_monster_moveset: RandomMonsterMoveset
    shuffle_monster_params: MonsterShuffleParams

    custom_goal_location: LocationLogicCheck
    
