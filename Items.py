from typing import Callable, Dict, NamedTuple, Optional, TYPE_CHECKING

from BaseClasses import Item, ItemClassification
from .Locations import shipment_data_table #filler_items,
import logging
if TYPE_CHECKING:
    from . import RF4World
    
logger = logging.getLogger("Rune Factory 4 Items")
class RF4Item(Item):
    game = "Rune Factory 4"

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


def match_csv(csv_name, csvdata, cell):
    match csv_name:
        case "Rune Factory 4 AP - Items":
            csvdata[cell["Name"]] = parse_items(cell)
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
                    set_byte = cell['Set Byte'],set_bit = cell['Set Bit'],reset_byte = cell['Reset Byte'],reset_bit = cell['Reset Bit'],)

def parse_csv(csv_name):
    #import csv
    import pkgutil
    raw_csv_text =  str(pkgutil.get_data(__name__, f"data/{csv_name}.csv"))
    csvdata = {}
    rows = str.split(raw_csv_text,"\\r\\n")
    col = []
    row_num = 0
    for row_raw in rows:
        row= str.split(row_raw, ",")
        try:
            row[1]
        except Exception as e:
            logger.warning(f"error: {e} - {row}")
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
    return csvdata

item_data_table = parse_csv("Rune Factory 4 AP - Items")


item_data_table.update({
    name: RF4ItemData(code = data.apid, type=ItemClassification.filler, num_exist= 0, fillweight= data.fill_weight, item_id= data.id, item_type=data.type, amount=data.fill_amount, group="I", working = True) for name, data in shipment_data_table.items() if data.shipable == True
})
#logger.warning(f"item table: {item_data_table}")
#logger.warning(f"fill_weights= {[data.fillweight for name, data in item_data_table.items() if data.type == ItemClassification.filler and (data.fillweight is not None and data.fillweight != 0)]}")
item_table = {name: data.code for name, data in item_data_table.items() if (data.code is not None)}
item_id_to_name = {data.code: name for name, data in item_data_table.items() if (data.code is not None)}
item_filler = [name for name, data in item_data_table.items() if data.type == ItemClassification.filler and (data.fillweight is not None and data.fillweight != 0)]
item_filler_weight = [data.fillweight for name, data in item_data_table.items() if data.type == ItemClassification.filler and (data.fillweight is not None and data.fillweight != 0)]

trap_filler = [name for name, data in item_data_table.items() if data.type == ItemClassification.trap and (data.fillweight is not None and data.fillweight != 0)]
trap_filler_weight = [data.fillweight for name, data in item_data_table.items() if data.type == ItemClassification.trap and (data.fillweight is not None and data.fillweight != 0)]


story_flag_items = {data.code:name for name, data in item_data_table.items() if data.group == "F"}
order_flag_items = {data.code:name for name, data in item_data_table.items() if data.group == "L"}
physical_items = {data.code:name for name, data in item_data_table.items() if data.group == "I"}
special_items = {data.code:name for name, data in item_data_table.items() if data.group == "S"}
progressive_items = {data.code:name for name, data in item_data_table.items() if data.group == "P"}
perm_items = {data.code:name for name, data in item_data_table.items() if data.permanent == True}
trap_items = {data.code:name for name, data in item_data_table.items() if data.group == "T"}
area_items = [
    "Obsidian Bridge", "Autumn Bridge", "Maya Bridge", "Cerezo Bridge", "Winters Grasp", "Chipsqueek Guide",
    "Forging License", "Crafting License", "EZ Cooking License", "Pro Cooking License", "Etherlink", "Volkanon Axe"
    ]
top_tools = ["Legendary Sickle","Sacred Pole", "Joy Waterpot", "Blessed Hoe", "Platinum Hammer","Miracle Axe"]
wep_cats = ["Fist", "Dual Blade", "Short Sword", "Staff", "Axe/Hammer", "Long Sword", "Spear"]