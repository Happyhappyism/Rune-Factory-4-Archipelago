from typing import Callable, Dict, NamedTuple, Optional, TYPE_CHECKING

from BaseClasses import Location

import logging

from .game_data import friendsanity_data, friend_items, outfit_data

#from .com_ap_methods import parse_csv
if TYPE_CHECKING:
    from . import RF4World

logger = logging.getLogger("Rune Factory 4 Locations")

class RF4Location(Location):
    game = "Rune Factory 4"

class RF4ShipData(NamedTuple):
    name: str = None
    id: int = None
    start_byte: int = 0
    start_bit: int = 0
    apid: int = None
    type: str = None
    region: str = "Selphia"
    loc_name: str = None
    #level: int = 0
    tier: int = 0
    shipable: bool = True
    buy_value: int = 0
    sell_value: int = 0
    required_items: list = None
    fill_weight: int = 0
    fill_amount: int = 1
    monster: str = None

class RF4ChestData(NamedTuple):
    items: list = None
    id: int = 0
    apid: int = 0
    region: str = None
    loc_name: str = None
    byte: int = 0
    mask: int = 0
    name: str = None
    room: str = None
    tier: int = 0
    recipe: list = None
    notes: str = None

class RF4RecipeData(NamedTuple):
    id: int = 0
    #apid: int = 0
    #region: str = None
    loc_name: str = None
    byte: int = 0
    mask: int = 0
    craft_type: str = None
    subtype: str = None
    level: int = 0
    name: str = None
    tier: int = None
    ingredients: list = None

class RF4RequestData(NamedTuple):
    #region_con: str = None
    apid: int = 0
    name: str = None
    loc_name: str = None
    byte: int = 0
    mask: int = 0
    request_req: str = None
    item_req: list = None
    tier: int = None

class RF4FriendData(NamedTuple):
    apid: int = 0
    name: str = None
    loc_name: str = None
    index: int = 0
    tier: int = 0
    liked_item: str = None
    loved_item: str = None

class RF4TameData(NamedTuple):
    apid: int = 0
    name: str = None
    loc_name: str = None
    index: int = 0
    tier: int = 0
    liked_item: str = None
    drop_rates: list = None
    region: str = None
    produce: str = None
    drop: list = None
    boss: bool = False

class RF4OutfitData(NamedTuple):
    apid: int = 0
    name: str = None
    loc_name: str = None
    region: str = "Selphia Clothing Shop"
    byte: int = 0
    mask: int = 0
    tier: int = 0
    cost: int = 0

class RF4LocationData(NamedTuple):
    name: str = None
    region: str = "Selphia"
    address: Optional[int] = None
    can_create: Callable[["RF4World"], bool] = lambda world: True
    locked_item: Optional[str] = None
    item_id: Optional[int] = None
    #item_type: Optional[str] = None
    loc_type: Optional[str] = None
    required_items: Optional[list] = None
    loc_name: str = None


# def get_class_defaults(cell, class_type):
#     default_dict = class_type._field_defaults
#     for cell_name in cell:
#         cell_default = default_dict[cell_name.lower()]
#         if not default_dict[cell_name.lower()]:
#             cell[cell_name] = cell_default
#     return cell

def match_csv(csv_name, csvdata, cell):
    match csv_name:
        case "Rune Factory 4 AP - Shipments":
            csvdata[cell["Name"]] = parse_shipment(cell)
        case "Rune Factory 4 AP - Chests":
            csvdata[cell["ID"]] = parse_chest(cell)
        case "Rune Factory 4 AP - Recipes":
            csvdata[cell["Name"]] = parse_recipe(cell)
        case "Rune Factory 4 AP - Requests Info":
            csvdata[cell["Name"]] = parse_request(cell)
        case "Rune Factory 4 AP - Tame":
            csvdata[cell["Name"]] = parse_tame(cell)
        case _:
            logger.warning(f"csv {csv_name} not found")
    return csvdata




def parse_shipment(cell):
    for col_name, cell_value in cell.items():
        match col_name:
            case "Name":
                cell[col_name] = cell[col_name].replace("/",'')
            case "ID" | "APID":
                if cell_value:
                    cell[col_name] = int(cell[col_name],16)
            case "Byte" | "Bit" | "Level" | "Rarity" | "Filler Weight" | "Filler Count":
                if cell_value:
                    cell[col_name] = int(cell[col_name])
            case "Tier" | "Buy" | "Sell":
                if cell_value:
                    cell[col_name] = int(cell[col_name])
                else:
                    cell[col_name] = 0
            case "Region":
                if not cell_value:
                    cell[col_name] = "Selphia"
            case "Required items":
                if cell_value:
                    cell[col_name] = (cell['Required items']).split(" + ")
            case "Shipable":
                if cell_value == "FALSE":
                    cell[col_name] = False
                else:
                    cell[col_name] = True
    
    return RF4ShipData(name = cell['Name'], id = cell["ID"], start_byte = cell["Byte"], start_bit = cell["Bit"], 
                    apid = cell["APID"], type= cell["Type"], region = cell["Region"], 
                    tier= cell["Tier"], shipable=bool(cell["Shipable"]), buy_value = cell["Buy"], sell_value = cell["Sell"], 
                    monster = cell["Monster"], fill_weight = cell["Filler Weight"], fill_amount = cell["Filler Count"], required_items = cell["Required items"],
                    loc_name= f"{cell["Region"]} Shipment - {cell['Name']}" )

def parse_chest(cell):
    for col_name, cell_value in cell.items():
        match col_name:
            case "ID" | "APID" | "Byte" | "Mask":
                if cell_value:
                    cell[col_name] = int(cell[col_name],16)
            case "Tier":
                if cell_value:
                    cell[col_name] = int(cell[col_name])
            case "Region":
                if not cell_value:
                    cell[col_name] = "Selphia"
            case "Items":
                if cell_value:
                    cell[col_name] = (cell['Items']).split(" + ")
            case "Recipe":
                if cell_value:
                    cell[col_name] = (cell['Recipe']).split(" + ")
    return RF4ChestData(name = cell['Location Name'],loc_name=cell['Location Name'], id = cell['ID'], apid = cell["APID"], room= cell['Room Code'], recipe=cell["Recipe"],
                        items = cell["Items"] , tier = cell["Tier"], region = cell["Region"], byte= cell['Byte'], mask= cell['Mask'], notes= cell['Notes'])


def parse_recipe(cell):
    for col_name, cell_value in cell.items():
        match col_name:
            case "ID" | "Byte" | "Mask":
                if cell_value:
                    cell[col_name] = int(cell[col_name],16)
            case "Level":
                if cell_value:
                    cell[col_name] = int(cell[col_name])
            case "Type":
                match cell[col_name]:
                    case "Forging":
                        loc_string = f"Forge Shipment"
                    case "Crafting":
                        loc_string = f"Crafting Shipment"
                    case "Chemistry":
                        loc_string = f"Selphia Shipment"
                    case "Cooking":
                        match cell['Subtype']:
                            case "Mixer" | "Knife" | "Frying Pan":
                                loc_string = "EZ Cooking Shipment"
                            case "Oven" | "Steamer" | "Pot":
                                loc_string = "Pro Cooking Shipment"
                            case _:
                                loc_string = "Cooking Shipment"
                    case _:
                        loc_string = f"Selphia Shipment"

            case "Ingredients":
                if cell_value:
                    cell[col_name] = (((cell['Ingredients']).replace('"','')).split(" + "))
    return RF4RecipeData(name = cell['Name'], id = cell['ID'], craft_type = cell["Type"], level= cell['Level'],
                        subtype = cell["Subtype"], byte= cell['Address'], mask= cell['Mask'], ingredients= cell['Ingredients'],
                        loc_name= f"{loc_string} - {cell['Name']}")

def parse_request(cell):
    for col_name, cell_value in cell.items():
        match col_name:
            case "APID" | "Byte" | "Mask":
                if cell_value:
                    cell[col_name] = int(cell[col_name],16)
            case "Item Requirements":
                if cell_value:
                    cell[col_name] = (((cell[col_name]).replace('"','')).split(" + "))
                else:
                    cell[col_name] = []
    return RF4RequestData(name = cell['Name'], apid = cell['APID'],  byte= cell['Byte'], mask= cell['Mask'], 
                          request_req = cell['Region Connect'], item_req= cell['Item Requirements'],
                          loc_name= f"Selphia Request - {cell['Name']}")
            

def parse_tame(cell):
    for col_name, cell_value in cell.items():
        match col_name:
            case "ID" | "APID":
                if cell_value:
                    cell[col_name] = int(cell[col_name],16)
            case "Tier":
                if cell_value:
                    cell[col_name] = int(cell[col_name])
            case "Region":
                if not cell_value:
                    cell[col_name] = "Selphia"
            case "Drop":
                if cell_value:
                    cell_items = [item for item in (cell[col_name].split(" + ")) if item != '']
                    cell[col_name] = cell_items
            case "Is Boss":
                if cell_value == "Yes":
                    cell[col_name] = True
                else:
                    cell[col_name] = False
            case "Drop Chance":
                if cell_value:
                    cell_items = [chance for chance in (cell[col_name].split(" + ")) if chance != 0]
                    cell[col_name] = cell_items
            
    return RF4TameData(name = cell['Name'], index = cell['ID'], apid = cell["APID"], region= cell['Region'], produce=cell["Produce"], boss= cell['Is Boss'],
                        tier= cell['Tier'], drop= cell['Drop'], liked_item= cell['Friend Item'], drop_rates = cell['Drop Chance'], loc_name= f"{cell["Region"]} Tame - {cell['Name']}")



def parse_csv(csv_name):
    #import csv
    import pkgutil

    # ##DEBUGGING PURPOSES ONLY
    # import requests
    # match csv_name:
    #     case "Rune Factory 4 AP - Shipments":
    #         gid = "2037917468"
    #     case "Rune Factory 4 AP - Chests":
    #         gid = "868007808"
    #     case "Rune Factory 4 AP - Recipes":
    #         gid = "206530369"
    #     case _:
    #         gid = None
    # #URL = f'https://docs.google.com/spreadsheets/d/1YU6grqkNfm-fRCV1gIQCDBU466W79-UGnRhtYPxam4Q//export?format=csv&gid={SHEET_ID}'
    
    # if gid is not None:
    #     url = f"https://docs.google.com/spreadsheets/d/1YU6grqkNfm-fRCV1gIQCDBU466W79-UGnRhtYPxam4Q/export?format=csv&gid={gid}"
    #     headers = {
    #             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    #         }
    #     response = (requests.get(url, headers=headers))
    #     raw_csv_text = response.text
    #     rows = str.split(raw_csv_text,"\r\n")
    # else:
        # END DEBUG, Untab this later
    raw_csv_text =  str(pkgutil.get_data(__name__, f"data/{csv_name}.csv"))
    rows = str.split(raw_csv_text,"\\r\\n")
    #raw_csv_text =  str(pkgutil.get_data(__name__, f"data/{csv_name}.csv"))
    csvdata = {}
    
    col = []
    row_num = 0
    for row_raw in rows:
        row= str.split(row_raw, ",")
        try:
            row[1]
        except Exception as e:
            #logger.warning(f"error: {e} - {row}")
            break
        if row_num == 0:
            #logger.warning(f"Parsing CSV Columns: {row}")
            for col_name in row:
                if col_name[:2] == 'b"' or col_name[:2] == "b'":
                    col_name = col_name[2:]
                col.append(col_name)
            row_num += 1
            continue
        for x in range(len(row)):
            if row[x] == '':
                row[x] = None
        
        cell = {}
        for col_name in col:
            cell[col_name] = row[col.index(col_name)]
        csvdata = match_csv(csv_name, csvdata, cell)
        row_num += 1
    return csvdata

shipment_data_table = parse_csv("Rune Factory 4 AP - Shipments")
chest_data_table = parse_csv("Rune Factory 4 AP - Chests")
recipe_data_table = parse_csv("Rune Factory 4 AP - Recipes")
request_data_table = parse_csv("Rune Factory 4 AP - Requests Info")
tame_data_table = parse_csv("Rune Factory 4 AP - Tame")

#Generate Frienship data
friend_data_table = {}
for name, index in friendsanity_data.items():
    for level in range(0,10):
        ap_address = 0x1C4300 + ((index * 0x10) + level)
        friend_data_table[f"{name} level {level+1}"] = RF4FriendData(
            apid = ap_address, name = f"{name} level {level+1}", index= index, tier= level+1, 
            liked_item=friend_items[name][0], loved_item=friend_items[name][1], loc_name= f"Selphia Friendship - {name} level {level+1}"
        )

# Generate Clothing Data
outfit_data_table = {}
index = 0
for name, data in outfit_data.items():
    outfit_byte = data[0]
    outfit_mask = data[1]
    outfit_cost = data[2]
    ap_address = 0x1C45D0 + index
    match outfit_cost:
        case 980:
            outfit_tier = 1
        case 1500:
            outfit_tier = 2
        case 2800:
            outfit_tier = 3
        case 24000:
            outfit_tier = 5
        case 36000:
            outfit_tier = 7
        case _:
            outfit_tier = 3
    outfit_data_table[name] = RF4OutfitData(
        apid=ap_address, name=name, loc_name= f"Selphia Clothing Shop - {name}", 
        byte=outfit_byte, mask=outfit_mask, tier = outfit_tier, cost=outfit_cost
    )
    index += 1
#logger.warning(f"{friend_data_table}")

#Shipments
location_data_table= {data.name: RF4LocationData(
    item_id= data.id, address=data.apid, loc_type= "shipment", region=data.region, name=data.name, loc_name= data.loc_name)
    for name, data in shipment_data_table.items() if data.shipable == True}

# Chests
location_data_table.update({data.name: 
    RF4LocationData(address=data.apid,region=data.region,name=data.name,loc_name= data.name, loc_type="chest")
    for id, data in chest_data_table.items()}) 

# Requestsanity
location_data_table.update({data.name: 
    RF4LocationData(address=data.apid,region=data.name,name=data.name, loc_name= data.loc_name,loc_type="request")
    for name, data in request_data_table.items()}) 

#Friendsanity
location_data_table.update({name:
    RF4LocationData(address=data.apid,region="Selphia",name=data.name,loc_name = data.loc_name, loc_type="friendship")
    for name, data in friend_data_table.items()
})

#Tamesanity
location_data_table.update({name:
    RF4LocationData(address=data.apid, region=data.region, loc_type="tame", name=data.name, loc_name= data.loc_name)
    for name, data in tame_data_table.items() if data.liked_item is not None
})
#Outfitsanity
location_data_table.update({name:
    RF4LocationData(address=data.apid, region=data.region, name=name, loc_name=data.loc_name, loc_type= "outfit")
    for name, data in outfit_data_table.items()
})

location_table = {data.loc_name: data.address for name, data in location_data_table.items() if data.address is not None}
locked_locations = {name: data for name, data in location_data_table.items() if data.locked_item}

shipment_data = {data.apid: [data.start_byte, data.start_bit] for name, data in shipment_data_table.items() if data.shipable == True}
chest_data =    {data.apid: [data.byte, data.mask] for name, data in chest_data_table.items()}
request_data =  {data.apid: [data.byte, data.mask] for name, data in request_data_table.items() if data.mask is not None}
tame_data =     {data.index: data.apid for name, data in tame_data_table.items() if data.liked_item is not None}
recipe_levels = {data.name: [data.level, data.craft_type, data.ingredients] for name, data in recipe_data_table.items() if data.level is not None}

spell_list = [data.loc_name for name, data in shipment_data_table.items() if data.type == "Spell" and data.shipable == True]
filler_items = {name: [data.apid, data.fill_weight, data.id, data.type, data.fill_amount] for name, data in shipment_data_table.items() if data.fill_weight != 0 and data.fill_weight is not None}
chest_recipes = {name: data.recipe for name, data in chest_data_table.items() if data.recipe is not None}
item_to_region = {name: data.region for name, data in shipment_data_table.items() if data.shipable == True}
request_rules = {name: [data.request_req, data.item_req] for name, data in request_data_table.items() if data.item_req is not None}
request_list = list(request_data_table)
top_requests = [name for name, data in request_data_table.items() if "Fenrir" in data.item_req]
request_data = {data.apid: [data.byte, data.mask] for name, data in request_data_table.items() if data.byte is not None}

outfit_game_data = {data.apid: [data.byte, data.mask] for name, data in outfit_data_table.items()}

ship_loc_name = {data.name: data.loc_name  for name, data in shipment_data_table.items()}
recipe_loc_name = {data.name:data.loc_name  for name, data in recipe_data_table.items()}
request_loc_name = {data.name: data.loc_name  for name, data in request_data_table.items()}
friend_loc_name = {data.name: data.loc_name  for name, data in friend_data_table.items()}
tame_loc_name = {data.name: data.loc_name  for name, data in tame_data_table.items()}
boss_tame_list = [data.loc_name for name, data in tame_data_table.items() if data.boss == True]
top_crop_list = [data.loc_name for name, data in shipment_data_table.items() if data.tier >= 6 and (data.type == "Crop" or data.type == "Large Crop" or data.type == "Gold Crop")]

ship_loc_list = [data.loc_name for name, data in shipment_data_table.items()]
chest_loc_list = [data.loc_name for name, data in chest_data_table.items()]
request_loc_list = [data.loc_name for name, data in request_data_table.items()]
friend_loc_list = [data.loc_name for name, data in friend_data_table.items()]
tame_loc_list = [data.loc_name for name, data in tame_data_table.items()]
outfit_loc_list = [data.loc_name for name, data in outfit_data_table.items()]

recipe_tiering = {}
for name, data in recipe_data_table.items():
    #logger.warning(f"{name}")
    recipe_tier_list = []
    for ingredient in data.ingredients:
        recipe_tier_list.append(shipment_data_table[ingredient].tier)
    recipe_tier = max(recipe_tier_list)
    #recipe_data_table[name].tier = recipe_tier
    if not recipe_tiering.get(data.subtype):
        recipe_tiering[data.subtype] = {}
    if not recipe_tiering.get(data.subtype, {}).get(recipe_tier):
        recipe_tiering[data.subtype][recipe_tier] = []
    recipe_tiering[data.subtype][recipe_tier].append(name)
    # recipe_tiering[name] = [data.subtype, max(recipe_tier_list)]
#logger.warning(f"Recipe tiers:\n{recipe_tiering}")
bugged_locs = [
    "Sechs Territory F1 I2 Chest - Mystery Potion x x3 + Levelizer"
]

