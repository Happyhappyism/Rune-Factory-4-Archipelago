from .Locations import shipment_data_table, chest_data_table, request_data_table, tame_data_table, boss_data_table, \
outfit_data_table, barrier_data_table, box_data_table, search_data_table, festival_data_table, friend_data_table, recipe_data_table


shipment_data = {data.apid: [data.start_byte, data.start_bit] for name, data in shipment_data_table.items() if data.shipable == True}
chest_data =    {data.apid: [data.byte, data.mask] for name, data in chest_data_table.items()}
request_data =  {data.apid: [data.byte, data.mask, data.prog] for name, data in request_data_table.items() if data.include}
tame_data =     {data.index: data.apid for name, data in tame_data_table.items() if data.liked_item is not None}
boss_kill_data ={data.apid: data.boss_id for name, data in boss_data_table.items() if data.boss_id is not None}
outfit_game_data = {data.apid: [data.byte, data.mask] for name, data in outfit_data_table.items()}
barrier_flag_data = {data.apid: data.field_flag for name, data in barrier_data_table.items()}
box_flag_data = {data.apid: data.field_flag for name, data in box_data_table.items()}
search_flag_data = {data.apid: data.field_flag for name, data in search_data_table.items()}
festival_data = {data.apid: [data.id, data.rank] for name, data in festival_data_table.items()}

ship_loc_list = [data.loc_name for name, data in shipment_data_table.items()]
chest_loc_list = [data.loc_name for name, data in chest_data_table.items()]
request_loc_list = [data.loc_name for name, data in request_data_table.items()]
friend_loc_list = [data.loc_name for name, data in friend_data_table.items()]
tame_loc_list = [data.loc_name for name, data in tame_data_table.items()]
outfit_loc_list = [data.loc_name for name, data in outfit_data_table.items()]
barrier_loc_list = [data.loc_name for name, data in barrier_data_table.items()]
box_loc_list = [data.loc_name for name, data in box_data_table.items()]
search_loc_list = [data.loc_name for name, data in box_data_table.items()]
boss_loc_list = [data.loc_name for name, data in boss_data_table.items()]
festival_loc_list = [data.loc_name for name, data in festival_data_table.items()]

spell_list = [data.loc_name for name, data in shipment_data_table.items() if data.type == "Spell" and data.shipable == True]
ship_loc_name = {data.name: data.loc_name  for name, data in shipment_data_table.items()}
recipe_loc_name = {data.name:data.loc_name  for name, data in recipe_data_table.items()}
request_loc_name = {data.name: data.loc_name  for name, data in request_data_table.items()}
friend_loc_name = {data.name: data.loc_name  for name, data in friend_data_table.items()}
tame_loc_name = {data.name: data.loc_name  for name, data in tame_data_table.items()}
boss_tame_list = [data.loc_name for name, data in tame_data_table.items() if data.boss == True]
top_crop_list = [data.loc_name for name, data in shipment_data_table.items() if data.tier >= 6 and (data.type == "Crop" or data.type == "Large Crop" or data.type == "Gold Crop")]