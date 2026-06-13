# Many of the follow codes were made by 
# @minhnhatx and @ajip from https://fearlessrevolution.com/viewtopic.php?t=18439

def airship_mod():
    #flag_adr = p_base + 0xE9AC40
    working_bytes = b'\xC1\xEA\x05'                     # shr edx,05
    working_bytes += b'\x41\x8D\x40\x01'                # lea eax,[r8+01]
    working_bytes += b'\x8B\x8C\x93\xF4\x00\x00\x00'    # mov ecx,[rbx+rdx*4+000000F4]
    working_bytes += b'\x81\xF9\xFF\xFF\xFF\x00'        # cmp ecx,00FFFFFF
    working_bytes += b'\x75\x06'                        # jne 7FF73D7C016C
    working_bytes += b'\x8B\x8B\x30\xE1\x05\x00'        # mov ecx,[rbx+0005E130]
    working_bytes += b'\xC3'                            # ret
    return working_bytes

def airship_mod_2():
    working_bytes = b'\xB8\x01\x00\x00\x00'         # mov eax,00000001
    working_bytes += b'\xD3\xE0'                    # shl eax,cl
    working_bytes += b'\x49\x8D\x1C\x93'            # lea rbx,[r11+rdx*4]
    working_bytes += b'\x8B\x93\xF4\x00\x00\x00'    # mov edx,[rbx+000000F4]
    working_bytes += b'\x81\xFA\xFF\xFF\x7F\x00'    # cmp edx,007FFFFF
    working_bytes += b'\x75\x06'                    # jne 7FF73D7C025f
    working_bytes += b'\x8B\x93\x30\xE1\x05\x00'    # mov edx,[rbx+0005E130]
    working_bytes += b'\xC3'                        # ret
    return working_bytes

def generate_fish(p_base):
    # Check if carmen's bait is active, if so, spawn 20 fish, otherwise spawn 3 then return
    flag_adr = p_base + 0xE9AC3C
    working_bytes = b'\x48\xA1'                     # mov rax
    working_bytes += flag_adr.to_bytes(8, byteorder= 'little') # [RF4S.exe+E9AC38]
    working_bytes += b'\x48\x25\x00\x00\x01\x00'    # and rax,0001 0000
    working_bytes += b'\x74\x07'                    # je +7
    working_bytes += b'\xB8\x14\x00\x00\x00'        # mov eax,14
    working_bytes += b'\xEB\x02'                    # jmp +2
    working_bytes += b'\xB0\x03'                    # mov al,03
    working_bytes += b'\x44\x8B\xF0'                # mov r14d,eax
    working_bytes += b'\xC3'                        # Ret
    return working_bytes
     #,0x, 0x38,0xAC,0x66,0x3E,0xF7,0x7F,0x00,0x00, # mov rax,
    #0x48,0x25, 0x00,0x10,0x00,0x00, # and rax,00001000
    #0x74,0x06, # je 1DF0D0A0016
    #0x66,0xB8,0x14,0x00, # mov ax,14
    #0xEB,0x02, # jmp 1DF0D0A0018
    #0xB0,0x03, # mov al,03
    #0x44,0x8B,0xF0, # mov r14d,eax
    #0xC3, # Ret
    #0xFF,0x25, 0x00,0x00,0x00,0x00, 0xCC,0x0C,0x95,0x3D,0xF7,0x7F,0x00,0x00 # jmp RF4S.exe+180CCC


def aquaticus_rain(p_base):
    flag_adr = p_base + 0xE9AC3C
    working_bytes = b'\x48\xA1'                     # mov rax
    working_bytes += flag_adr.to_bytes(8, byteorder= 'little') # [RF4S.exe+E9AC38]
    working_bytes += b'\x48\x25\x00\x00\x08\x00'    # and rax,0008 0000
    working_bytes += b'\x74\x10'                    # je +10
    working_bytes += b'\x81\x4B\x04\x00\x00\x00\x20'# or [rbx+04],20000000
    working_bytes += b'\x81\x63\x04\xFF\xFF\xFF\xBF'# and [rbx+04],BFFFFFFF
    working_bytes += b'\xEB\x07'                    # jmp +7
    working_bytes += b'\x81\x63\x04\xFF\xFF\xFF\xDF'# and [rbx+04],DFFFFFFF
    working_bytes += b'\x0F\xB6\x43\x2E'            # movzx eax,byte ptr [rbx+2E]
    working_bytes += b'\x24\xFC'                    # and al,-04
    working_bytes += b'\xC3'                        # Ret
    return working_bytes

def ventis_wind(p_base):
    flag_adr = p_base + 0xE9AC3C
    working_bytes = b'\x0F\xBA\xE0\x0B'                         # bt eax,0B
    working_bytes += b'\x73\x1B'                                # jae +1B
    working_bytes += b'\xF7\x83\x38\x02\x00\x00\x00\x00\x80\x00'# test [rbx+00000238],00800000
    working_bytes += b'\x74\x0F'                                # je +F
    working_bytes += b'\xF6\x87\x58\x07\x00\x00\x04'            # test byte ptr [rdi+00000758],04
    working_bytes += b'\x75\x06'                                # jne +6
    working_bytes += b'\x81\xC6\x00\x16\x00\x00'                # add esi,00001600
    working_bytes += b'\x48\xA1'                                # move rax
    working_bytes += flag_adr.to_bytes(8, byteorder= 'little')  # [RF4S.exe+E9AC38]
    working_bytes += b'\x25\x00\x00\x10\x00'                    # and eax,0010 0000
    working_bytes += b'\x74\x06'                                # je +6
    working_bytes += b'\x81\xC6\x00\x16\x00\x00'                # add esi,00001600
    working_bytes += b'\xC3'                                    # ret
    return working_bytes

def fiersome_sun(p_base):
    flag_adr = p_base + 0xE9AC3C
    working_bytes =  b'\x44\x09\xD0'                            # or eax,r10d
    working_bytes += b'\x45\x8B\x56\x04'                        # mov r10d,[r14+04]
    working_bytes += b'\x48\x8B\xD0'                            # mov rdx,rax
    working_bytes += b'\x48\xA1'                                # mov rax,
    working_bytes += flag_adr.to_bytes(8, byteorder= 'little')  # [RF4S.exe+E9AC38]
    working_bytes += b'\x48\x25\x00\x00\x04\x00'                # and rax,0004 0000
    working_bytes += b'\x74\x07'                                # je +7
    working_bytes += b'\xBA\x00\x05\xC0\x7F'                    # mov edx,7FC006F2
    working_bytes += b'\x90\x90'                                # nop
    working_bytes += b'\x48\x8B\xC2'                            # mov rax,rdx
    working_bytes += b'\x41\x89\x06'                            # mov [r14],eax
    working_bytes += b'\x48\xA1'                                # mov rax
    working_bytes += flag_adr.to_bytes(8, byteorder= 'little')  # [RF4S.exe+E9AC38]
    working_bytes += b'\x48\x25\x00\x00\x02\x00'                # and rax,0002 0000
    working_bytes += b'\x74\x0E'                                # je +E
    working_bytes += b'\x48\xB8\x80\xFF\xFE\xFE\xFE\xFE\xFE\xFF'# mov rax,FFFEFEFEFEFEFF80
    working_bytes += b'\x49\x89\x46\x08'                        # mov [r14+08],rax
    working_bytes += b'\x41\x8B\xD2'                            # mov edx,r10d
    working_bytes += b'\xC3'                                    # ret
    return working_bytes

def pandora_mandate(p_base):
    flag_adr = p_base + 0xE9AC3C
    working_bytes = b'\x39\xD0'                                 # cmp eax,edx
    working_bytes += b'\x0F\x47\xC2'                            # cmova eax,edx
    working_bytes += b'\x83\xE7\xFE'                            # and edi,-02
    working_bytes += b'\x83\xCF\x04'                            # or edi,04
    working_bytes += b'\x66\x89\x43\xF8'                        # mov [rbx-08],ax
    working_bytes += b'\x50'                                    # push rax
    working_bytes += b'\x48\xB8'                                # mov rax,
    working_bytes += flag_adr.to_bytes(8, byteorder= 'little')  # [RF4S.exe+E9AC38]
    working_bytes += b'\x48\x25\x00\x00\x00\x01'                # and rax,0100 0000
    working_bytes += b'\x74\x08'                                # je +8
    working_bytes += b'\x66\xB8\xFF\x00'                        # mov ax,00FF
    working_bytes += b'\x66\x89\x43\xF8'                        # mov [rbx-08],ax
    working_bytes += b'\x58'                                    # pop rax
    working_bytes += b'\xC3'                                    # ret 
    return working_bytes

def lucky_charm(p_base):
    flag_adr = p_base + 0xE9AC3C
    working_bytes = b'\x48\xB8'                                # mov rax,
    working_bytes += flag_adr.to_bytes(8, byteorder= 'little')  # [RF4S.exe+E9AC3C]
    working_bytes += b'\x48\x8B\x08'                            # mov rcx,[rax]
    working_bytes += b'\x48\x81\xE1\xFF\xFF\x00\x00'            # and rcx,0000FFFF
    working_bytes += b'\x48\x81\xF9\xA2\x03\x00\x00'            # cmp rcx, 3A2
    working_bytes += b'\x7C\x04'                                # jl +4
    working_bytes += b'\x66\xB9\xA2\x03'                        # mov cx, 3A2
    working_bytes += b'\x66\x29\xCB'                            # sub bx,cx
    working_bytes += b'\x48\x2D\xD0\x5C\x00\x00'                # sub rax,00005CD0
    working_bytes += b'\x8B\x08'                                # mov ecx,[rax]
    working_bytes += b'\xC3'                                    # ret 
    return working_bytes

def generate_inject(alloc_ptr, offset, padding, reg="rax"):
    match reg:
        case "rax":
            reg_byte = b'\x48\xB8'
            call_bytes = b'\xFF\xD0'
        case "rcx":
            reg_byte = b'\x48\xB9'
            call_bytes = b'\xFF\xD1'
        case "rdx":
            reg_byte = b'\x48\xBA'
            call_bytes = b'\xFF\xD2'
        case "r14":
            reg_byte = b'\x49\xBE'
            call_bytes = b'\x41\xFF\xD6'
        case _:
            reg_byte = b'\x48\xB8'
            call_bytes = b'\xFF\xD0'
    alloc_addr = alloc_ptr + offset
    working_bytes = reg_byte # mov allocation ptr to register
    working_bytes += alloc_addr.to_bytes(8, byteorder= 'little')
    working_bytes += call_bytes #call reg
    for x in range(padding):
        working_bytes += b'\x90' # nop
    return working_bytes
