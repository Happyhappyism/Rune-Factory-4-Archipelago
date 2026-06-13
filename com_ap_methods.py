import random

# This is just a common method library I made for my own apworlds

def parse_manual_logic_rule(rule):
    import re
    item_list = re.findall(r'\|[^|]+\|', rule)
    rule = rule.replace("AND","and")
    rule = rule.replace("OR","or")
    for item in item_list:
        if ":" in item:
            new_item = item.split(":")[0]
            item_count = item.split(":")[1]
            rule = rule.replace(item, f"state.has(\"{new_item[1:]}\",player, {item_count[:-1]})")
        else:
            rule = rule.replace(item, f"state.has(\"{item[1:-1]}\", player)")
    return rule

# Randomization Methods

def split_into_xbit_chunks(byte_array,size):
   #Splits a byte array into chunks of 32 bits (4 bytes).

    chunks = []
    for i in range(0, len(byte_array), size):
        chunk = byte_array[i:i + size]
        # If the last chunk is less than 4 bytes, pad it with zeros
        if len(chunk) < size:
            chunk += b'\x00' * (size - len(chunk)) 
        chunks.append(chunk)
    return chunks

def shuffle_dict(in_dict):
    value_list = list(in_dict.values())
    random.shuffle(value_list)
    shuffled_dict = {}
    keys_list = list(in_dict.keys())
    for i, key in enumerate(keys_list):
        shuffled_dict[key] = value_list[i]
    return shuffled_dict

def randomize_dict_items(my_dict):
    values = list(my_dict.values())
    random.shuffle(values)

    keys = list(my_dict.keys())
    for i, key in enumerate(keys):
        my_dict[key] = values[i]
    return my_dict

def ramdomize_table(tbl,entrysize):
    split_table = split_into_xbit_chunks(tbl,entrysize)
    random.shuffle(split_table)
    result = b''.join(split_table)
    return result

def ramdomize_table_with_exclude(tbl,entrysize,excepts):
    split_table = split_into_xbit_chunks(tbl,entrysize)
    idxshuffle = []
    new_table = []
    for x in range(len(split_table)):
        idxshuffle.append(x)
        new_table.append(b'/x00/x00/x00/x00')
    random.shuffle(idxshuffle)
    for idx in range(len(split_table)):
        if idx in excepts:
            new_table[idx] = split_table[idx]
            continue
        randidx = idxshuffle.pop(0)
        while randidx in excepts:
            randidx = idxshuffle.pop(0)
        new_table[idx] = split_table[randidx]
    result = b''.join(new_table)
    return result

def ramdomize_table_with_exclude_list(tbl,entrysize,excepts,baseoffset):
    # Same as the other function but returns a list of offsets and data to write,
    # Useful when randomizing multiple sets of data to the same table
    split_table = split_into_xbit_chunks(tbl,entrysize)
    idxshuffle = []
    new_table = []
    out_dict = {}
    offset = baseoffset
    for x in range(len(split_table)):
        idxshuffle.append(x)
        new_table.append(b'/x00/x00/x00/x00')
    random.shuffle(idxshuffle)
    for idx in range(len(split_table)):
        
        if idx in excepts:
            new_table[idx] = split_table[idx]
            continue
        randidx = idxshuffle.pop(0)
        while randidx in excepts:
            randidx = idxshuffle.pop(0)
        
        new_table[idx] = split_table[randidx]
        if randidx not in excepts:
            out_dict.update({offset:new_table[idx]})
        offset += entrysize
    #result = b''.join(new_table)
    return out_dict

def randomize_multi_table(tbl,size1,tb2,size2,excepts):
    split_table1 = split_into_xbit_chunks(tbl,size1)
    split_table2 = split_into_xbit_chunks(tb2,size2)
    idxshuffle = []
    new_table1 = []
    new_table2 = []
    for x in range(len(split_table1)):
        idxshuffle.append(x)
        new_table1.append(b'/x00')
        new_table2.append(b'/x00')
    random.shuffle(idxshuffle)

    for idx in range(len(split_table1)):
        #logger.warning(f"{idx} : {idxshuffle}")
        if idx in excepts:
            new_table1[idx] = split_table1[idx]
            new_table2[idx] = split_table2[idx]
            continue 
        randidx = idxshuffle.pop(0)
        while randidx in excepts:
            randidx = idxshuffle.pop(0)
        #logger.warning(f"{idx} - {randidx}")
        new_table1[idx] = split_table1[randidx]
        new_table2[idx] = split_table2[randidx]

    out_tbl_1 = b''.join(new_table1)
    out_tbl_2 = b''.join(new_table2)
    return out_tbl_1, out_tbl_2

def import_binary_bytes(file_name: str, apworld: str):
    from pkgutil import get_data
    get_data(__name__, "data/Rooms.json")
    with open(file_name, "rb") as f:
        data = f.read()
    return bytes(data)

def match_csv():
    return

def parse_csv(csv_name):
    import csv
    import pkgutil
    raw_csv_text =  str(pkgutil.get_data(__name__, f"data/{csv_name}.csv"))
    csvdata = {}
    rows = str.split(raw_csv_text,"\\r\\n")
    col = []
    #logger.warning(f"{}")
    #entrys = len(rows) - 1 - int(rows[1].split(",")[1])
    row_num = 0
    for row_raw in rows:
        row= str.split(row_raw, ",")
        try:
            row[1]
            #logger.warning(f"{row}")
        except Exception as e:
            #logger.warning(f"error: {e} - {row}")
            break
        #if row[1] == hex(entrys)[2:]:
        #   break
        if row_num == 0:
            for col_name in row:
                if col_name[:2] == 'b"' or col_name[:2] == "b'":
                    col_name = col_name[2:]
                col.append(col_name)
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

def randomize_palettes(world, pal_sources):
    from .palette_colors import colorsets, single_color
    tokens = {}
    for pal_set in pal_sources:
        rand_colorset = world.random.choice(list(colorsets[pal_sources[pal_set][0]].keys()))
        i = 0
        for clrinx in pal_sources[pal_set][1]:
            if clrinx == 18:
                color = world.random.choice(single_color)
                #rom.write_bytes(pal_set+i,bytes(color))
                tokens[pal_set + i] = bytes(color)
            elif clrinx == 16:
                i = i+2
                continue
            elif clrinx == 17:
                #rom.write_bytes(pal_set+i,bytes([0x00,0x00]))
                tokens[pal_set + i] = bytes([0x00,0x00])
            else:
                color = colorsets[pal_sources[pal_set][0]][rand_colorset][clrinx]
                #rom.write_bytes(pal_set+i,bytes(color))
                tokens[pal_set + i] = bytes(color)
            i=i+2
    return tokens

def main():
    pass

if __name__ == "__main__":
    main()