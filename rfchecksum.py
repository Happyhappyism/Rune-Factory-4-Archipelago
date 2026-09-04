import zlib
import struct
from typing import Optional, Tuple
from dataclasses import dataclass

# Taken from skyrain8149's save editor, not yet implemented into the apworld


SYS_CRC_DATA_OFF        = 8
SYS_CRC_DATA_LEN        = 9296
RF3BACKUP_BODY_LEN = 0x223A4  # 140196 bytes'
SYS_FILE_MAGIC          = b'RF4D'

@dataclass
class CRCInfo:
    stored: int
    matched_scope: Optional[Tuple[int, int]]  # (start, end_exclusive) or None
    computed: Optional[int]                   # value that matched, if any

class RF4SSave:
    def __init__(self, data: bytes) -> None:
            self.data = bytearray(data)
            self.file_type: str = self._detect_file_type()
            self.crc_info: CRCInfo = self._discover_crc_scope()

    def _detect_file_type(self) -> str:
            return 'sys' if self.data[:4] == SYS_FILE_MAGIC else 'per_slot'

    @property
    def is_sys(self) -> bool:
        return self.file_type == 'sys'

    def _crc_field_offset(self) -> int:
            # System file: 'RF4D' magic at +0, CRC stored at +4
            # Per-slot:    CRC stored at +0
            return 4 if self.is_sys else 0

    def _crc_field_offset(self) -> int:
            # System file: 'RF4D' magic at +0, CRC stored at +4
            # Per-slot:    CRC stored at +0
            return 4 if self.is_sys else 0

    def _candidate_scopes(self):
        if self.is_sys:
            # Verified live: crc32(data[8:8+9296]) on rf4_sys.sav matches the
            # stored CRC at +4. This is Save_FinalizeMetadata's invariant.
            yield (SYS_CRC_DATA_OFF, SYS_CRC_DATA_OFF + SYS_CRC_DATA_LEN)
            return
        # Per-slot file (rf3BackupSaveDataBuild scope), plus a few fallbacks.
        yield (4, 4 + RF3BACKUP_BODY_LEN)
        yield (4, len(self.data))
        yield (8, len(self.data))

    def _discover_crc_scope(self) -> CRCInfo:
        stored = struct.unpack_from('<I', self.data, self._crc_field_offset())[0]
        for start, end in self._candidate_scopes():
            if start < 0 or end > len(self.data) or end <= start:
                continue
            crc = zlib.crc32(bytes(self.data[start:end])) & 0xFFFFFFFF
            if crc == stored:
                return CRCInfo(stored, (start, end), crc)
        return CRCInfo(stored, None, None)

    def _recompute_crc(self) -> None:
        # If we couldn't verify the scope on load, fall back to the first
        # candidate scope for this file type. User will see a warning at load.
        scope = self.crc_info.matched_scope
        if scope is None:
            scope = next(iter(self._candidate_scopes()))
        start, end = scope
        crc = zlib.crc32(bytes(self.data[start:end])) & 0xFFFFFFFF
        struct.pack_into('<I', self.data, self._crc_field_offset(), crc)
        self.crc_info = CRCInfo(crc, self.crc_info.matched_scope, crc)