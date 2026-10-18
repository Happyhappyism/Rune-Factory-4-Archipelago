from typing import Callable, Dict, NamedTuple, Optional, TYPE_CHECKING

from BaseClasses import Item, ItemClassification
from .Locations import shipment_data_table #filler_items,
from .process_csv import parse_csv, RF4ItemData
import logging
if TYPE_CHECKING:
    from . import RF4World
    
logger = logging.getLogger("Rune Factory 4 Items")
class RF4Item(Item):
    game = "Rune Factory 4"

item_data_table = parse_csv("Rune Factory 4 AP - Items")


item_data_table.update({
    name: RF4ItemData(code = data.apid, type=ItemClassification.filler, num_exist= 0, fillweight= data.fill_weight, item_id= data.id, item_type=data.type, amount=data.fill_amount, group="I", working = True) for name, data in shipment_data_table.items() if data.shipable == True
})
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