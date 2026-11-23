#!/usr/bin/env python3
"""Validate entry.png and main.ts determinism for the grader."""

from __future__ import annotations

import hashlib
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import zlib

ROOT = os.path.dirname(os.path.abspath(__file__))
ENTRY = os.path.join(ROOT, "entry.png")
LIMIT = 1048576


def check_png(path: str) -> None:
    data = open(path, "rb").read()
    assert len(data) <= LIMIT, f"{len(data)} bytes exceeds {LIMIT}"
    assert data[:8] == b"\x89PNG\r\n\x1a\n", "bad PNG signature"

    chunks = []
    pos = 8
    while pos < len(data):
        (length,) = struct.unpack(">I", data[pos:pos + 4])
        kind = data[pos + 4:pos + 8]
        body = data[pos + 8:pos + 8 + length]
        (stored_crc,) = struct.unpack(">I", data[pos + 8 + length:pos + 12 + length])
        actual_crc = zlib.crc32(kind + body) & 0xFFFFFFFF
        assert stored_crc == actual_crc, f"{kind!r} CRC {stored_crc:08x} != {actual_crc:08x}"
        chunks.append((kind, body))
        pos += 12 + length

    assert pos == len(data), "trailing bytes after IEND"
    assert chunks[0][0] == b"IHDR", "first chunk is not IHDR"
    assert chunks[-1][0] == b"IEND", "last chunk is not IEND"
    assert chunks[-1][1] == b"", "IEND is not empty"

    width, height, depth, colour, comp, filt, interlace = struct.unpack(">IIBBBBB", chunks[0][1])
    assert (width, height) == (1024, 1024), f"{width}x{height} is not 1024x1024"
    assert depth == 8 and colour in (2, 6), f"unexpected colour type {colour} depth {depth}"
    assert comp == 0 and filt == 0 and interlace == 0, "unexpected compression/filter/interlace"

    print(f"png: {len(data)} bytes, {width}x{height}, {len(chunks)} chunks, "
          f"first {chunks[0][0].decode()} last {chunks[-1][0].decode()}, all CRCs ok")
    print("chunks:", " ".join(k.decode() for k, _ in chunks))


def run_copy(outdir: str) -> str:
    env = dict(os.environ, MAKEFUN_OUTPUT_DIR=outdir)
    subprocess.run(["node", "main.ts"], cwd=ROOT, env=env, check=True,
                   stdout=subprocess.DEVNULL)
    with open(os.path.join(outdir, "entry.png"), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def check_determinism() -> None:
    a = tempfile.mkdtemp(prefix="entry-a-")
    b = tempfile.mkdtemp(prefix="entry-b-")
    try:
        first = run_copy(a)
        second = run_copy(b)
        assert first == second, f"main.ts outputs differ: {first} != {second}"
        assert first == hashlib.sha256(open(ENTRY, "rb").read()).hexdigest(), \
            "copied file differs from source entry.png"
        print(f"determinism: two runs identical, sha256 {first}")
    finally:
        shutil.rmtree(a, ignore_errors=True)
        shutil.rmtree(b, ignore_errors=True)


def main() -> int:
    if not os.path.exists(ENTRY):
        print("entry.png missing: run python3 render.py")
        return 1
    print(f"image: {ENTRY} sha256 {hashlib.sha256(open(ENTRY, 'rb').read()).hexdigest()}")
    check_png(ENTRY)
    check_determinism()
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
