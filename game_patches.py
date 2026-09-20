# Many of the follow codes were made by
# @minhnhatx and @ajip from https://fearlessrevolution.com/viewtopic.php?t=18439
from .pc_ap_methods import *

loggerDebug = logging.getLogger("Rune Factory 4 Debug")

# A single continous memory modification
class Patch:
    def __init__(
        self,
        name: str,
        description: str,
        offset: int,
        instructions: bytes
    ):
        self.name = name
        self.description = description
        self.offset = offset
        self.instructions = instructions
        self.original_bytes: bytes | None = None

    @property
    def size(self) -> int:
        return len(self.instructions)

    def verify(self, ctx) -> bool:
        address = ctx.processes_base + self.offset
        current = pc_read_bytes(ctx.pm, address, self.size)

        return current == self.instructions

    def apply(self, ctx):
        address = ctx.processes_base + self.offset
        current = pc_read_bytes(ctx.pm, address, self.size)

        if current == self.instructions:
            # Log that the patch is already applied correctly
            return

        if self.original_bytes is None:
            self.original_bytes = current

        pc_write_bytes(ctx.pm, address, self.instructions)

    def revert(self, ctx):
        address = ctx.processes_base + self.offset
        current = pc_read_bytes(ctx.pm, address, self.size)

        if self.original_bytes is None:
            # Log that we didn't capture the original bytes yet so no patch was applied
            return

        if current != self.instructions:
            # Log that the bytes do not match the instructions
            pass

        pc_write_bytes(ctx.pm, address, self.original_bytes)
        self.original_bytes = None

# A logical set of patches that belong together (e.g. savemod_1 savemod_2)
class PatchSet:
    def __init__(
        self,
        name: str,
        patches: list[Patch]
    ):
        self.name = name
        self.patches = patches

    def apply(self, ctx):
        for patch in self.patches:
            patch.apply(ctx)

    def revert(self, ctx):
        for patch in reversed(self.patches):
            patch.revert(ctx)

    def verify(self, ctx) -> bool:
        return all(
            patch.verify(ctx)
            for patch in self.patches
        )

class PatchManager:
    def __init__(self):
        self.patch_sets: list[PatchSet] = []

    def build_patches(self, ctx):
        patch_sets: list[PatchSet] = []

        patch_sets.append(
            PatchSet("Requests", [
                Patch(
                    "Open_Requests",
                    "Open Requests",
                    0x21835A,
                    bytes([0x90, 0x90, 0x90, 0x90]),
                ),
            ])
        )

        patch_sets.append(
            PatchSet("Order Flag Writes", [
                Patch(  "Order Flag Furniture Store",   "Disables the buy option for Furniture Store",
                        0x1EA65E, bytes([0xD2, 0x05, 0xCB, 0x00])),
                Patch(  "Order Flag Blossoms Grocery",  "Disables the buy option for Blossoms Groceries",
                        0x1EA66D, bytes([0xC3, 0x05, 0xCB, 0x00])),
                Patch(  "Order Flag Bados Accessories", "Disables the buy option for Bados Accessories",
                        0x1EA67C, bytes([0xB4, 0x05, 0xCB, 0x00])),
                Patch(  "Order Flag Bados Bargains",    "Disables the buy option for Bados Bargains",
                        0x1EA68B, bytes([0xA5, 0x05, 0xCB, 0x00])),
                Patch(  "Order Flag Clothing Shop",     "Disables the buy option for Clothing Shop",
                        0x1EA69A, bytes([0x96, 0x05, 0xCB, 0x00])),
                Patch(  "Order Flag Fish Market",       "Disables the buy option for Fish Market",
                        0x1EA6A9, bytes([0x87, 0x05, 0xCB, 0x00])),
                Patch(  "Order Flag Jewelry Shop",      "Disables the buy option for Jewelry Shop",
                        0x1EA6B8, bytes([0x78, 0x05, 0xCB, 0x00])),
                Patch(  "Order Flag Magic Shop",        "Disables the buy option for Magic Shop",
                        0x1EA6C7, bytes([0x69, 0x05, 0xCB, 0x00])),
                Patch(  "Order Flag Rune Ability Shop", "Disables the buy option for Rune Ability Shop",
                        0x1EA6D6, bytes([0x5A, 0x05, 0xCB, 0x00])),
                Patch(  "Order Flag Business License",  "Disables the buy option for Business License",
                        0x1EA6E5, bytes([0x4B, 0x05, 0xCB, 0x00])),
                #Patch( "Order Flag Nationalize Baths", "Disables the buy option for Nationalize Baths",
                #       0x1EA6F4, bytes([0x3C, 0x05, 0xCB, 0x00])),
            ])
        )

        patch_sets.append(
            PatchSet("Stability", [
                Patch(
                    "Main_Menu_Return_Crash",
                    "Fix return to main menu crash",
                    0x157D84,
                    bytes([0x90, 0x90, 0x90, 0x90, 0x90]),
                ),
            ])
        )

        if ctx.doctor_option:
            patch_sets.append(
                PatchSet("Free Doctor", [
                    Patch(
                        "Free_Doctor",
                        "Removes Jones' doctor fee - NOPs the 6 byte charge instruction",
                        0x20D97F,
                        bytes([0x90] * 6),
                    ),
                ])
            )

        if ctx.skill_exp_multi:
            patch_sets.append(
                PatchSet("Skill EXP Multiplier", [
                    Patch(
                        "Skill_EXP_Multiplier",
                        "Scales skill and crafting EXP by 1 << skill_exp_multi",
                        0xB3E73,
                        bytes([
                            0x48, 0xC1, 0xE7, ctx.skill_exp_multi,  # shl rdi, skill_exp_multi
                        ]) + bytes([0x90] * 10),
                    ),
                    # Patch("Disable_Craft_Exp", "Disable craft exp", 0x75629, bytes([0x90] * 6)),
                    # Patch("Disable_Upgrade_Exp", "Disable upgrade exp", 0x3F064, bytes([0x90] * 5)),
                ])
            )

        if ctx.exp_multi:
            patch_sets.append(
                PatchSet("EXP Multiplier", [
                    Patch(
                        "EXP_Multiplier",
                        "Scales combat EXP by 1 << exp_multi",
                        0xB2874,
                        bytes([
                            0x48, 0xC1, 0xE7, ctx.exp_multi,        # shl rdi, exp_multi
                        ]) + bytes([0x90] * 10),
                    ),
                ])
            )

        if ctx.gay_dating:
            patch_sets.append(
                PatchSet("Gay Dating", [
                    Patch(
                        "Gay_Dating_1",
                        "Turns the gender check into a jne so males can date males",
                        0x2044B2,
                        bytes([0x75]),
                    ),
                    Patch(
                        "Gay_Dating_2",
                        "Turns the gender check into a jne so females can date females",
                        0x2273A2,
                        bytes([0x75]),
                    ),
                ])
            )

        patch_sets.append(
            PatchSet("Taming", [
                Patch(
                    "Friend Item Tame Bonus",
                    "Triple Friend item tame bonus",
                    0x970D4,
                    bytes([
                        0x48, 0xC1, 0xE3, 0x02,                     # shl rbx, 02
                        0x90, 0x90,                                 # Nop
                    ]),
                ),
                # 0x9676D (Lucky Charm) is written by patch_injects() via lucky_charm()
            ])
        )

        patch_sets.append(
            PatchSet("Friendship", [
                Patch(
                    "Friendship_Point_Multiplier",
                    "Scales friendship point gains by 1 << fp_multi, replacing a check for Doug under specific conditions",
                    0x225F44,
                    bytes([
                        0x49, 0x8B, 0xCF,                           # mov rcx,r15 {r15: fp_add, eax: new_fp}
                        0xC1, 0xE1, ctx.fp_multi,                   # shl ecx,fp_multi
                        0x01, 0xCF,                                 # add edi,ecx
                        0xEB, 0x22,                                 # jmp RF4S.exe+225F70
                    ]) + bytes([0x90] * 34),                        # pad out the replaced Doug check
                ),
            ])
        )

        if ctx.extra_routine_ptr:
            path_ptr = ctx.extra_routine_ptr + 0x300
            patch_sets.append(
                PatchSet("Savemod", [
                    Patch(
                        "Savemod_1",
                        "Turns the if statement that leads to the temporary folder path into an unconditional jump",
                        0x254D90+0x7A,
                        bytes([
                            0xE9, 0xD0, 0x01, 0x00, 0x00,           # jmp     loc_7FF67BA94FDF
                            0x90                                    # Nop
                            ]),
                    ),
                    Patch(
                        "Savemod_2",
                        "Patches the actual save folder location",
                        0x254D90+0x24F,
                        bytes([
                            0x48, 0xBA,                             # mov     rdx, path_ptr
                            ]) + path_ptr.to_bytes(8, byteorder='little')
                          + bytes([0x90] * 9),                      # Nop out GetTempPathA
                    ),
                ])
            )

        self.patch_sets = patch_sets

    def apply(self, ctx):
        for patch_set in self.patch_sets:
            patch_set.apply(ctx)

    def revert(self, ctx):
        for patch_set in reversed(self.patch_sets):
            patch_set.revert(ctx)

    def verify(self, ctx) -> bool:
        return all(
            patch_set.verify(ctx)
            for patch_set in self.patch_sets
        )


def get_patch_manager(ctx) -> PatchManager:
    manager = getattr(ctx, "patch_manager", None)
    if manager is None:
        manager = PatchManager()
        manager.build_patches(ctx)
        ctx.patch_manager = manager
    return manager


def patch_game(ctx):
    try:
        manager = get_patch_manager(ctx)
        manager.apply(ctx)
    except Exception as e:
        loggerDebug.critical(f"Error Patching: {e}\n{traceback.format_exc()}")


def verify_patches(ctx):
    try:
        manager = get_patch_manager(ctx)
        if not manager.verify(ctx):
            manager.apply(ctx)
    except Exception as e:
        loggerDebug.critical(f"Error Verifying Patches: {e}\n{traceback.format_exc()}")

    byte_val = pc_readb(ctx.pm, ctx.processes_base + 0x1F464B)
    if byte_val == 0xC1:
        patch_injects(ctx)


def patch_injects(ctx):
    try:
        if not ctx.extra_routine_ptr:
            ctx.extra_routine_ptr = pc_alloc_mem(ctx.pm, 0x1000)
        path_str = (ctx.ap_save_seed_path).replace("\\","/")
        pc_write_bytes(ctx.pm, ctx.extra_routine_ptr + 0x300, path_str.encode())

        pc_write_bytes(ctx.pm, ctx.extra_routine_ptr + 0x200, airship_mod())
        pc_write_bytes(ctx.pm, ctx.processes_base+0x1F464B, generate_inject(ctx.extra_routine_ptr, 0x200, 2))

        pc_write_bytes(ctx.pm, ctx.extra_routine_ptr + 0x240, airship_mod_2())
        pc_write_bytes(ctx.pm, ctx.processes_base+0x21C656, generate_inject(ctx.extra_routine_ptr, 0x240, 5))


        pc_write_bytes(ctx.pm, ctx.extra_routine_ptr + 0x0, generate_fish(ctx.processes_base))
        pc_write_bytes(ctx.pm, ctx.processes_base+0x180CC0, generate_inject(ctx.extra_routine_ptr, 0, 4))

        pc_write_bytes(ctx.pm, ctx.extra_routine_ptr + 0x40, aquaticus_rain(ctx.processes_base))
        pc_write_bytes(ctx.pm, ctx.processes_base+0x185830, generate_inject(ctx.extra_routine_ptr, 0x40, 1))

        pc_write_bytes(ctx.pm, ctx.extra_routine_ptr + 0x80, ventis_wind(ctx.processes_base))
        pc_write_bytes(ctx.pm, ctx.processes_base+0x1711F4, generate_inject(ctx.extra_routine_ptr, 0x80, 20, "r14"))

        pc_write_bytes(ctx.pm, ctx.extra_routine_ptr + 0xC0, fiersome_sun(ctx.processes_base))
        pc_write_bytes(ctx.pm, ctx.processes_base+0x185C26, generate_inject(ctx.extra_routine_ptr, 0xC0, 1, "rdx"))

        pc_write_bytes(ctx.pm, ctx.extra_routine_ptr + 0x140, pandora_mandate(ctx.processes_base))
        pc_write_bytes(ctx.pm, ctx.processes_base+0x1E3841, generate_inject(ctx.extra_routine_ptr, 0x140, 3, "rcx"))

        pc_write_bytes(ctx.pm, ctx.extra_routine_ptr + 0x280, lucky_charm(ctx.processes_base))
        pc_write_bytes(ctx.pm, ctx.processes_base+0x9676D, generate_inject(ctx.extra_routine_ptr, 0x280, 2, "rcx"))

        menu_slot_row_patches(ctx)
    except Exception as e:
        loggerDebug.critical(f"Error  Injects: {e}\n{traceback.format_exc()}")

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

def menu_slot_row_patches(ctx):
    alloc_addr = ctx.extra_routine_ptr
    simple_patches = {
        0x158960: b'\x42\x0f\xB6\x84\x02\x7B\x05\x00\x00', # move text check to norad farm
    }
    for process_offset, patch_bytes in simple_patches.items():
        pc_write_bytes(ctx.pm, ctx.processes_base + process_offset, patch_bytes)
    pass

def generate_inject(alloc_ptr, offset, padding, reg="rax"):
    try:
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
    except Exception as e:
        loggerDebug.critical(f"Error Generating Inject: {e}\n{traceback.format_exc()}")
