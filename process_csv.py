from typing import TYPE_CHECKING, Callable, Set, Optional, List, Dict, Any, NamedTuple
from BaseClasses import Item, ItemClassification
import logging
import pkgutil
if TYPE_CHECKING:
    from . import RF4World

logger = logging.getLogger("Rune Factory 4 CSV")
class RF4ItemData(NamedTuple):
    name: Optional[str] = None
    code: Optional[int] = None
    type: ItemClassification = ItemClassification.filler
    num_exist: int = 1
    item_id: Optional[int] = None
    item_type: Optional[str] = None
    can_create: Callable[["RF4World"], bool] = lambda world: True
    fillweight: Optional[int] = None
    id: Optional[int] = None
    amount: Optional[int] = 1
    set_byte: Optional[int] = None
    set_bit: Optional[int] = None
    reset_byte:  Optional[int] = None
    reset_bit:  Optional[int] = None
    permanent: Optional[bool] = False
    working: Optional[bool] = True
    group: Optional[str] = None

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
    prog: int = 0
    reqid: int = 0
    include: bool = False
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
    boss_id: int = None

class RF4OutfitData(NamedTuple):
    apid: int = 0
    name: str = None
    loc_name: str = None
    region: str = "Selphia Clothing Shop"
    byte: int = 0
    mask: int = 0
    tier: int = 0
    cost: int = 0

class RF4MapObj(NamedTuple):
    apid: int = 0
    region: str = None
    room_number: int = 0
    field_flag: int = None
    loc_name: str = None
    map_type: str = None

class RF4FestivalData(NamedTuple):
    name: str = None
    apid: int = 0
    region: str = None
    id: int = None
    loc_name: str = None
    season: int = None
    day: int = None
    prince_points: int = None
    rank: int = None

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
        case "Rune Factory 4 AP - Items":
            csvdata[cell["Name"]] = parse_items(cell)
        case "Rune Factory 4 AP - Audio":
            csvdata[cell["ID"]] = parse_music(cell)
        case _:
            logger.warning(f"csv {csv_name} not found")
    return csvdata


def parse_items(cell):
    for col_name, cell_value in cell.items():
        match col_name:
            case "Name":
                cell[col_name] = cell[col_name].replace("\\",'')
            case "ID" | "APID" |"Set Byte" | "Reset Byte":
                if cell_value:
                    cell[col_name] = int(cell[col_name],16)
            case  "Set Bit" | "Reset Bit" | "Filler Weight" | "Count":
                if cell_value:
                    cell[col_name] = int(cell[col_name])
            case "Permanent":
                if cell_value == "TRUE":
                    cell[col_name] = True
                else:
                    cell[col_name] = False
            case "Classification":
                match cell[col_name]:
                    case "progression":
                        cell[col_name] = ItemClassification.progression
                    case "useful":
                        cell[col_name] = ItemClassification.useful
                    case "trap":
                        cell[col_name] = ItemClassification.trap
                    case _:
                        cell[col_name] = ItemClassification.filler
            case "Implemented":
                if cell_value == "TRUE":
                    cell[col_name] = True
                else:
                    cell[col_name] = False
    return RF4ItemData(name = cell['Name'], id = cell["ID"], code = cell["APID"], num_exist = cell["Count"], type=cell["Classification"],
            item_type=cell["Item Type"], fillweight = cell['Filler Weight'], group= cell['Group'], permanent= cell['Permanent'],working = cell["Implemented"],
            set_byte = cell['Set Byte'],set_bit = cell['Set Bit'],reset_byte = cell['Reset Byte'],reset_bit = cell['Reset Bit'])

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
                else:
                    cell[col_name] = None
            case "Prog" | "Request ID":
                if cell_value:
                    cell[col_name] = int(cell[col_name])
                else:
                    cell[col_name] = None
            case "Item Requirements":
                if cell_value:
                    cell[col_name] = (((cell[col_name]).replace('"','')).split(" + "))
                else:
                    cell[col_name] = []
            case "Include":
                if cell_value:
                    cell[col_name] = bool(cell[col_name])
    return RF4RequestData(name = cell['Name'], apid = cell['APID'],  byte= cell['Byte'], mask= cell['Mask'], prog= cell['Prog'],
                          request_req = cell['Region Connect'], item_req= cell['Item Requirements'], reqid= cell['Request ID'], include= cell['Include'],
                          loc_name= f"Selphia Request - {cell['Name']}")
            

def parse_tame(cell):
    for col_name, cell_value in cell.items():
        match col_name:
            case "ID" | "APID":
                if cell_value:
                    cell[col_name] = int(cell[col_name],16)
            case "Tier" | "Boss ID":
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
            
    return RF4TameData(name = cell['Name'], index = cell['ID'], apid = cell["APID"], region= cell['Region'], produce=cell["Produce"], boss= cell['Is Boss'], boss_id = cell['Boss ID'],
                        tier= cell['Tier'], drop= cell['Drop'], liked_item= cell['Friend Item'], drop_rates = cell['Drop Chance'], loc_name= f"{cell["Region"]} Tame - {cell['Name']}")

def parse_music(cell):
    for col_name, cell_value in cell.items():
        match col_name:
            case "Name":
                cell[col_name] = cell[col_name].replace("\\",'')
            case "ID":
                if cell_value:
                    cell[col_name] = int(cell[col_name],16)
            case  "Length":
                if cell_value:
                    cell[col_name] = float(cell[col_name])
            case "Tags":
                if cell_value:
                    cell[col_name] = (cell[col_name]).split(" + ")
            case "Implemented":
                if cell_value == "TRUE":
                    cell[col_name] = True
                else:
                    cell[col_name] = False
    return MusicData(name = cell['Name'], id = cell["ID"], type = cell["Type"], format = cell["Format"], alias = cell["Alias"], 
        tags = cell["Tags"], game = cell["Game"], length = cell["Length"], group = cell["Group"])

def parse_csv(csv_name):
    raw_csv_text = pkgutil.get_data(__name__, f"data/{csv_name}.csv").decode("utf-8").replace("\r\n","\n")
    rows = str.split(raw_csv_text,"\n")
    csvdata = {}
    
    col = []
    row_num = 0
    for row_raw in rows:
        row= str.split(row_raw, ",")
        try:
            row[1]
        except Exception as e:
            break
        if row_num == 0:
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
    #logger.info(f"csv: {csvdata}")
    return csvdata