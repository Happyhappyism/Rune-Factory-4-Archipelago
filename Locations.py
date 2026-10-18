from typing import Callable, Dict, NamedTuple, Optional, TYPE_CHECKING

from BaseClasses import Location

import logging
import pkgutil
import json
from .process_csv import parse_csv, RF4TameData
from .game_data import friendsanity_data, friend_items, outfit_data, festival_list

#from .com_ap_methods import parse_csv
if TYPE_CHECKING:
    from . import RF4World

logger = logging.getLogger("Rune Factory 4 Locations")

class RF4Location(Location):
    game = "Rune Factory 4"

class RF4MapObj(NamedTuple):
    apid: int = 0
    region: str = None
    room_number: int = 0
    field_flag: int = None
    loc_name: str = None
    map_type: str = None

class RF4FriendData(NamedTuple):
    apid: int = 0
    name: str = None
    loc_name: str = None
    index: int = 0
    tier: int = 0
    liked_item: str = None
    loved_item: str = None

class RF4OutfitData(NamedTuple):
    apid: int = 0
    name: str = None
    loc_name: str = None
    region: str = "Selphia Clothing Shop"
    byte: int = 0
    mask: int = 0
    tier: int = 0
    cost: int = 0

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

def parse_mapobj_json(json_name, ap_base, loc_type):
    mobj_file = pkgutil.get_data(__name__, f"data/{json_name}.json").decode("utf-8")
    mobj_json = json.loads(mobj_file)
    mapobj_data_table = {}
    ap_address = ap_base
    for map_file in mobj_json:
        field_flags = set(map_file["field_flags"])
        map_region = map_file["region"]
        room_num = map_file["room_number"]
        mtype = map_file["map_type"]
        base_name = f"{map_region} {loc_type} - Room {room_num}"
        if len(field_flags) > 1:
            flag_idx = 0
            for flag in field_flags:
                flag_idx += 1
                ap_address += 1
                name = base_name + f" {loc_type} {flag_idx}"
                mapobj_data_table[name] = RF4MapObj(
                            apid = ap_address, field_flag = flag, region = map_region, room_number = room_num, map_type= mtype, loc_name = name
                        )
        else:
            ap_address +=1
            flag = next(iter(field_flags))
            mapobj_data_table[base_name] = RF4MapObj(
                apid = ap_address, field_flag = flag, region = map_region, room_number = room_num, map_type= mtype, loc_name = base_name
            )
    return mapobj_data_table

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

# Generate Barriers and Boxes
barrier_data_table = parse_mapobj_json("barrier_flags", 0x1C4600, "Barrier")
box_data_table = parse_mapobj_json("box_flags", 0x1C4700, "Box")
search_data_table = parse_mapobj_json("search_flags", 0x1C4800, "Search")

# Boss data table
boss_data_table = {name: RF4TameData(
    apid = 0x1C4900 + data.boss_id, region= data.region, name=name, loc_name= f"{data.region} - Defeat {name}", index=data.index,
    tier=data.tier, boss_id= data.boss_id, boss=True
) for name, data in tame_data_table.items() if data.boss and data.boss_id is not None}

# Generate Festival data
fest_rank_names = ["Gold", "Silver", "Bronze"]
festival_data_table = {}
fest_idx = 0
for festival, fest_region in festival_list.items():
    base_apid = 0x1C4940 + (fest_idx * 4)
    for festival_rank in range(3):
        rank_name = fest_rank_names[festival_rank]
        apid = base_apid + festival_rank
        fest_loc_name = f"Selphia Festival - {festival} {rank_name}"
        festival_data_table[f"{festival} {rank_name}"] = RF4FestivalData(
            apid = apid, region = fest_region, id = fest_idx, loc_name=fest_loc_name, rank = festival_rank + 1
        )
    fest_idx += 1
        

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
# Barriersanity
location_data_table.update({name:
    RF4LocationData(address=data.apid, region=data.region, name=name, loc_name=data.loc_name, loc_type= "barrier")
    for name, data in barrier_data_table.items()
})
# Boxsanity
location_data_table.update({name:
    RF4LocationData(address=data.apid, region=data.region, name=name, loc_name=data.loc_name, loc_type= "box")
    for name, data in box_data_table.items()
})
# Searchsanity
location_data_table.update({name:
    RF4LocationData(address=data.apid, region=data.region, name=name, loc_name=data.loc_name, loc_type= "search")
    for name, data in search_data_table.items()
})
# Boss Sanity
location_data_table.update({data.loc_name:
    RF4LocationData(address=data.apid, region=data.region, loc_type="boss", name=data.name, loc_name= data.loc_name)
    for name, data in boss_data_table.items() if data.boss_id is not None
})
# Festival Sanity
location_data_table.update({name:
    RF4LocationData(address=data.apid, region=data.region, loc_type="festival", name=data.name, loc_name= data.loc_name)
    for name, data in festival_data_table.items() if data.id is not None
})

location_table = {data.loc_name: data.address for name, data in location_data_table.items() if data.address is not None}
locked_locations = {name: data for name, data in location_data_table.items() if data.locked_item}

recipe_levels = {data.name: [data.level, data.craft_type, data.ingredients] for name, data in recipe_data_table.items() if data.level is not None}



filler_items = {name: [data.apid, data.fill_weight, data.id, data.type, data.fill_amount] for name, data in shipment_data_table.items() if data.fill_weight != 0 and data.fill_weight is not None}
chest_recipes = {name: data.recipe for name, data in chest_data_table.items() if data.recipe is not None}
item_to_region = {name: data.region for name, data in shipment_data_table.items() if data.shipable == True}
request_rules = {name: [data.request_req, data.item_req] for name, data in request_data_table.items()}
request_list = list(request_data_table)
top_requests = [name for name, data in request_data_table.items() if "Fenrir" in data.item_req]
# request_data = {data.apid: [data.byte, data.mask] for name, data in request_data_table.items() if data.byte is not None}






recipe_tiering = {}


for name, data in recipe_data_table.items():
    recipe_tier_list = []
    for ingredient in data.ingredients:
        recipe_tier_list.append(shipment_data_table[ingredient].tier)
    recipe_tier = max(recipe_tier_list)
    if not recipe_tiering.get(data.subtype):
        recipe_tiering[data.subtype] = {}
    if not recipe_tiering.get(data.subtype, {}).get(recipe_tier):
        recipe_tiering[data.subtype][recipe_tier] = []
    recipe_tiering[data.subtype][recipe_tier].append(name)
bugged_locs = [
    "Sechs Territory F1 I2 Chest - Mystery Potion x3 + Levelizer"
]
