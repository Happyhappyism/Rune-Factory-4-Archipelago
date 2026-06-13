#!/usr/bin/python3
# Script by Ravenger, taken from https://github.com/ravener/ips-patcher

import struct
from argparse import ArgumentParser
from io import BytesIO
from pathlib import Path


def parse_ips_file(data: bytes):
    patches = []
    (P, A, T, C, H) = struct.unpack_from(">ccccc", data)

    if P != b"P" or A != b"A" or T != b"T" or C != b"C" or H != b"H":
        raise Exception("Invalid file header, not an IPS file.")

    offset = 5
    EOF = False

    while not EOF:
        # Parse patch header.
        # 3 Bytes target offset.
        # 2 Bytes patch length
        (a, b, c, length) = struct.unpack_from(">BBBH", data, offset)
        offset += 5

        # Because there's no integer type for 3 bytes
        # we parsed the individual bytes and combine it here
        target_offset = int.from_bytes([a, b, c], "big")

        # RLE Patch
        if length == 0:
            (run_len, value) = struct.unpack_from(">HB", data, offset)
            offset += 3
            patches.append((target_offset, length, run_len, value))
        else:
            patch = data[offset : offset + length]
            offset += length
            patches.append((target_offset, length, patch))

        # Check for EOF
        if offset + 3 <= len(data):
            (E, O, F) = struct.unpack_from(">ccc", data, offset)
            if E == b"E" and O == b"O" and F == b"F":
                EOF = True

    return patches


# Adds a .patched extension before the actual file extension.
# file.rom -> file.patched.rom
def filename(name: str) -> Path:
    path = Path(name)

    return path.with_suffix(".patched" + path.suffix)


def patch(rom, patches) -> bytes:
    data = BytesIO(rom)

    for offset, length, *patch in patches:
        # RLE
        if length == 0:
            (run_len, value) = patch
            data.seek(offset)
            data.write(bytes([value] * run_len))
        else:
            data.seek(offset)
            data.write(patch[0])

    return data.getvalue()


def main() -> None:
    parser = ArgumentParser(description="Patch files using a .ips patch file.")

    parser.add_argument("input", help="Input file to patch")
    parser.add_argument("patch", help="The IPS patch file to apply")
    parser.add_argument("output", help="Output File", nargs="?")

    args = parser.parse_args()

    input_file = Path(args.input)
    patch_file = Path(args.patch)
    output_file = Path(args.output or filename(args.input))

    print(f"Parsing IPS File '{patch_file}'")
    patches = parse_ips_file(patch_file.read_bytes())

    print(f"Patching File '{input_file}'")
    patched = patch(input_file.read_bytes(), patches)

    print(f"Writing Output to '{output_file}'")
    output_file.write_bytes(patched)


if __name__ == "__main__":
    main()
