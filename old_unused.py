

# def read_playerObj(player_base,stat_type):
#     player_obj_dict = {
#         "combat_stat": 0x130,
#         "skill_level": 0x138,
#     }
#     base_pointer = pc_read_ptr(p, player_base+player_obj_dict[stat_type])
#     return base_pointer

# def get_skill_level(playerObj, skill_name):
#     skill_base = pc_read_ptr(p, playerObj + 0x138)
#     skill_level = pc_read(p, skill_base + skill_level_offsets[skill_name])
#     return skill_level


# def get_ptr(diff_offset, cmp_offset, byte_txt):
#     scan_adr = pc_aob_scan(p, byte_txt)
#     if scan_adr:
#         diff = pc_read(p, scan_adr+diff_offset)
#         comp_adr = scan_adr + cmp_offset
#         exp_adr = comp_adr + diff
#         return exp_adr
#     else:
#         return None

# def get_RF4D():
#     scan_list = pc_aob_scan_multi(p, b"\\x52\\x46\\x34\\x44")
#     logger.warning(f"scan_list = {scan_list}")
#     if scan_list:
#         for scan_adr in scan_list:
#             bcheck = pc_readb(p, scan_adr+0xC)
#             if bcheck == 0:
#                 break
#             bcheck = None
#         return scan_adr
#     else:
#         return None

# def update_seed_options(self):

#     try:
#         # Seed options were written to the save file and are here read.
#         #self.death_link = bool(self.seed_options[0] & 0x1)
#         #self.shopbox_link = bool(self.seed_options[0] & 0x4)
#         #self.fortress_sphere_need = self.seed_options[2]
#         #self.prana_sphere_need = self.seed_options[3]
#         # self.game_goal = self.seed_options[4]
#         self.drop_boost = self.seed_options[5]
#         #ctx.require_baths = ctx.seed_options[4] & 0x4 >> 2
#         #ctx.ship_percent_need = ctx.seed_options[4] & 0xF8 >> 3
#     except Exception as e:
#         loggerExt.critical(f"Error updating seed options {e}\n{traceback.format_exc()}")

# match story_flag_items[item_id]:
#     case "Cerezo Bridge":
#         pc_set_bit(ctx.pm, airship_base, 7) # Secerezo Hill
#         pc_set_bit(ctx.pm, airship_base + 1, 0) # Indra Cave
#         pc_set_bit(ctx.pm, airship_base + 1, 4) # Spring Field
#         pc_set_bit(ctx.pm, airship_base + 2, 0) # Sercerzo Lake
#         pc_set_bit(ctx.pm, airship_base + 2, 6) # Demon's Den
#     case "Volkanon Axe":
#         pc_set_bit(ctx.pm, airship_base, 2) # Water Ruins
#         pc_set_bit(ctx.pm, airship_base + 1, 5) # Summer Field
#         pc_set_bit(ctx.pm, airship_base + 2, 1) # Keeno Lake
#         pc_set_bit(ctx.pm, airship_base + 2, 4) # Cluck Cluck Nest
#     case "Autumn Bridge":
#         pc_set_bit(ctx.pm, airship_base, 4) # Autumn Road
#         pc_set_bit(ctx.pm, airship_base, 5) # Delirium Lava Ruins
#         pc_set_bit(ctx.pm, airship_base + 2, 2) # Autumn River
#         pc_set_bit(ctx.pm, airship_base + 2, 5) # Revival Cave
#     case "Winters Grasp":
#         pc_set_bit(ctx.pm, airship_base + 1, 2) # Sechs Territory
#         pc_set_bit(ctx.pm, airship_base + 1, 7) # Winter Field
#         pc_set_bit(ctx.pm, airship_base + 2, 3) # Silver Lake
#     case "Volkanon Bridge":
#         pc_set_bit(ctx.pm, airship_base, 3) # Obsidian Mansion
#     case "Obsidian Ladder":
#         pc_set_bit(ctx.pm, airship_base, 3) # Obsidian Mansion
#     case "Maya Bridge":
#         pc_set_bit(ctx.pm, airship_base + 1, 1) # Maya Road
#         pc_set_bit(ctx.pm, airship_base + 1, 6) # Autumn Field
#     case "Etherlink":
#         pc_set_bit(ctx.pm, airship_base, 6) # Leon Karnak
#     case _:
#         pass