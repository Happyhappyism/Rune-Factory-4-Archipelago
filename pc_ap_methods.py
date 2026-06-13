import pymem
import pymem.process
import sys
import psutil
import logging
import traceback

# PC Memory Methods
logging.getLogger("pymem").setLevel(logging.CRITICAL)
logger = logging.getLogger("pc_ap_methods")



def pc_get_proc_base(proc):
    try:
        pm = pymem.Pymem(proc)
        module = pymem.process.module_from_name(pm.process_handle, proc)
        base_address = module.lpBaseOfDll
        pm.close_process()
        return base_address

    except Exception as e:
        print(f"An unexpected error occurred: {e}\n{traceback.format_exc()}")
        return None

def pc_check_process(proc):
    try:
        pm = pymem.Pymem(proc)
        pm.close_process()
        return True
    except:
        return False

def pc_get_dll_base(process_name, dll):
    pid = None
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'].lower() == process_name.lower():
            pid = proc.info['pid']
    if pid is None:
        logger.warning(f"Process '{proc}' not found.\n{traceback.format_exc()}")
        return None
    
    try:
        pm = pymem.Pymem(pid)
        module = pymem.process.module_from_name(pm.process_handle, dll)
        base = module.lpBaseOfDll
        pm.close_process()
        return base
    
    except Exception as e:
        logger.warning(f"An unexpected error occurred: {e}\n{traceback.format_exc()}")
        return None

def pc_read(pm, adr):
    try:
        #pm = pymem.Pymem(proc)
        value = pm.read_int(adr)
        #pm.close_process()
        return value
    except Exception as e:
        logger.warning(f"An error occurred: {e}\n{traceback.format_exc()}")

def pc_readb(pm, adr):
    try:
        #pm = pymem.Pymem(proc)
        value = int.from_bytes(pm.read_bytes(adr, 1))
        #pm.close_process()
        return value
    except Exception as e:
        logger.warning(f"An error occurred: {e}\n{traceback.format_exc()}")

def pc_read_bit(pm, adr, bit):
    try:
        #pm = pymem.Pymem(proc)
        value = int.from_bytes((pm.read_bytes(adr,1)))
        mask = 1 << bit
        #pm.close_process()
        return bool(value & mask)
    except Exception as e:
        logger.warning(f"An error occurred: {e}\n{traceback.format_exc()}")

def pc_read_ptr(pm, adr):
    #try:
        #pm = pymem.Pymem(proc)
    value = pm.read_longlong(adr)
        #pm.close_process()
    return value
    #except Exception as e:
    #    logger.warning(f"An error occurred: {e}\n{traceback.format_exc()}")

def pc_read_bytes(pm, adr, size):
    try:
        #pm = pymem.Pymem(proc)
        value = pm.read_bytes(adr,size)
        #pm.close_process()
        return value
    except Exception as e:
        logger.warning(f"An error occurred: {e}\n{traceback.format_exc()}")

def pc_write(pm, adr, value):
    try:
        #pm = pymem.Pymem(proc)
        pm.write_int(adr, value)
        #pm.close_process()
    except Exception as e:
        logger.warning(f"An unexpected error occurred: {e}\n{traceback.format_exc()}")
        return None
    
def pc_write_bytes(pm, adr, byte_list):
    try:
        #pm = pymem.Pymem(proc)
        pm.write_bytes(adr, byte_list, len(byte_list))
        #pm.close_process()
    except Exception as e:
        logger.warning(f"An unexpected error occurred: {e}\n{traceback.format_exc()}")
        return None
    
    
def pc_writeb(pm, adr, value):
    try:
        #pm = pymem.Pymem(proc)
        pm.write_bytes(adr, value.to_bytes(length=1, byteorder='little'), 1)
        #pm.close_process()
    except Exception as e:
        logger.warning(f"An unexpected error occurred: {e}\n{traceback.format_exc()}")
        return None
    
def pc_set_bit(pm, adr, bit, reset=False):
    try:
        #pm = pymem.Pymem(proc)
        old_value = int.from_bytes(pm.read_bytes(adr, 1))
        mask = 1 << bit
        if not reset:
            new_value = old_value | mask
        else:
            new_value = old_value & (0xFF ^ mask)
        pm.write_bytes(adr, new_value.to_bytes(length=1, byteorder='little'), 1)
        #pm.close_process()
    except Exception as e:
        logger.warning(f"An unexpected error occurred: {e}\n{traceback.format_exc()}")
        return None
    
def pc_follow_ptr_list(proc, ptr_list, dll_base):
    value = dll_base
    for offset in ptr_list:
        value = pc_read_ptr(proc, value + offset)
    return value

def pc_aob_scan(pm, byte_list):
    try:
        #bytes_pattern = bytes.fromhex(byte_list.replace(' ', ''))
        #regex_pattern = bytes_pattern.replace(b'?', b'.')
        #pm = pymem.Pymem(proc)
        pat_adr = pymem.pattern.pattern_scan_all(pm.process_handle, byte_list)
        #pm.close_process()
        return pat_adr
    except Exception as e:
        logger.warning(f"An unexpected error occurred: {e}\n{traceback.format_exc()}")
        return None
    
def pc_aob_scan_multi(pm, byte_list):
    try:
        #bytes_pattern = bytes.fromhex(byte_list.replace(' ', ''))
        #regex_pattern = bytes_pattern.replace(b'?', b'.')
        #pm = pymem.Pymem(proc)
        pat_adr = pymem.pattern.pattern_scan_all(pm.process_handle, byte_list, return_multiple = True)
        #pm.close_process()
        return pat_adr
    except Exception as e:
        logger.warning(f"An unexpected error occurred: {e}\n{traceback.format_exc()}")
        return None
    
def pc_aob_scan_wild(pm, byte_list):
    try:
        #bytes_pattern = bytes.fromhex(byte_list.replace(' ', ''))
        #regex_pattern = bytes_pattern.replace(b'?', b'.')
        #pm = pymem.Pymem(proc)
        pat_adr = pymem.pattern.pattern_scan_all(pm.process_handle, byte_list)
        #pm.close_process()
        return pat_adr
    except Exception as e:
        logger.warning(f"An unexpected error occurred scanning memory: {e}\n{traceback.format_exc()}")
        return None

def pc_alloc_mem(pm, size):
    try:
        #pm = pymem.Pymem(proc)
        adr = pm.allocate(size)
        #pm.close_process()
        return adr
    except Exception as e:
        logger.warning(f"An unexpected error occurred allocating memory: {e}\n{traceback.format_exc()}")
        return None

def pc_free_mem(pm, adr):
    try:
        pm.free(adr)
    except Exception as e:
        logger.warning(f"An unexpected error occurred freeing memory: {e}\n{traceback.format_exc()}")
        return None

def pc_aob_scan_by_module(pm, byte_list, module):
    try:
        #bytes_pattern = bytes.fromhex(byte_list.replace(' ', ''))
        #regex_pattern = bytes_pattern.replace(b'?', b'.')
        #pm = pymem.Pymem(proc)
        pat_adr = pymem.pattern.pattern_scan_module(pm.process_handle, byte_list, module)
        #pm.close_process()
        return pat_adr
    except Exception as e:
        logger.warning(f"An unexpected error occurred: {e}\n{traceback.format_exc()}")
        return None
    
